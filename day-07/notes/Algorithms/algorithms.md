# Step 1: The Input (Our "stack of cards")
network_events = [
    {"src_ip": "192.168.1.10", "protocol": "TCP"},
    {"src_ip": "10.0.0.5", "protocol": "UDP"},
    {"src_ip": "172.16.0.4", "protocol": "TCP"},
    {"src_ip": "192.168.1.50", "protocol": "ICMP"}
]

# Step 2: Initialize our counter notepad to zero
tcp_count = 0

# Step 3 & 4: Loop through each event and check if protocol is TCP
for event in network_events:
    if event["protocol"] == "TCP":
        tcp_count += 1  # Add 1 to the counter

# Step 5: Output the final result
print("Total TCP network events observed:", tcp_count)