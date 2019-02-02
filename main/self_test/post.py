import sqlite3
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

PLATFORM = platform.system()

def disk_test():
    if not PLATFORM == 'Linux':
        logger.warning('Disk test: platform not supported')
        return
        
    result_map = { 0: 'No errors',
                   1: 'File system errors corrected',
                   2: 'System should be rebooted',
                   4: 'File system errors left uncorrected',
                   8: 'Operational error',
                   16: 'Usage or syntax error',
                   32: 'Fsck canceled by user request',
                   128: 'Shared library error' }
                   
    return_code = subprocesses.call('fsck -T', shell=True)
    
    if return_code == 0:
        logger.info(result_map[return_code])
        return True
    elif return_code in [1,2,4]:
        logger.warning(result_map[return_code])
    elif return_code in result_map.keys():
        logger.error(result_map[return_code])
    else:
        logger.error('Unknown error code {}'.format(return_code))
    return False
        

def run_post():
    disk_test()
    