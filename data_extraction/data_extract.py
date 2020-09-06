import pandas as pd
import matplotlib.pyplot as plt
import pyshark
import numpy as np
from DeviceFilter import DeviceFilter
import seaborn as sns
import os
from PacketSizeFilter import PacketSizeFilter
from ProtocolFilter import ProtocolFilter
from Filter import Filter


class DataExtract:
    def __init__(self):
        self.__filters = [DeviceFilter('controller')]
        self.__source = dir_path = os.path.abspath(os.path.dirname(__file__)) + r'\btsnoop.log'
        self.__destination = ""

    def set_source(self, source):
        self.__source = source

    def set_destination(self, destination):
        self.__destination = destination

    def start(self):
        packets_body = list(pyshark.FileCapture(self.__source))
        packets_body = packets_body[1:]
        packets_summary = list(pyshark.FileCapture(self.__source, only_summaries=True))

        packets = zip(packets_summary, packets_body)
        packets = self.__filter_packets(packets, self.__filters)

        inter_arrival_times = np.array(self.__calculate_inter_arrival_time(packets))
        print(inter_arrival_times)

        df = pd.DataFrame()
        df['inter_arrival_time'] = pd.Series(inter_arrival_times)

        sns.distplot(inter_arrival_times)
        plt.show()

    def __filter_packets(self, packets, filters):
        filtered_packets = packets
        for filter in filters:
            filtered_packets = filter.filter(filtered_packets)

        return filtered_packets

    def __calculate_inter_arrival_time(self, packets):
        inter_arrival_times = []

        previous_timestamp_s = float(packets[0][1].sniff_timestamp)
        for packet in packets:
            packet_body = packet[1]
            packet_timestamp_s = float(packet_body.sniff_timestamp)
            inter_arrival_times.append((packet_timestamp_s - previous_timestamp_s) * 1000)
            previous_timestamp_s = packet_timestamp_s

        return inter_arrival_times
