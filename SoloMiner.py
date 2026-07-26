import base64
import hashlib
import http.client
import json
import os
import select
import socket
import struct
import sys
import time
import errno

MAX_TARGET = 0xFFFF * 2**208
LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_COLORS = {
    "INFO": "\u001b[38;5;81m",
    "SUCCESS": "\u001b[38;5;120m",
    "WARNING": "\u001b[38;5;214m",
    "ERROR": "\u001b[38;5;196m",
    "DEBUG": "\u001b[38;5;141m",
    "RESET": "\u001b[0m",
}

CURRENT_STATUS = None
STATUS_WIDTH = 120


def enable_ansi():
    if os.name == "nt":
        try:
            os.system("")
        except Exception:
            pass


def format_log(level, message):
    timestamp = time.strftime(LOG_TIMESTAMP_FORMAT)
    color = LOG_COLORS.get(level, "")
    reset = LOG_COLORS["RESET"]
    return f"{color}[{timestamp}] [{level}] {message}{reset}"


def clear_status_line():
    global CURRENT_STATUS
    if CURRENT_STATUS is not None:
        sys.stdout.write("\r" + " " * STATUS_WIDTH + "\r")
        sys.stdout.flush()


def restore_status_line():
    if CURRENT_STATUS is not None:
        sys.stdout.write("\r" + CURRENT_STATUS.ljust(STATUS_WIDTH))
        sys.stdout.flush()


def log_info(message):
    clear_status_line()
    print(format_log("INFO", message))
    restore_status_line()


def log_success(message):
    clear_status_line()
    print(format_log("SUCCESS", message))
    restore_status_line()


def log_warning(message):
    clear_status_line()
    print(format_log("WARNING", message))
    restore_status_line()


def log_error(message):
    clear_status_line()
    print(format_log("ERROR", message))
    restore_status_line()


def log_debug(message):
    clear_status_line()
    print(format_log("DEBUG", message))
    restore_status_line()


def print_status(message):
    global CURRENT_STATUS
    CURRENT_STATUS = f"[STATUS] {message}"
    sys.stdout.write("\r" + CURRENT_STATUS.ljust(STATUS_WIDTH))
    sys.stdout.flush()


def format_eta(difficulty, hash_rate):
    if hash_rate <= 0 or difficulty <= 0:
        return "?"
    expected_hashes = difficulty * 2**32
    seconds = expected_hashes / hash_rate
    if seconds < 60:
        return f"{seconds:.1f}s"
    if seconds < 3600:
        return f"{seconds/60:.1f}m"
    if seconds < 86400:
        return f"{seconds/3600:.1f}h"
    return f"{seconds/86400:.1f}d"


def get_input(prompt, data_type=str, default=None):
    while True:
        value = input(prompt)
        if value == "" and default is not None:
            return default
        try:
            return data_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}.")


def load_config():
    if os.path.isfile("config.json"):
        with open("config.json", "r") as file:
            config = json.load(file)
        log_info("Loaded config.json")
        return config

    log_warning("config.json not found. Creating new configuration.")
    connection_type = get_input("Enter connection type (stratum/rpc): ").lower()

    if connection_type == "rpc":
        rpc_host = get_input("Bitcoin RPC host (default 127.0.0.1): ", str, "127.0.0.1")
        rpc_user = get_input("Bitcoin RPC username: ")
        rpc_password = get_input("Bitcoin RPC password: ")
        rpc_port = get_input("Bitcoin RPC port (default 8332): ", int, 8332)
        min_diff = get_input("Minimum difficulty (default 1.0): ", float, 1.0)
        config = {
            "connection_type": connection_type,
            "rpc_host": rpc_host,
            "rpc_user": rpc_user,
            "rpc_password": rpc_password,
            "rpc_port": rpc_port,
            "min_diff": min_diff,
        }
    else:
        pool_address = get_input("Pool address: ")
        pool_port = get_input("Pool port: ", int)
        username = get_input("Miner username: ")
        password = get_input("Miner password: ")
        min_diff = get_input("Minimum difficulty (default 1.0): ", float, 1.0)
        config = {
            "connection_type": connection_type,
            "pool_address": pool_address,
            "pool_port": pool_port,
            "user_name": username,
            "password": password,
            "min_diff": min_diff,
        }

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    log_success("Configuration saved to config.json")
    return config


def connect_to_pool(host, port, timeout=30):
    log_info(f"Connecting to pool {host}:{port}")
    return socket.create_connection((host, port), timeout)


def connect_to_bitcoin_rpc(rpc_user, rpc_password, rpc_host="127.0.0.1", rpc_port=8332, timeout=30):
    auth = base64.b64encode(f"{rpc_user}:{rpc_password}".encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    }
    conn = http.client.HTTPConnection(rpc_host, rpc_port, timeout=timeout)
    return conn, headers


