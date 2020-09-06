from Filter import Filter


class DeviceFilter(Filter):
    def __init__(self, device : str):
        super().__init__()
        self.__device = device

    def _apply_filter(self, packet_summaries : list):
        self._filtered_list = []
        for packet in packet_summaries:
            packet_summary = packet[0]
            if packet_summary.source != self.__device and packet_summary.destination != self.__device:
                self._filtered_list.append(packet)
