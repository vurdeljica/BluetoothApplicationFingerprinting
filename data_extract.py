from btsnoop.btsnoop import *

btsnp = btsnoop('btsnoop.log')
packets = btsnp.parsed
for packet in packets:
    hci_event = packet[0]
    data = packet[1]
    #print(hci_event.btsnp_timestamp_us)
    #print(type(packet[0]))
    #print(type(packet[1]))
    #print(packet)

remote_info = btsnp.get_remote_info()
print(remote_info)