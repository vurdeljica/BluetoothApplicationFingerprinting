from Filter import Filter


class PacketSizeFilter(Filter):
    def __init__(self, packet_size : str):
        super().__init__()
        self.__packet_size = int(packet_size)

    def _apply_filter(self, packet_summaries : list):
        self._filtered_list = []
        for packet in packet_summaries:
            packet_summary = packet[0]
            if int(packet_summary.length) >= self.__packet_size:
                self._filtered_list.append(packet)
