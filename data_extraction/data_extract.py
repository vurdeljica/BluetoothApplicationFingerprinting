import pyshark
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from DeviceFilter import DeviceFilter
import seaborn as sns
import os
from PacketSizeFilter import PacketSizeFilter
from ProtocolFilter import ProtocolFilter
from Filter import Filter
import fs_util
import paths
import os


class Bluetooth:
    DIRECTION_SENT = 0
    DIRECTION_RECEIVED = 1

class DataExtract:
    def __init__(self):
        self.__filters = [DeviceFilter('controller')]
        self.__source = paths.BTSNOOP_LOG
        self.__destination = paths.RESULT_DIR

    def set_source(self, source):
        self.__source = source

    def set_destination(self, destination):
        self.__destination = destination

    def __filter_packets(self, packets, filters):
        filtered_packets = packets
        for filter in filters:
            filtered_packets = filter.filter(filtered_packets)

        return filtered_packets

    def __calculate_inter_arrival_time(self, packets):
        inter_arrival_times_ms = []

        previous_timestamp_s = float(packets[0][1].sniff_timestamp)
        for packet in packets:
            packet_body = packet[1]
            packet_timestamp_s = float(packet_body.sniff_timestamp)
            inter_arrival_times_ms.append((packet_timestamp_s - previous_timestamp_s) * 1000)
            previous_timestamp_s = packet_timestamp_s

        return inter_arrival_times_ms

    def __extract_protocol_data(self):
        pass

    def __extract_data(self, packets, extracted_log_path):
        total_summed_size_of_packages_B = 0
        num_of_bytes_sent = 0
        num_of_bytes_received = 0

        total_num_of_packages = 0
        num_of_received_messages = 0
        num_of_sent_messages = 0

        sample_duration_s = 0

        min_packet_size_B = 0
        max_packet_size_B = 0


        for packet in packets:
            packet_short_info = packet[0]
            packet_body = packet[1]

            direction = int(packet_body.hci_h4.direction, 16)
            is_packet_sent = direction == Bluetooth.DIRECTION_SENT
            packet_size = int(packet_body.length)

            total_num_of_packages += 1
            sample_duration_s = float(packet_body.sniff_timestamp) - float(packets[0][1].sniff_timestamp)
            total_summed_size_of_packages_B += packet_size

            if is_packet_sent:
                num_of_bytes_sent += packet_size
                num_of_sent_messages += 1
            else:
                num_of_bytes_received += packet_size
                num_of_received_messages += 1

        num_of_total_packets_per_second = total_num_of_packages / sample_duration_s
        num_of_sent_packets_per_second = num_of_sent_messages / sample_duration_s
        num_of_received_packets_per_second = num_of_received_messages / sample_duration_s

        avg_packet_size_B = total_summed_size_of_packages_B / total_num_of_packages
        avg_sent_packet_size_B = num_of_bytes_sent / num_of_sent_messages
        avg_received_packet_size_B = num_of_bytes_sent / num_of_received_messages

        throughput_B_per_second = total_summed_size_of_packages_B / sample_duration_s

        """columns = ['total_num_of_packages', 'num_of_received_messages', 'num_of_sent_messages',
                   'total_summed_size_of_packages_B', 'num_of_bytes_sent', 'num_of_bytes_received',
                   'sample_duration_s', 'avg_packet_size_B']"""
        columns = ['num_of_total_packets_per_second','num_of_sent_packets_per_second',
                   'num_of_received_packets_per_second','avg_packet_size_B','avg_sent_packet_size_B',
                   'avg_received_packet_size_B','throughput_B_per_second']
        df = pd.DataFrame(columns=columns)
        df_length = len(df)
        df.loc[df_length] = [num_of_total_packets_per_second, num_of_sent_packets_per_second,
                             num_of_received_packets_per_second, avg_packet_size_B,
                             avg_sent_packet_size_B, avg_received_packet_size_B, throughput_B_per_second]
        df.to_csv(extracted_log_path, index=False)

        """print("\nBEGIN\n")
        print(extracted_log_path )
        print(' ')

        print('total_num_of_packages:', total_num_of_packages)
        print('num_of_received_messages:', num_of_received_messages)
        print('num_of_sent_messages:', num_of_sent_messages)

        print(' ')

        print('total_summed_size_of_packages_B:', total_summed_size_of_packages_B)
        print('num_of_bytes_sent:', num_of_bytes_sent)
        print('num_of_bytes_received:', num_of_bytes_received)


        print(' ')
        print('sample_duration_s:', sample_duration_s)
        print('avg_packet_size_B:', avg_packet_size_B)
        print("\nEND\n")"""

    def __extract_log(self, result_dir_path, raw_log_path):
        extracted_log_path = os.path.join(result_dir_path,
                                          fs_util.get_file_name_without_extension(fs_util.get_name_from_path(raw_log_path)) + ".csv")

        file_capture = pyshark.FileCapture(input_file=raw_log_path)
        packets_body = list(file_capture)
        packets_body = packets_body[1:]
        file_capture.close()

        file_capture_summary = pyshark.FileCapture(input_file=raw_log_path, only_summaries=True)
        packets_summary = list(file_capture_summary)

        file_capture_summary.close()

        del file_capture
        del file_capture_summary

        packets = zip(packets_summary, packets_body)
        packets = self.__filter_packets(packets, self.__filters)

        self.__extract_data(packets, extracted_log_path)

        """
        inter_arrival_times_ms = np.array(self.__calculate_inter_arrival_time(packets))

        df = pd.DataFrame()
        df['inter_arrival_time'] = pd.Series(inter_arrival_times_ms)

        df.to_csv(extracted_log_path)
        """

    def extract_single_file(self):
        if not fs_util.check_if_file_exists(self.__source):
            print("Invalid source file: " + self.__source)
            return

        if not fs_util.check_if_directory_exists(self.__destination):
            print("Invalid destination directory: " + self.__destination)
            return

        self.__extract_log(self.__destination, self.__source)


    def extract_all(self):
        # check if source directory exists:
        # check if destination directory exists
        # create directory with extracted data
        #
        # for every directory
            # create extracted subdirectory
            # for every log
                # create extracted data

        if not fs_util.check_if_directory_exists(self.__source):
            print("Invalid source directory: " + self.__source)
            return

        if fs_util.check_if_directory_exists(self.__destination):
            is_destination_deleted = fs_util.delete_directory(self.__destination)
            if not is_destination_deleted:
                print("Couldn't delete: " + self.__destination)
                return

        is_destination_created = fs_util.make_directory(self.__destination)
        if not is_destination_created:
            print("Couldn't make destination directory: " + self.__destination)
            return

        application_dir_paths = fs_util.get_list_of_subdirectory_paths(self.__source)
        for application_dir_path in application_dir_paths:
            application_extracted_dir_path = self.__destination + "/" + fs_util.get_name_from_path(application_dir_path)
            is_dir_created = fs_util.make_directory(application_extracted_dir_path)
            if not is_dir_created:
                print("Error while creating directory: " + application_extracted_dir_path)

            application_log_names = fs_util.get_list_of_file_paths_in_directory(application_dir_path)
            for application_log_name in application_log_names:
                #print(application_extracted_dir_path, application_log_name)
                #self.__extract_log(application_extracted_dir_path, application_log_name)

                # Hack due to bug in pyshark
                os.system('python ' + paths.MAIN_CLI_FILE_PATH + ' data_extract --file -src '+ application_log_name +
                          ' -dst ' + application_extracted_dir_path)