def send_rpc_request(conn, headers, method, params=None):
    if params is None:
        params = []
    payload = {
        "jsonrpc": "1.0",
        "id": "python_miner",
        "method": method,
        "params": params,
    }
    conn.request("POST", "/", json.dumps(payload), headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    return json.loads(data)


def nbits_to_target(nbits_hex):
    nbits = int(nbits_hex, 16)
    exponent = nbits >> 24
    coefficient = nbits & 0xFFFFFF
    if exponent <= 3:
        return coefficient >> (8 * (3 - exponent))
    return coefficient << (8 * (exponent - 3))


def difficulty_to_target(difficulty):
    if difficulty <= 0:
        return 0
    target = int(MAX_TARGET / difficulty)
    return min(target, MAX_TARGET)


def target_to_difficulty(target):
    if target == 0:
        return float("inf")
    return MAX_TARGET / target


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def parse_notify(params):
    if len(params) < 9:
        raise ValueError("Unexpected mining.notify format")

    job_id = params[0]
    prevhash = params[1]
    coinb1 = params[2]
    coinb2 = params[3]
    merkle_branch = params[4] if isinstance(params[4], list) else []
    version = params[5]
    nbits = params[6]
    ntime = params[7]
    clean_jobs = params[8]

    return {
        "job_id": job_id,
        "prevhash": prevhash,
        "coinb1": coinb1,
        "coinb2": coinb2,
        "merkle_branch": merkle_branch,
        "version": version,
        "nbits": nbits,
        "ntime": ntime,
        "clean_jobs": clean_jobs,
    }


def build_coinbase(coinb1, extranonce1, extranonce2, coinb2):
    return bytes.fromhex(coinb1) + bytes.fromhex(extranonce1) + extranonce2 + bytes.fromhex(coinb2)


def build_merkle_root(coinbase_hash, merkle_branch):
    merkle = coinbase_hash
    for branch in merkle_branch:
        merkle = double_sha256(merkle + bytes.fromhex(branch))
    return merkle


def header_prefix(job, extranonce1, extranonce2):
    version = bytes.fromhex(job["version"])
    prevhash = bytes.fromhex(job["prevhash"])[::-1]
    ntime = bytes.fromhex(job["ntime"])
    nbits = bytes.fromhex(job["nbits"])
    coinbase = build_coinbase(job["coinb1"], extranonce1, extranonce2, job["coinb2"])
    merkle_root = build_merkle_root(double_sha256(coinbase), job["merkle_branch"])
    return version + prevhash + merkle_root[::-1] + ntime + nbits


def hash_to_int(hash_bytes):
    return int.from_bytes(hash_bytes, byteorder="big")


class StratumClient:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b""

    def send(self, message):
        payload = json.dumps(message) + "\n"
        self.sock.sendall(payload.encode("utf-8"))

    def receive(self, timeout=0.1):
        self.sock.settimeout(timeout)
        try:
            chunk = self.sock.recv(4096)
        except socket.timeout:
            return []
        except OSError as e:
            if e.errno in (errno.EWOULDBLOCK, errno.EAGAIN, 10035):
                return []
            raise

        if not chunk:
            raise ConnectionResetError("Socket closed by server")

        self.buffer += chunk
        messages = []
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            text = line.strip()
            if not text:
                continue
            messages.append(json.loads(text.decode("utf-8")))
        return messages

    def receive_until(self, predicate, timeout=10.0):
        start = time.time()
        while time.time() - start < timeout:
            messages = self.receive(timeout=1.0)
            for message in messages:
                if predicate(message):
                    return message
        raise TimeoutError("Timed out waiting for expected Stratum response")


def subscribe(client):
    client.send({"id": 1, "method": "mining.subscribe", "params": []})
    response = client.receive_until(lambda msg: msg.get("id") == 1)
    if response.get("error"):
        error_text = json.dumps(response["error"])
        log_error(f"Subscription error: {error_text}")
        raise RuntimeError(f"Subscription error: {response['error']}")
    log_success("Subscription accepted")
    return response["result"]


def authorize(client, username, password):
    client.send({"id": 2, "method": "mining.authorize", "params": [username, password]})
    response = client.receive_until(lambda msg: msg.get("id") == 2)
    if response.get("error"):
        error_text = json.dumps(response["error"])
        log_error(f"Authorization error: {error_text}")
        raise RuntimeError(f"Authorization error: {response['error']}")
    log_success("Authorization accepted")
    return response["result"]


def submit_share(client, username, job_id, extranonce2, ntime, nonce):
    params = [username, job_id, extranonce2.hex(), ntime, struct.pack("<I", nonce).hex()]
    client.send({"id": 4, "method": "mining.submit", "params": params})
    response = client.receive_until(lambda msg: msg.get("id") == 4)
    return response


def mine_job(client, job, extranonce1, extranonce2_size, share_diff, min_diff):
    difficulty = max(share_diff, min_diff)
    target = difficulty_to_target(difficulty)
    extranonce1_bytes = bytes.fromhex(extranonce1)
    job_header_data = None

    for extranonce2_counter in range(1 << (8 * extranonce2_size)):
        extranonce2 = struct.pack("<Q", extranonce2_counter)[:extranonce2_size]
        prefix = header_prefix(job, extranonce1, extranonce2)

        nonce = 0
        hashes = 0
        report_time = time.time()
        while nonce < 0x100000000:
            if nonce % 4096 == 0:
                try:
                    messages = client.receive(timeout=0)
                except ConnectionResetError:
                    raise
                except OSError as e:
                    if e.errno in (errno.EWOULDBLOCK, errno.EAGAIN, 10035):
                        messages = []
                    else:
                        raise
                for message in messages:
                    if message.get("method") == "mining.set_difficulty":
                        return ("update_difficulty", float(message["params"][0]), message)
                    if message.get("method") == "mining.notify":
                        log_info("Received new job notification")
                        return ("new_job", parse_notify(message["params"]), message)

            header = prefix + struct.pack("<I", nonce)
            result = double_sha256(header)
            hash_int = int.from_bytes(result, "big")
            hashes += 1

            now = time.time()
            if now - report_time >= 1.0:
                print_status(f"Hashrate: {hashes / (now - report_time):,.0f} H/s | Target: {hex(target)}")
                hashes = 0
                report_time = now

            if hash_int <= target:
                log_success(f"Valid share found for job {job['job_id']} nonce={nonce} target={hex(target)}")
                return ("share", job["job_id"], extranonce2, job["ntime"], nonce, result)

            nonce += 1

    return None


def run_stratum(config):
    while True:
        try:
            pool_address = config["pool_address"]
            pool_port = config["pool_port"]
            if pool_address.startswith("stratum+tcp://"):
                pool_address = pool_address.split("stratum+tcp://", 1)[1]

            sock = connect_to_pool(pool_address, pool_port)
            client = StratumClient(sock)
            extra = subscribe(client)
            extranonce1 = extra[1]
            extranonce2_size = extra[2]
            authorize(client, config["user_name"], config["password"])

            print(f"Subscribed. extranonce1={extranonce1}, size={extranonce2_size}")
            current_job = None
            pool_diff = 1.0

            while True:
                if current_job is None:
                    messages = client.receive(timeout=1.0)
                    for message in messages:
                        if message.get("method") == "mining.notify":
                            current_job = parse_notify(message["params"])
                            log_info(f"New job received: {current_job['job_id']}")
                        elif message.get("method") == "mining.set_difficulty":
                            pool_diff = float(message["params"][0])
                            log_info(f"Pool difficulty updated: {pool_diff}")
                    continue

                outcome = mine_job(client, current_job, extranonce1, extranonce2_size, pool_diff, config.get("min_diff", 1.0))
                if outcome is None:
                    continue

                if outcome[0] == "new_job":
                    current_job = outcome[1]
                    log_info(f"Job updated during mining: {current_job['job_id']}")
                    continue

                if outcome[0] == "update_difficulty":
                    pool_diff = outcome[1]
                    log_info(f"Pool difficulty updated during mining: {pool_diff}")
                    continue

                if outcome[0] == "share":
                    _, job_id, extranonce2, ntime, nonce, result = outcome
                    log_success(f"Found share for job {job_id} nonce={nonce}")
                    submission = submit_share(client, config["user_name"], job_id, extranonce2, ntime, nonce)
                    log_info(f"Submission result: {submission}")

        except (socket.error, ConnectionResetError, RuntimeError, TimeoutError) as exc:
            log_warning(f"Connection lost or error occurred: {exc}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            log_warning("Interrupted by user. Exiting.")
            sys.exit(0)


def mine_with_rpc(config):
    log_warning("RPC mining is not supported by this script in production mode.")
    log_info("Use a dedicated Bitcoin mining client or implement a local block template miner.")


def main():
    enable_ansi()
    config = load_config()
    connection_type = config.get("connection_type", "stratum").lower()

    if connection_type == "stratum":
        run_stratum(config)
    elif connection_type == "rpc":
        mine_with_rpc(config)
    else:
        print(f"Unknown connection type: {connection_type}")


if __name__ == "__main__":
    main()
