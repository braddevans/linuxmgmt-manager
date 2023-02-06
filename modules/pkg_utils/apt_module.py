import asyncio
import os
import subprocess
import sys
import time

import psutil

from util.ConfigManager import ConfigManager

config_manager = ConfigManager()
config = config_manager.get_config()


#
# Any function suffixed with Worker will be run by the ModuleManager
#

# new modules are configured by placing the following object into config.json
#
# module_name = file_name without .py,  example: (apt_module) would be (apt_module.py)
# dir = module/{directory_name}/ ,      example: (pkg_utils) would be (modules/pkg_utils/)
# check_time: is not implemented yet but would be available when importing config.json
# "module_name": {
#   "enabled": true,
#   "dir": "pkg_utils",
#   "term": "/bin/bash",
#   "check_time": "30m"
# }

async def updateCheckerWorker(logger, wait_time=915):
    prefix = "apt_update_checker"
    while True:
        term_subprocess_handler(logger, "apt-get -q -y --ignore-hold --allow-change-held-packages --allow-unauthenticated -s dist-upgrade | /bin/grep  ^Inst | wc -l")
        logger.log_message(prefix, "Apt Update Checker Worker Executed, waiting for {}".format(
            time.strftime("Hours: %H, Minutes: %M, Seconds: %S", time.gmtime(wait_time)))
                           )
        await asyncio.sleep(wait_time)


def term_subprocess_handler(logger, command):
    prefix = "apt_term_process_handler"
    is_windows = sys.platform.startswith('win')
    logger.log_message(prefix, "is_windows: " + str(is_windows))
    if is_windows:
        command = "echo This wont work on windows"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        logger.log_message(prefix, str(output, 'utf-8').replace("\n", ""))
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        str_processed = str(output, 'utf-8').replace("\n", "")
        if int(str_processed) > 0:
            logger.log_message(prefix, f"{str_processed} packages to update.")

    psutil_proc = psutil.Process(os.getppid())
    proc_children = psutil_proc.children(recursive=True)
    logger.log_message(prefix, str(proc_children))
