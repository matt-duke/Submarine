import logging

logger = logging.getLogger(__name__)

def verify_src_module(module):
    result = True
    expected = ['setup','loop','test']
    for e in expected:
        if not hasattr(module, e):
            result = False
            logger.critical('Missing module: {}'.format(e))
    return result