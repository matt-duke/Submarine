import common
import core.BaseClass


class PostClass(core.BaseClass):
    def __init__(self): 
        core.BaseClass.__init__(self)
        
    def dpkg_list(self):
        cmd = self.systemCall('dpkg -l')
        if cmd.returncode > 0:
            self.logger.critical("Failed to list packages")
        return cmd.stdout.stdout