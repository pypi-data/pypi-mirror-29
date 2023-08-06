#! /usr/bin/env python

import sys, os, csv
from urlparse import urlparse


def make_download_command(val,sec, recursive_flg):    

    cmd = 'docker run -v /mnt:/mnt '
    if recursive_flg:
        cmd += '-e INPUT_RECURSIVE={} '.format(val)
    else:
        cmd += '-e INPUT={} '.format(val)

    cmd += '-e STORAGE_ACCOUNT_KEY={} '.format(sec)
    cmd += '-e DIR=/mnt/input '
    cmd += 'ken01nn/lifecycle bash /lifecycle/download.sh '
    return cmd


def make_dl_script_command(script, sec):    

    cmd = 'docker run -v /mnt:/mnt '
    cmd += '-e SCRIPT={} '.format(script)
    cmd += '-e STORAGE_ACCOUNT_KEY={} '.format(sec)
    cmd += '-e DIR=/mnt/script '
    cmd += 'ken01nn/lifecycle bash /lifecycle/download.sh '
    return cmd


def make_outdir_command(out_root_dir, task):    

    cmd = 'mkdir -p'
    for key in task.output_recursive:
        o = urlparse(task.output_recursive[key])
        cmd += ' '+ out_root_dir + o.path
    return cmd


def make_analysis_command(in_root_dir, out_root_dir, task, image, script):    

    cmd = 'docker run -v /mnt:/mnt'

    for key in task.inputs:
        o = urlparse(task.inputs[key])
        cmd += ' -e ' + key + '=' + in_root_dir + o.path
    for key in task.input_recursive:
        o = urlparse(task.input_recursive[key])
        cmd += ' -e ' + key + '=' + in_root_dir + o.path
    for key in task.output_recursive:
        o = urlparse(task.output_recursive[key])
        cmd += ' -e ' + key + '=' + out_root_dir + o.path
    for key in task.env:
        cmd += ' -e ' + key + '=\"' + task.env[key] + '\"'

    cmd += ' ' + image + ' bash ' + script
    return cmd


def make_upload_command(out_url, sec):    

    o = urlparse(out_url)
    cmd = 'docker run -v /mnt:/mnt '
    cmd += '-e SRC=/mnt/output'+ o.path +' '
    cmd += '-e DEST={} '.format(out_url)
    cmd += '-e STORAGE_ACCOUNT_KEY={} '.format(sec)
    cmd += 'ken01nn/lifecycle bash /lifecycle/upload.sh '
    return cmd

