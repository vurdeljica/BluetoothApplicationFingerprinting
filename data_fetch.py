import os
from btsnooz import *
import time

BLUETOOTH_MANAGER_LOG = "bluetooth_manager.log"
BTSNOOP_LOG = "btsnoop.log"


def fetch_bluetooth_manager_logs():
    os.system('adb shell dumpsys bluetooth_manager > ' + BLUETOOTH_MANAGER_LOG)


def extract_btsnoop_log():
    parse_log(BLUETOOTH_MANAGER_LOG, BTSNOOP_LOG)


def turn_bluetooth_on():
    os.system('adb shell settings put global bluetooth_disabled_profiles 1')


def turn_bluetooth_off():
    os.system('adb shell settings put global bluetooth_disabled_profiles 0')


def clear_bluetooth_data():
    os.system('adb shell "pm clear com.android.bluetooth > /dev/null"')


def get_application_full_package_name(application_name):
    all_packages = os.popen('adb shell cmd package list packages').read().splitlines()
    for package_name in all_packages:
        if application_name in package_name:
            package_name = package_name.replace('package:', '')
            return package_name

    return 'none'


def start_application(application_name):
    os.system('adb shell "monkey -p ' + get_application_full_package_name(application_name) +
              ' -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1"')


# necessary in order to clear previous logs
# turn_bluetooth_off()
# turn_bluetooth_on()


clear_bluetooth_data()
#start_application('linkedin')
time.sleep(30)
fetch_bluetooth_manager_logs()
extract_btsnoop_log()
