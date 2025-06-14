import socket
import json
import hashlib
import struct
import time
import os

def get_input(prompt, data_type=str):
    while True:
        try:
            value = data_type(input(prompt))
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}.")

if os.path.isfile('config.json'):
    print("config.json found,start mining")
    with open('config.json','r') as file:
        config = json.load(file)
    pool_address = config['pool_address']
    pool_port = config["pool_port"]
    username = config["user_name"]
    password = config["password"]
    min_diff = config["min_diff"]
else:
    print("config.json doesn't exist,generating now")
    pool_address = get_input("Enter the pool address: ")
    pool_port = get_input("Enter the pool port: ", int)
    user_name = get_input("Enter the user name: ")
    password = get_input("Enter the password: ")
    min_diff = get_input("Enter the minimum difficulty: ", float)
    config_data = {
        "pool_address": pool_address,
        "pool_port": pool_port,
        "user_name": user_name,
        "password": password,
        "min_diff": min_diff
    }
    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Configuration data has been written to config.json")

def connect_to_pool(pool_address, pool_port, timeout=30, retries=5):
    for attempt in range(retries):
        try:
            print(f"Attempting to connect to pool (Attempt {attempt + 1}/{retries})...")
            sock = socket.create_connection((pool_address, pool_port), timeout)
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
    sock.sendall((json.dumps(message) + '\n').encode('utf-8'))

def receive_messages(sock, timeout=30):
    buffer = b''
    sock.settimeout(timeout)
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
            print(f"Authorize response: {response}")
            return response['result']

def calculate_difficulty(hash_result):
    hash_int = int.from_bytes(hash_result[::-1], byteorder='big')
    max_target = 0xffff * (2**208)
    difficulty = max_target / hash_int
    return difficulty

def mine(job, target, extranonce1, extranonce2_size):
    job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs = job

    extranonce2 = struct.pack('<Q', 0)[:extranonce2_size]
    coinbase = (coinb1 + extranonce1 + extranonce2.hex() + coinb2).encode('utf-8')
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(coinbase).digest()).digest()
    
    merkle_root = coinbase_hash_bin
    for branch in merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256((merkle_root + bytes.fromhex(branch))).digest()).digest()

    block_header = (version + prevhash + merkle_root[::-1].hex() + ntime + nbits).encode('utf-8')
    target_bin = bytes.fromhex(target)[::-1]

    for nonce in range(2**32):
        nonce_bin = struct.pack('<I', nonce)
        hash_result = hashlib.sha256(hashlib.sha256(block_header + nonce_bin).digest()).digest()

        if hash_result[::-1] < target_bin:
            difficulty = calculate_difficulty(hash_result)
            if difficulty > min_diff:
                print(f"Nonce found: {nonce}, Difficulty: {difficulty}")
                print(f"Hash: {hash_result[::-1].hex()}")
                return job_id, extranonce2, ntime, nonce

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
    if pool_address.startswith("stratum+tcp://"):
        pool_address = pool_address[len("stratum+tcp://"):]

    while True:
        try:
            sock = connect_to_pool(pool_address, pool_port)
            
            extranonce = subscribe(sock)
            extranonce1, extranonce2_size = extranonce[1], extranonce[2]
            authorize(sock, username, password)
            
            while True:
                for response in receive_messages(sock):
                    if response['method'] == 'mining.notify':
                        job = response['params']
                        result = mine(job, job[6], extranonce1, extranonce2_size)
                        if result:
                            submit_solution(sock, *result)
        except Exception as e:
            print(f"An error occurred: {e}. Reconnecting...")
            time.sleep(5)
