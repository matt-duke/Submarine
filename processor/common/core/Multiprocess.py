import logging
import multiprocessing
import multiprocessing.managers as m
import queue, threading


#https://stackoverflow.com/questions/46779860/multiprocessing-managers-and-custom-classes
# Backup original AutoProxy function
backup_autoproxy = multiprocessing.managers.AutoProxy

# Defining a new AutoProxy that handles unwanted key argument 'manager_owned'
def redefined_autoproxy(token, serializer, manager=None, authkey=None,
          exposed=None, incref=True, manager_owned=True):
    # Calling original AutoProxy without the unwanted key argument
    return backup_autoproxy(token, serializer, manager, authkey,
                     exposed, incref)

# Updating AutoProxy definition in multiprocessing.managers package
multiprocessing.managers.AutoProxy = redefined_autoproxy


class ProxyServer(m.BaseManager):
    def __init__(self):
        m.BaseManager.__init__(self)
        
        # Defaults of SyncManager (https://github.com/python/cpython/blob/3.7/Lib/multiprocessing/managers.py)
        self.register('Queue', queue.Queue)
        self.register('JoinableQueue', queue.Queue)
        self.register('Event', threading.Event, m.EventProxy)
        self.register('Lock', threading.Lock, m.AcquirerProxy)
        self.register('RLock', threading.RLock, m.AcquirerProxy)
        self.register('Semaphore', threading.Semaphore, m.AcquirerProxy)
        self.register('BoundedSemaphore', threading.BoundedSemaphore,
                             m.AcquirerProxy)
        self.register('Condition', threading.Condition, m.ConditionProxy)
        self.register('Barrier', threading.Barrier, m.BarrierProxy)
        self.register('Pool', m.pool.Pool, m.PoolProxy)
        self.register('list', list, m.ListProxy)
        self.register('dict', dict, m.DictProxy)
        self.register('Value', m.Value, m.ValueProxy)
        self.register('Array', m.Array, m.ArrayProxy)
        self.register('Namespace', m.Namespace, m.NamespaceProxy)
        
    def start(self):
        m.BaseManager.start(self)