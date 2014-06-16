import csv
import os
import ConfigParser
import usb

from yaml import load

import core.dict_helper as dict_helper
import logging.config
import sys
import cPickle as pickle


class PropertiesHelper:

    def get_usb(self):
        for dev in usb.core.find(find_all=True):
            print "Device:", dev.filename
            print "  idVendor: %d (%s)" % (dev.idVendor, hex(dev.idVendor))
            print "  idProduct: %d (%s)" % (dev.idProduct, hex(dev.idProduct))

    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def set_logger(self, conf_file):
        try:
            if conf_file is not None:
                logging.config.dictConfig(conf_file)
        except:
            print "Error setting up logging: ", sys.exc_info()[0]

    def write_csv(self, some_dict, file_location):

        dh = dict_helper.DictHelper()
        dh.sort_dict(some_dict)

        with open(file_location, 'wb') as f:
            self.w = csv.DictWriter(f, some_dict.keys())
            #TODO if there is a header append to the bottom of the file
            self.w.writeheader()
            self.w.writerow(some_dict)

    def write_pickle(self, some_dict, file_location):
        with open(file_location, 'wb') as output:
            pickle.dump(some_dict, output, -1)

    def get_yaml_config(self, *args, **kwargs):

        # change it to take filename with path
        self.default_config_file = kwargs.get('default_config_file', None)
        self.use_override = kwargs.get('use_override', False)
        self.use_full_path = kwargs.get('use_full_path', False)
        self.filename = kwargs.get('filename', None)

        try:
            if not self.default_config_file:
                default_config_path, filename = os.path.split(os.path.abspath(__file__))
                default_config_file = os.path.join(default_config_path, 'config', self.filename)
            conf_file = None
            # override
            if self.use_override and os.path.exists(os.path.join(os.getenv("HOME"), 'config', self.filename)):
                conf_file = os.path.join(os.getenv("HOME"), 'config', self.filename)
            elif self.use_full_path and os.path.exists(self.filename):
                conf_file = self.filename
            elif default_config_file is not None and os.path.exists(default_config_file):
                conf_file = default_config_file
            if conf_file is not None:
                config = load(open(conf_file, 'r'))
                return config
        except:
            print "Error loading yaml config: ", sys.exc_info()[0]
            raise

    def get_configparser_config(self, *args, **kwargs):

        # change it to take filename with path
        self.filename = kwargs.get('filename', None)
        self.use_override = kwargs.get('use_override', False)
        self.use_full_path = kwargs.get('use_full_path', False)
        self.section = kwargs.get('section', None)

        try:
            if not self.default_config_file:
                default_config_file = os.path.join(__file__[:__file__.rfind('lib')], 'config', self.filename)
            conf_file = None
            # override
            if self.use_override and os.path.exists(os.path.join(os.getenv("HOME"), 'config', self.filename)):
                conf_file = os.path.join(os.getenv("HOME"), 'config', self.filename)
            elif self.use_full_path and os.path.exists(self.filename):
                conf_file = self.filename
            elif default_config_file is not None and os.path.exists(default_config_file):
                conf_file = default_config_file
            if conf_file is not None:
                config = ConfigParser.SafeConfigParser()
                config.read(self.propertiesFile)
                propertiesDict = dict(config._sections[self.section], raw=True)
            return propertiesDict
        except:
            print "Error loading configparser config: ", sys.exc_info()[0]
            raise
