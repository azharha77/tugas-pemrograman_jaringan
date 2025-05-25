import os
import time
import logging
import random
import concurrent.futures
from file_client_cli import remote_upload, remote_get

FILES = ["10MB_File.pdf", "50MB_File.pdf", "100MB_File.pdf"]
OPERATIONS = ["DOWNLOAD", "UPLOAD"]

def test_operation(op, filename):
    start_time = time.time()
    success = False
    try:
        print(f"[DEBUG] Starting {op} on {filename}", flush=True)
        if op == "UPLOAD":
            success = remote_upload(filename)
        elif op == "DOWNLOAD":
            success = remote_get(filename)
        else:
            raise ValueError("Unknown operation")
        print(f"[DEBUG] Finished {op} on {filename}: {'Success' if success else 'Fail'}", flush=True)
    except Exception as e:
        logging.warning(f"Operation {op} failed: {e}")
    elapsed = time.time() - start_time
    file_size = os.path.getsize(filename)
    throughput = file_size / elapsed if elapsed > 0 else 0
    return success, elapsed, throughput

def run_stress_test(op, filename, client_pool_size, server_pool_size):
    print(f"[TEST] Server: {server_pool_size}, Clients: {client_pool_size}, Op: {op}, File: {filename}")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=client_pool_size) as executor:
        futures = [executor.submit(test_operation, op, filename) for _ in range(client_pool_size)]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())

    total_time = sum(r[1] for r in results)
    total_throughput = sum(r[2] for r in results)
    success_count = sum(1 for r in results if r[0])
    failed_count = client_pool_size - success_count

    avg_time = total_time / client_pool_size
    avg_throughput = total_throughput / client_pool_size

    print(f"Success: {success_count}, Failed: {failed_count}")
    print(f"Avg Time per Client: {avg_time:.2f} seconds")
    print(f"Avg Throughput per Client: {avg_throughput:.2f} bytes/second\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    server_pool_options = [1, 5, 50]
    client_pool_options = [1, 5, 50]
    for op in OPERATIONS:
        for filename in FILES:
            for server_pool in server_pool_options:
                for client_pool in client_pool_options:
                    run_stress_test(op, filename, client_pool, server_pool)
