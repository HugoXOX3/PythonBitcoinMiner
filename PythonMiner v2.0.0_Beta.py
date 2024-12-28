import socket
import json
import hashlib
import struct
import time

def sha256d(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def connect_to_pool(pool_address, pool_port, timeout=30, retries=5):
    for attempt in range(retries):
        try:
            print(f"Attempting to connect to pool (Attempt {attempt + 1}/{retries})...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((pool_address, pool_port))
            print("Connected to pool!")
            return sock
        except socket.gaierror as e:
            print(f"Address-related error connecting to server: {e}")
        except socket.timeout as e:
            print(f"Connection timed out: {e}")
        except socket.error as e:
            print(f"Socket error: {e}")

        print(f"Retrying in 5 seconds...")
        time.sleep(5)
    
    raise Exception("Failed to connect to the pool after multiple attempts")

def send_message(sock, message):
    print(f"Sending message: {message}")
    sock.sendall(json.dumps(message).encode('utf-8') + b'\n')

def receive_messages(sock, timeout=30):
    buffer = b''
    sock.settimeout(timeout)  # Set the timeout for receive operation
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                break
            buffer += chunk
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                print(f"Received message: {line.decode('utf-8')}")
                yield json.loads(line.decode('utf-8'))
        except socket.timeout:
            print("Receive operation timed out. Retrying...")
            continue

def subscribe(sock):
    message = {
        "id": 1,
        "method": "mining.subscribe",
        "params": []
    }
    send_message(sock, message)
    for response in receive_messages(sock):
        if response['id'] == 1:
            print(f"Subscribe response: {response}")
            return response['result']

def authorize(sock, username, password):
    message = {
        "id": 2,
        "method": "mining.authorize",
        "params": [username, password]
    }
    send_message(sock, message)
    for response in receive_messages(sock):
        if response['id'] == 2:
            return response['result']

def mine(sock, job, target, extranonce1, extranonce2_size):
    job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs = job

    # Ensure extranonce2_size is an integer
    extranonce2_size = int(extranonce2_size)
    extranonce2 = struct.pack('<Q', 0)[:extranonce2_size]
    
    coinbase = (coinb1 + extranonce1 + extranonce2.hex() + coinb2).encode('utf-8')
    coinbase_hash_bin = sha256d(coinbase)
    
    merkle_root = coinbase_hash_bin
    for branch in merkle_branch:
        merkle_root = sha256d(merkle_root + bytes.fromhex(branch))

    block_header = (version + prevhash + merkle_root[::-1].hex() + ntime + nbits).encode('utf-8')

    nonce = 0
    max_nonce = 2**32
    target_bin = bytes.fromhex(target)[::-1]

    while nonce < max_nonce:
        nonce_bin = struct.pack('<I', nonce)
        hash_result = sha256d(sha256d(block_header + nonce_bin))

        if hash_result[::-1] < target_bin:
            print(f"Nonce found: {nonce}")
            print(f"Hash: {hash_result[::-1].hex()}")
            submit_solution(sock, job_id, extranonce2, ntime, nonce)
            return

        nonce += 1

def submit_solution(sock, job_id, extranonce2, ntime, nonce):
    message = {
        "id": 4,
        "method": "mining.submit",
        "params": [username, job_id, extranonce2.hex(), ntime, struct.pack('<I', nonce).hex()]
    }
    send_message(sock, message)
    for response in receive_messages(sock):
        if response['id'] == 4:
            print("Submission response:", response)
            if response['result'] == False and response['error']['code'] == 23:
                print(f"Low difficulty share: {response['error']['message']}")
                return

if __name__ == "__main__":
    pool_address = "public-pool.io"
    pool_port = 21496
    username = "bc1qp84qrxsntmpyekp9vzdenlt8khnj0h4wqafeqe"
    password = "x"

    # Ensure the pool address does not include protocol prefix
    if pool_address.startswith("stratum+tcp://"):
        pool_address = pool_address[len("stratum+tcp://"):]

    while True:
        try:
            sock = connect_to_pool(pool_address, pool_port)
            
            extranonce = subscribe(sock)
            extranonce1, extranonce2_size = extranonce[1], extranonce[2]  # Adjust indices based on the actual response structure
            authorize(sock, username, password)
            
            while True:
                for response in receive_messages(sock):
                    if response['method'] == 'mining.notify':
                        job = response['params']
                        mine(sock, job, job[6], extranonce1, extranonce2_size)
        except Exception as e:
            print(f"An error occurred: {e}. Reconnecting...")
            time.sleep(5)
