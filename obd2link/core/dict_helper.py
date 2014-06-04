import logging
import json
from collections import OrderedDict


class DictHelper:
    def __init__(self):
        self.logger = logging.getLogger("dictHelper")

    def search_by_value(self, some_dict, search_age):
        self.logger.debug('In searchByValue: list={0}, search_age={1}'.format(list, search_age))
        return some_dict.keys()[some_dict.values().index(search_age)]

    # will update or and new key if key is not already there
    def update_dict(self, any_dict, key, newvalue):
        self.logger.debug('In update_dict: key={0}, newvalue={1}'.format(key, newvalue))
        any_dict[key] = newvalue

        self.logger.debug('Updated Value of any_dict is: {0}'.format(any_dict[key]))

        return any_dict

    def update_key(self, any_dict, new_key, old_key):
        self.logger.debug('In update_dict: new_key={0}, old_key={1}'.format(old_key, new_key))
        any_dict[new_key] = any_dict.pop(old_key)

        self.logger.debug('Updated Value of any_dict is: {0}'.format(any_dict[new_key]))

        return any_dict

    def string_to_JSON(self, string):
        self.logger.debug('In stringToJSON: string={0}'.format(string))
        json_acceptable_string = string.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        return d

    def is_empty(self, any_structure):
        self.logger.debug('stucture to be validated {0}'.format(any_structure))
        if any_structure:
            #print('Structure is not empty.')
            return False
        else:
            #print('Structure is empty.')
            return True

    def sort_dict(self, any_dict):
        self.logger.debug('In Sort_dict: {0}'.format(any_dict))
        return sorted(any_dict, key=lambda key: any_dict[key])
        #any_dict = OrderedDict(sorted(any_dict.items(), key=lambda t: t[0]))
        #return any_dict