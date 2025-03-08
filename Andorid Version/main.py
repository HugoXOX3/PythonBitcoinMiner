import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import socket
import json
import hashlib
import struct
import time
import multiprocessing
import os

class MiningApp(toga.App):

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create input fields
        self.pool_address_input = toga.TextInput(placeholder='Pool Address')
        self.pool_port_input = toga.TextInput(placeholder='Pool Port')
        self.username_input = toga.TextInput(placeholder='Username')
        self.password_input = toga.PasswordInput(placeholder='Password')
        self.min_diff_input = toga.TextInput(placeholder='Minimum Difficulty(Recommend >0.01)')
        
        # Create button
        self.start_button = toga.Button('Start Mining', on_press=self.start_mining)
        
        # Create status label
        self.status_label = toga.Label('')

        # Layout
        box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        box.add(self.pool_address_input)
        box.add(self.pool_port_input)
        box.add(self.username_input)
        box.add(self.password_input)
        box.add(self.min_diff_input)
        box.add(self.start_button)
        box.add(self.status_label)
        
        self.main_window.content = box
        self.main_window.show()

    def start_mining(self, widget):
        pool_address = self.pool_address_input.value
        pool_port = int(self.pool_port_input.value)
        username = self.username_input.value
        password = self.password_input.value
        min_diff = float(self.min_diff_input.value)
        
        self.status_label.text = "Starting mining process..."
        
        # Here you would integrate the mining logic from the provided Python code
        self.mine(pool_address, pool_port, username, password, min_diff)

    def get_input(self, prompt, data_type=str):
        while True:
            try:
                value = data_type(input(prompt))
                return value
            except ValueError:
                print(f"Invalid input. Please enter a valid {data_type.__name__}.")

    def load_config(self):
        if os.path.isfile('config.json'):
            print("config.json found, start mining")
            with open('config.json','r') as file:
                config = json.load(file)
            return config
        else:
            print("config.json doesn't exist, generating now")
            config = {
                "pool_address": self.get_input("Enter the pool address: "),
                "pool_port": self.get_input("Enter the pool port: ", int),
                "user_name": self.get_input("Enter the user name: "),
                "password": self.get_input("Enter the password: "),
                "min_diff": self.get_input("Enter the minimum difficulty: ", float)
            }
            with open("config.json", "w") as config_file:
                json.dump(config, config_file, indent=4)
            print("Configuration data has been written to config.json")
            return config

    def connect_to_pool(self, pool_address, pool_port, timeout=30, retries=5):
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

    def send_message(self, sock, message):
        print(f"Sending message: {message}")
        sock.sendall((json.dumps(message) + '\n').encode('utf-8'))

    def receive_messages(self, sock, timeout=30):
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

    def subscribe(self, sock):
        message = {
            "id": 1,
            "method": "mining.subscribe",
            "params": []
        }
        self.send_message(sock, message)
        for response in self.receive_messages(sock):
            if response['id'] == 1:
                print(f"Subscribe response: {response}")
                return response['result']

    def authorize(self, sock, username, password):
        message = {
            "id": 2,
            "method": "mining.authorize",
            "params": [username, password]
        }
        self.send_message(sock, message)
        for response in self.receive_messages(sock):
            if response['id'] == 2:
                print(f"Authorize response: {response}")
                return response['result']

    def calculate_difficulty(self, hash_result):
        hash_int = int.from_bytes(hash_result[::-1], byteorder='big')
        max_target = 0xffff * (2**208)
        difficulty = max_target / hash_int
        return difficulty

    def mine_worker(self, job, target, extranonce1, extranonce2_size, nonce_start, nonce_end, result_queue, stop_event):
        job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs = job

        extranonce2 = struct.pack('<Q', 0)[:extranonce2_size]
        coinbase = (coinb1 + extranonce1 + extranonce2.hex() + coinb2).encode('utf-8')
        coinbase_hash_bin = hashlib.sha256(hashlib.sha256(coinbase).digest()).digest()
        
        merkle_root = coinbase_hash_bin
        for branch in merkle_branch:
            merkle_root = hashlib.sha256(hashlib.sha256((merkle_root + bytes.fromhex(branch))).digest()).digest()

        block_header = (version + prevhash + merkle_root[::-1].hex() + ntime + nbits).encode('utf-8')
        target_bin = bytes.fromhex(target)[::-1]

        for nonce in range(nonce_start, nonce_end):
            if stop_event.is_set():
                return
            
            nonce_bin = struct.pack('<I', nonce)
            hash_result = hashlib.sha256(hashlib.sha256(hashlib.sha256(hashlib.sha256(block_header + nonce_bin).digest()).digest()).digest()).digest()

            if hash_result[::-1] < target_bin:
                difficulty = self.calculate_difficulty(hash_result)
                if difficulty > min_diff:
                    print(f"Nonce found: {nonce}, Difficulty: {difficulty}")
                    print(f"Hash: {hash_result[::-1].hex()}")
                    result_queue.put((job_id, extranonce2, ntime, nonce))
                    stop_event.set()
                    return

    def mine(self, sock, job, target, extranonce1, extranonce2_size):
        num_processes = multiprocessing.cpu_count()
        nonce_range = 2**32 // num_processes
        result_queue = multiprocessing.Queue()
        stop_event = multiprocessing.Event()

        while not stop_event.is_set():
            processes = []
            for i in range(num_processes):
                nonce_start = i * nonce_range
                nonce_end = (i + 1) * nonce_range
                p = multiprocessing.Process(target=self.mine_worker, args=(job, target, extranonce1, extranonce2_size, nonce_start, nonce_end, result_queue, stop_event))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

            if not result_queue.empty():
                return result_queue.get()

    def submit_solution(self, sock, job_id, extranonce2, ntime, nonce):
        message = {
            "id": 4,
            "method": "mining.submit",
            "params": [username, job_id, extranonce2.hex(), ntime, struct.pack('<I', nonce).hex()]
        }
        self.send_message(sock, message)
        for response in self.receive_messages(sock):
            if response['id'] == 4:
                print("Submission response:", response)
                if response['result'] == False and response['error']['code'] == 23:
                    print(f"Low difficulty share: {response['error']['message']}")
                    return

def main():
    return MiningApp()

if __name__ == '__main__':
    main().main_loop()