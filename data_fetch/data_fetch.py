import os
import time
import fs_util
import paths
from btsnooz import parse_log


class DataFetch:
    def __init__(self, timeout_s = 30):
        self.__timeout_s = timeout_s
        self.__destination = paths.BTSNOOP_LOG
        if not os.path.exists(paths.RESULT_DIR):
            os.makedirs(paths.RESULT_DIR)

    @staticmethod
    def __fetch_bluetooth_manager_logs():
        os.system('adb shell dumpsys bluetooth_manager > ' + paths.BLUETOOTH_MANAGER_LOG)

    def __extract_btsnoop_log(self):
        parse_log(paths.BLUETOOTH_MANAGER_LOG, self.__destination)

    @staticmethod
    def __clear_bluetooth_data():
        os.system('adb shell "pm clear com.android.bluetooth > /dev/null"')

    @staticmethod
    def __get_application_full_package_name(application_name):
        all_packages = os.popen('adb shell cmd package list packages').read().splitlines()
        for package_name in all_packages:
            if application_name in package_name:
                package_name = package_name.replace('package:', '')
                return package_name

        return 'none'

    @staticmethod
    def __start_application(application_name):
        os.system('adb shell "monkey -p ' + DataFetch.__get_application_full_package_name(application_name) +
                  ' -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1"')

    def set_destination(self, destination):
        self.__destination = destination

    def set_timeout(self, timeout_s):
        self.__timeout_s = timeout_s

    def start(self):
        self.__clear_bluetooth_data()
        time.sleep(self.__timeout_s)
        self.__fetch_bluetooth_manager_logs()
        self.__extract_btsnoop_log()
