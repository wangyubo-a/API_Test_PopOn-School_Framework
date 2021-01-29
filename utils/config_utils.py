# -*- coding:UTF-8 -*-
import os
import configparser
import time

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'conf', 'localconfig.ini')


class ConfigUtils:
    def __init__(self, cfg_path=config_file_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    @property
    def HOSTS(self):
        hosts_value = self.cfg.get('default', 'hosts')
        return hosts_value

    @property
    def LOG_NAME(self):
        log_name_value = '%s_%s.log' % (self.cfg.get('default', 'log_name'), time.strftime('%Y_%m_%d'))
        return log_name_value

    @property
    def REPORT_PATH(self):
        report_path_value = self.cfg.get('path', 'REPORT_PATH')
        return report_path_value


local_config = ConfigUtils()

if __name__ == "__main__":
    print(local_config.LOG_NAME)
