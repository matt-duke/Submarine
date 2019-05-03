import sqlite3
import platform
import subprocess
import logging
import common
from common.data_types import OpMode

logger = logging.getLogger(__name__)

def disk_test():
    if not common.PLATFORM == 'Linux':
        logger.warning('Disk test: platform not supported')
        return True
        
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
        
def sensor_test():
    pass

def permissions_test():
    pass
    
def interface_test():
    result = True
    for IF in common.BusManager.list():
        IF_test_result = bool(IF.connection_test())
        if not IF_test_result:
            logger.error("{} failed connection test".format(IF.name))
        result &= IF_test_result
    return result
     
def run():
    old_mode = common.MODE
    common.MODE = OpMode.test
    logger.debug("Entering mode {}".format(common.MODE))
    result = disk_test()
    result &= interface_test()
    if not result:
        logger.critical("POST failed, changing to critical mode")
        common.MODE = OpMode.critical
    else:
        common.MODE = old_mode
        logger.debug("Entering mode {}".format(common.MODE))
    