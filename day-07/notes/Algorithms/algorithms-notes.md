# Day 7 - Algorithm Foundations & Problem-Solving Logic

## 1. What is an Algorithm?
An algorithm is a finite, ordered sequence of precise logical steps designed to solve a computational problem. Writing out an algorithm in plain English before touching code ensures our logic is sound and error-free.

## 2. Practical Exercise: Counting TCP Protocol Events

### Plain-English Algorithm (Step-by-Step Logic):
1. **Define the Input:** Obtain a dataset containing network connection events and their associated protocol fields.
2. **Initialize Counter:** Create a tracking variable named `tcp_count` and set its value to `0`.
3. **Iterate Through Records:** Examine each event record in the dataset one by one from start to finish.
4. **Evaluate Condition:** Check whether the protocol value of the current event is strictly equal to `"TCP"`.
5. **Increment Counter:** If the condition evaluates to `True`, increase `tcp_count` by `1`. If `False`, skip to the next record.
6. **Output Final Result:** After all records have been examined, display the final count of TCP events to the user.

### Corresponding Python Code Implementation:
```python
network_events = [
    {"src_ip": "192.168.1.10", "protocol": "TCP"},
    {"src_ip": "10.0.0.5", "protocol": "UDP"},
    {"src_ip": "172.16.0.4", "protocol": "TCP"},
    {"src_ip": "192.168.1.50", "protocol": "ICMP"}
]

tcp_count = 0

for event in network_events:
    if event["protocol"] == "TCP":
        tcp_count += 1

print("Total TCP network events observed:", tcp_count)
