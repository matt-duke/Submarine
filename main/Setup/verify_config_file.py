import re
import os
import configparser

import logging
logger = logging.getLogger(__name__)

import common

def compare_options(schema_options, options):
    result = True
    for key, item in schema_options.items():
        if key not in options.keys():
            logger.critical('Invalid config file: Missing {} '.format(key))
            result = False
        else:
            type_dict = {'INT': int,
                         'BOOL': bool,
                         'STRING':str}

            if not item == 'LOGLEVEL':
                try:
                    type_dict[item](options[key])
                except:
                    result = False
                    logger.critical('Invalid config file: {} invalid type'.format(options[key]))
            else:
                result &= options[key] in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    return result

def verify_config_file(config):     
    result = True
    schema_file = common.Paths['CONFIG_SCHEMA']
    schema = configparser.ConfigParser()
    schema.read(schema_file)
    
    for section in schema.sections():        
        if not config.has_section(section):
            pattern = '{.*}'
            replace = '.+'
            match = re.sub(pattern, replace, section)
            #No matches found
            if match == None:
                result = False
                logger.critical('Invalid config file: missing section {}'.format(section))
                break
            #Find match in config file
            for s in config.sections():
                if re.match(match,s):
                    result &= compare_options(schema[section],config[s])
 
        else:
            result &= compare_options(schema[section], config[section])
            
    logger.info('Config file test passed: {}'.format(result))