#! /usr/bin/env python

from __future__ import print_function
import datetime
import os
import sys
import time
import client_util
import uuid

import azure.storage.blob as azureblob
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
import common.helpers  # noqa

from task_parser import *
from command_maker import *

def run(args):

    start_time = datetime.datetime.now().replace(microsecond=0)
    print('Sample start: {}'.format(start_time))
    print()

    id_suffix = uuid.uuid4().hex[1:16]
    JOB_ID = args.JOB_ID +"-"+ id_suffix 
    POOL_ID = args.POOL_ID +"-"+ id_suffix

    # Create a Batch service client.
    credentials = batchauth.SharedKeyCredentials(
        args.BATCH_ACCOUNT_NAME,
        args.BATCH_ACCOUNT_KEY)

    batch_client = batch.BatchServiceClient(
        credentials,
        base_url=args.BATCH_ACCOUNT_URL)

    blob_client = azureblob.BlockBlobService(
        account_name=args.STORAGE_ACCOUNT_NAME,
        account_key=args.STORAGE_ACCOUNT_KEY)

    blob_client.create_container(
        args.APP_CONTAINER,
        fail_on_exist=False)

    script_files = [
        client_util.upload_file_to_container(blob_client,
             args.APP_CONTAINER,
             os.path.realpath(args.script))
    ]

    # The resource files we pass in are used for configuring the pool's
    # start task, which is executed each time a node first joins the pool
    pool_start_commands = [
        'sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common',
        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
        'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
        'sudo apt-get update',
        'sudo apt-get install -y docker-ce',
    ]

    # Create the pool that will contain the compute nodes that will execute the
    # tasks.
    client_util.create_pool(batch_client,
        POOL_ID,
        script_files,
        args.NODE_OS_PUBLISHER,
        args.NODE_OS_OFFER,
        args.NODE_OS_SKU,
        args.POOL_VM_SIZE,
        args.POOL_NODE_COUNT,
        pool_start_commands)

    # Create the job that will run the tasks.
    client_util.create_job(batch_client,
        JOB_ID,
        POOL_ID)

    run_elevated = batchmodels.UserIdentity(
        auto_user=batchmodels.AutoUserSpecification(
        scope=batchmodels.AutoUserScope.pool,
        elevation_level=batchmodels.ElevationLevel.admin,))

    script_url = "https://"+ args.STORAGE_ACCOUNT_NAME +".blob.core.windows.net/"+ args.APP_CONTAINER +"/"+ os.path.basename(args.script)

    tasks = list()
    in_tasks = parseTasksFile(args.tasks)
    for idx, task in enumerate(in_tasks):

        commands = list()
        commands.append(
            make_dl_script_command(script_url,
                args.STORAGE_ACCOUNT_KEY))

        for input_key in task.inputs:
            if len(task.inputs[input_key]) > 0:
                commands.append(
                    make_download_command(task.inputs[input_key],
                        args.STORAGE_ACCOUNT_KEY, False))

        for input_key in task.input_recursive:
            if len(task.input_recursive[input_key]) > 0:
                commands.append(
                    make_download_command(task.input_recursive[input_key],
                        args.STORAGE_ACCOUNT_KEY, True))

        commands.append(make_outdir_command("/mnt/output", task))
        commands.append(
            make_analysis_command("/mnt/input", "/mnt/output",
                task, args.image, 
                "/mnt/script/"+args.APP_CONTAINER+"/"+os.path.basename(args.script)))

        for output_key in task.output_recursive:
            commands.append(
                make_upload_command(task.output_recursive[output_key],
                    args.STORAGE_ACCOUNT_KEY))

        tasks.append(batch.models.TaskAddParameter(
                'azbatchmon_task{}'.format(idx),
                common.helpers.wrap_commands_in_shell('linux', commands),
                user_identity=run_elevated))

    batch_client.task.add_collection(JOB_ID, tasks)

    # Pause execution until tasks reach Completed state.
    client_util.wait_for_tasks_to_complete(batch_client,
               JOB_ID,
               datetime.timedelta(minutes=int(120)))

    print("  Success! All tasks reached the 'Completed' state within the "
          "specified timeout period.")

    if not args.debug:
        batch_client.job.delete(JOB_ID)
        batch_client.pool.delete(POOL_ID)

    # Print out some timing info
    end_time = datetime.datetime.now().replace(microsecond=0)
    print()
    print('Sample end: {}'.format(end_time))
    print('Elapsed time: {}'.format(end_time - start_time))

