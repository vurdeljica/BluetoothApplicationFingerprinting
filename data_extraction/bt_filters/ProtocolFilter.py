from Filter import Filter
from pyshark.packet.packet import Packet


class ProtocolFilter(Filter):
    def __init__(self, protocol : str):
        super().__init__()
        self.__protocol = protocol

    def _apply_filter(self, packet_summaries : list):
        self._filtered_list = []
        for packet in packet_summaries:
            packet_summary = packet[0]
            if packet_summary.protocol == self.__protocol:
                self._filtered_list.append(packet)
