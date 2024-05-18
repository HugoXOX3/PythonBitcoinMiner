# context.py for CPU-based Bitcoin Mining

# Flag to indicate if the mining process should be shut down
fShutdown = False

# List to keep track of the running state of threads (e.g., mining, listening)
listfThreadRunning = [False] * 2

# Current height of the local blockchain copy
local_height = 0

# Dictionary to store the best difficulty achieved for each height
nHeightDiff = {}

# Hash of the previous block (to detect new blocks in the network)
updatedPrevHash = None

# Mining-related parameters (updated with each new block or job)
job_id = None
prevhash = None
coinb1 = None
coinb2 = None
merkle_branch = None
version = None
nbits = None
ntime = None
clean_jobs = None
sub_details = None
extranonce1 = None
extranonce2_size = None

# Performance Metrics for CPU Mining
total_hashes_computed = 0  # Total number of hashes computed
hash_rate = 0              # Hash rate (hashes per second)
mining_time_per_block = [] # Time taken to mine each block
resource_utilization = {   # Resource utilization (CPU, memory)
    'cpu_usage': 0,
    'memory_usage': 0
}

# Network Statistics
network_difficulty = None  # Current network difficulty
average_block_time = None  # Average time for block discovery in the network

# Error Handling and Logging
error_count = 0            # Number of errors encountered
last_error_message = ""    # Last error message for debugging

# Adaptive Mining Configuration
adaptive_difficulty = True  # Flag to enable adaptive difficulty
reconnection_attempts = 0    # Number of attempts to reconnect to the pool

# Blockchain Data
last_block_hashes = []     # Store hashes of the last N blocks

# User Customization
user_preferences = {
    'logging_level': 'info',
    'ui_settings': {}
}
