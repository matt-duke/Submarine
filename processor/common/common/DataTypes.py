import time
import types

class DataClass:
    def __init__(self, type):
        self.type = type
        self.value = self.type(None)
        
    def set(self):
        self.value = self.type(val)
        
    def get(self):
        return self.value


class SensorClass(DataClass):
    timeout = 30
    def __init__(self, type, unit=''):
        DataClass.__init__(self)
        self.valid = False
        self.timestamp = 0
        self.unit = unit
        
    def set(self, val):
        self.value = self.type(val)
        self.timestamp = time.time()
        self.valid = True
        
    def get(self):           
        if all([((time.time()-self.timestamp) > SensorClass.timeout)]):
            self.valid = False
        return self.value
        
    def is_valid(self):
        return self.valid
        
        
class SettingClass():
    def __init__(self, val):
        self.value = val
        self.subscribers = []
    
    def __setter(self, value):
        self.value = value
        for sub in self.subscribers:
            if sub.on_set:
                sub(self.value)
        
    def add_subscriber(self, fn, on_set=True, on_get=False):
        if type(fn) == types.FunctionType:
            fn.on_set = on_set
            fn.on_read = on_get
            self.subscribers.append(fn)
            
    def __clear_subscribers(self):
        self.subscribers = []
    
    def __getter(self):
        for sub in self.subscribers:
            if sub.on_get:
                sub(self.value)
        return self.value
        
    self.value = property(self.__getter, self.__setter)