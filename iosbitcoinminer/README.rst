===============================
How to Build an iOS Mining App
===============================

This guide will walk you through the steps to build an iOS mining app using SwiftUI and Python. The app allows users to configure mining settings and execute a mining script.

Prerequisites
=============

- Xcode installed on your macOS system. 

Setting Up the Project
======================

1. **Open Xcode** and create a new project:
   - Choose "App" under the iOS tab and click "Next."
   - Enter the project name, organization name, and identifier.
   - Choose the interface and lifecycle as "SwiftUI" and "SwiftUI App" respectively.
   - Click "Next" and choose a location to save the project.

Adding Pyto Dependency
======================

To run Python scripts within the iOS app, we will use the Pyto library.

1. **Using CocoaPods**:
   - Create a `Podfile` in your project directory with the following content:

     .. code-block:: ruby

        platform :ios, '14.0'
        use_frameworks!

        target 'YourProjectName' do
          pod 'Pyto'
        end

   - Run `pod install` in the terminal to install the dependency.
   - Open the generated `.xcworkspace` file to continue working on your project.


Creating the SwiftUI Interface
==============================

You can also copy from the 2 file in iosbitcoinminer dir

### ContentView.swift

This file contains the main view of the app.

.. code-block:: swift

    import SwiftUI
    import Pyto

    struct ContentView: View {
        @State private var output: String = ""
        @State private var showSettings = false

        var body: some View {
            VStack {
                Text("iOS Mining App")
                    .font(.largeTitle)
                    .padding()

                Button(action: {
                    runPythonScript()
                }) {
                    Text("Start Mining")
                        .font(.title)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }

                Button(action: {
                    showSettings.toggle()
                }) {
                    Text("Settings")
                        .font(.title)
                        .padding()
                        .background(Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .sheet(isPresented: $showSettings) {
                    SettingsView()
                }

                ScrollView {
                    Text(output)
                        .padding()
                }
            }
            .padding()
        }

        func runPythonScript() {
            let fileManager = FileManager.default
            guard let documentDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first else {
                return
            }
            let configFilePath = documentDirectory.appendingPathComponent("config.json").path

            let script = """
            import socket
            import json
            import hashlib
            import struct
            import time
            import multiprocessing
            import os

            config_file_path = '\(configFilePath)'
            
            with open(config_file_path, 'r') as file:
                config = json.load(file)
            
            pool_address = config['pool_address']
            pool_port = config["pool_port"]
            username = config["user_name"]
            password = config["password"]
            min_diff = config["min_diff"]

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
                sock.sendall((json.dumps(message) + '\\n').encode('utf-8'))

            def receive_messages(sock, timeout=30):
                buffer = b''
                sock.settimeout(timeout)
                while True:
                    try:
                        chunk = sock.recv(1024)
                        if not chunk:
                            break
                        buffer += chunk
                        while b'\\n' in buffer:
                            line, buffer = buffer.split(b'\\n', 1)
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

            def mine_worker(job, target, extranonce1, extranonce2_size, nonce_start, nonce_end, result_queue, stop_event):
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
                        difficulty = calculate_difficulty(hash_result)
                        if difficulty > min_diff:
                            print(f"Nonce found: {nonce}, Difficulty: {difficulty}")
                            print(f"Hash: {hash_result[::-1].hex()}")
                            result_queue.put((job_id, extranonce2, ntime, nonce))
                            stop_event.set()
                            return

            def mine(sock, job, target, extranonce1, extranonce2_size):
                num_processes = multiprocessing.cpu_count()
                nonce_range = 2**32 // num_processes
                result_queue = multiprocessing.Queue()
                stop_event = multiprocessing.Event()

                while not stop_event.is_set():
                    processes = []
                    for i in range(num_processes):
                        nonce_start = i * nonce_range
                        nonce_end = (i + 1) * nonce_range
                        p = multiprocessing.Process(target=mine_worker, args=(job, target, extranonce1, extranonce2_size, nonce_start, nonce_end, result_queue, stop_event))
                        processes.append(p)
                        p.start()

                    for p in processes:
                        p.join()

                    if not result_queue.empty():
                        return result_queue.get()

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
                                    result = mine(sock, job, job[6], extranonce1, extranonce2_size)
                                    if result:
                                        submit_solution(sock, *result)
                    except Exception as e:
                        print(f"An error occurred: {e}. Reconnecting...")
                        time.sleep(5)
            """

            let output = PyOutputHelper()
            output.textView = UITextView() // Add a UITextView to display output
            PyOutputHelper.output = output
            
            Python.shared.run(code: script)
        }
    }

    struct ContentView_Previews: PreviewProvider {
        static var previews: some View {
            ContentView()
        }
    }

### SettingsView.swift

This file contains the settings view where users can input their mining configuration.

.. code-block:: swift

    import SwiftUI

    struct SettingsView: View {
        @AppStorage("poolAddress") var poolAddress: String = ""
        @AppStorage("poolPort") var poolPort: String = ""
        @AppStorage("username") var username: String = ""
        @AppStorage("password") var password: String = ""
        @AppStorage("minDiff") var minDiff: String = ""

        var body: some View {
            NavigationView {
                Form {
                    Section(header: Text("Pool Settings")) {
                        TextField("Pool Address", text: $poolAddress)
                        TextField("Pool Port", text: $poolPort)
                            .keyboardType(.numberPad)
                    }

                    Section(header: Text("User Settings")) {
                        TextField("Username", text: $username)
                        SecureField("Password", text: $password)
                    }

                    Section(header: Text("Mining Settings")) {
                        TextField("Minimum Difficulty", text: $minDiff)
                            .keyboardType(.decimalPad)
                    }
                }
                .navigationBarTitle("Settings")
                .navigationBarItems(trailing: Button("Save") {
                    saveSettings()
                })
            }
        }

        func saveSettings() {
            let configData = [
                "pool_address": poolAddress,
                "pool_port": Int(poolPort) ?? 0,
                "user_name": username,
                "password": password,
                "min_diff": Double(minDiff) ?? 0.0
            ] as [String : Any]

            if let jsonData = try? JSONSerialization.data(withJSONObject: configData, options: .prettyPrinted) {
                let jsonString = String(data: jsonData, encoding: .utf8)
                let fileManager = FileManager.default
                if let documentDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first {
                    let filePath = documentDirectory.appendingPathComponent("config.json")
                    try? jsonString?.write(to: filePath, atomically: true, encoding: .utf8)
                }
            }
        }
    }

    struct SettingsView_Previews: PreviewProvider {
        static var previews: some View {
            SettingsView()
        }
    }

Building and Running the App
============================

1. **Connect your iOS device** or use a simulator.
2. Click the "Run" button in Xcode to build and run the app.

With these steps, you have successfully built an iOS mining app that allows users to configure mining settings and execute a mining script.
