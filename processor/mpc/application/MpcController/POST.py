import common
import core

import os
from pathlib import Path


class PostClass(core.BaseClass):
    def start(self, minimal=False):
        result = True
        if not minimal:
            result &= self._disk_test()
        result &= self._file_check()
        return result
        
    def _disk_test(self):
        if not common.CDS.read('platform') == 'Linux':
            self.logger.warning('Disk test: platform not supported')
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
            self.logger.info(result_map[return_code])
            return True
        elif return_code in [1,2,4]:
            self.logger.warning(result_map[return_code])
        elif return_code in result_map.keys():
            self.logger.error(result_map[return_code])
        else:
            self.logger.error('Unknown error code {}'.format(return_code))
        return False
        
    def _file_check(self):
        result = True
        for key, item in common.Paths.items():
            if not os.path.exists(item):
                self.logger.critical('File does not exist: {}'.format(item))
                result &= False
        return result
        
        