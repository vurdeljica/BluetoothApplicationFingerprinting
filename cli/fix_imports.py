import sys
import os

dir_path = os.path.abspath(os.path.dirname(__file__))

sys.path.append(dir_path + r"\..")
sys.path.append(dir_path + r"\..\learning")
sys.path.append(dir_path + r"\..\data_extraction")
sys.path.append(dir_path + r"\..\data_extraction\bt_filters")
sys.path.append(dir_path + r"\..\data_fetch")
sys.path.append(dir_path + r"\..\util")
