# Lab 6 Solution: REST vs gRPC

All values are milliseconds per call. Local and same-zone runs used 1000 repetitions; different-region runs used 100 repetitions. All cross-host tests used internal IP addresses (e2-standard-2 VMs; same-zone = us-west1-a to us-west1-a, different region = us-west1-a client to europe-west3-a server).

| Method | Local | Same-Zone | Different Region |
|---|---|---|---|
| REST add | 3.00 | 3.86 | 336.92 |
| gRPC add | 0.83 | 2.32 | 163.31 |
| REST rawimg | 5.91 | 9.04 | 1336.10 |
| gRPC rawimg | 13.92 | 20.79 | 232.35 |
| REST dotproduct | 3.44 | 4.44 | 335.08 |
| gRPC dotproduct | 0.91 | 2.25 | 164.45 |
| REST jsonimg | 29.71 | 34.42 | 1505.27 |
| gRPC jsonimg | 30.00 | 39.50 | 236.98 |
| PING | 0.053 | 0.534 | 178.33 |

## Observations

For small payloads (add and dotproduct), gRPC was faster than REST in every setup: about 3.6x faster locally (0.83 ms vs 3.00 ms for add), about 1.7x faster in the same zone, and about 2x faster across regions (163 ms vs 337 ms). The cross-region gap is explained by connection handling: my REST client opens a new TCP connection for every request, which costs roughly two round trips (about 337 ms, close to 2 x 178 ms ping), while the gRPC client reuses one HTTP/2 channel and needs roughly one round trip.

For the large 1.6 MB image calls the result depends on distance. Locally and within a zone, REST rawimage was actually faster than gRPC rawimage (5.9 vs 13.9 ms and 9.0 vs 20.8 ms), probably because Python gRPC/protobuf has extra overhead handling a large bytes message, while Flask reads the raw body directly. Across regions gRPC was much faster (232 ms vs 1336 ms), because REST pays TCP connection setup and slow start for every 1.6 MB upload, while gRPC's long-lived connection is already warmed up.

jsonimage was the slowest operation in nearly every case. Base64 makes the payload about 33% larger and adds encoding and decoding work on both client and server, so it was about 5x slower than rawimage for REST locally (29.7 vs 5.9 ms) and about 2x slower for gRPC locally (30.0 vs 13.9 ms).

As distance grows, the network dominates. Locally, ping is only 0.05 ms, so the 1-3 ms for small calls is almost entirely Python and RPC overhead. Across regions every call is bounded below by the roughly 178 ms ping time, and the differences between REST and gRPC come mostly from how many round trips each needs. One oddity: gRPC add across regions (163 ms) came out slightly below the ping average (178 ms), which is likely because ICMP ping can be treated differently from TCP traffic, so ping is only an approximate baseline.
