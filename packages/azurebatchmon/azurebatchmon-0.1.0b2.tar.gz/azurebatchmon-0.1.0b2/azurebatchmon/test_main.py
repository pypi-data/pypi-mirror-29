
from task_parser import *
from command_maker import *

filename = "bwa-alignment-tasks-ubuntu.tsv"
tasks = parseTasksFile(filename)

commands = []
'''
for idx, task in enumerate(tasks):
    for input_key in task.inputs:
        command = make_download_command(task.inputs[input_key], "sec", False)
        commands.append(command)
print commands[2]
'''
'''
for idx, task in enumerate(tasks):
    command = make_analysis_command("/mnt/input", "/mnt/output", task, "image", "script")
    commands.append(command)
print commands[0]
print commands[1]
'''
'''
for idx, task in enumerate(tasks):
    for output_key in task.output_recursive:
        command = make_upload_command(task.output_recursive[output_key], "sec")
        commands.append(command)
print commands[0]
'''
for idx, task in enumerate(tasks):
    command = make_outdir_command("/mnt/output", task)
    commands.append(command)
print commands[0]

