address = 'bc1qwp44lvxgrhh42de507kezjspcyh8cvw6tvuykp'
pool = "solo.ckpool.org"
port = 3333
import requests,socket,threading,json,hashlib,binascii,random,time,traceback
import context as ctx
from signal import SIGINT, signal
sock = None
best_difficulty = 0
difficulty = 16
best_share_difficulty = float('inf')
best_share_hash = None
difficulty = 16
def handler(signal_received, frame):
    ctx.fShutdown = True
def get_current_block_height():
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])
def check_for_shutdown(t):
    n = t.n
    if ctx.fShutdown:
        if n != -1:
            ctx.listfThreadRunning[n] = False
            t.exit = True
class ExitedThread(threading.Thread):
    def __init__(self, arg, n):
        super(ExitedThread, self).__init__()
        self.exit = False
        self.arg = arg
        self.n = n
    def run(self):
        self.thread_handler(self.arg, self.n)
    def thread_handler(self, arg, n):
        while True:
            check_for_shutdown(self)
            if self.exit:
                break
            ctx.listfThreadRunning[n] = True
            try:
                self.thread_handler2(arg)
            except Exception as e:
                Fuck=Fuck+1
            ctx.listfThreadRunning[n] = False
            time.sleep(2)
    def thread_handler2(self, arg):
        raise NotImplementedError("must implement this function")
    def check_self_shutdown(self):
        check_for_shutdown(self)
    def try_exit(self):
        self.exit = True
        ctx.listfThreadRunning[self.n] = False
best_difficulty = 16
def bitcoin_miner(t, restarted=False):
    global best_share_difficulty, best_share_hash
    share_difficulty = 0
    difficulty = 16
    best_difficulty = 0
    target = (ctx.nbits[2:] + '00' * (int(ctx.nbits[:2], 16) - 3)).zfill(64)
    extranonce2 = hex(random.randint(0, 2**32 - 1))[2:].zfill(2 * ctx.extranonce2_size)
    coinbase = ctx.coinb1 + ctx.extranonce1 + extranonce2 + ctx.coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()
    merkle_root = coinbase_hash_bin
    for h in ctx.merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()
    merkle_root = binascii.hexlify(merkle_root).decode()
    merkle_root = ''.join([merkle_root[i] + merkle_root[i + 1] for i in range(0, len(merkle_root), 2)][::-1])
    work_on = get_current_block_height()
    ctx.nHeightDiff[work_on + 1] = 0
    _diff = int("00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
    def calculate_difficulty(target, hash_hex):
        hash_int = int(hash_hex, 16)
        target_int = int(target, 16)
        return target_int / max(hash_int, 1) 
    while True:
        t.check_self_shutdown()
        if t.exit:
            break
        if ctx.prevhash != ctx.updatedPrevHash:
            ctx.updatedPrevHash = ctx.prevhash
            bitcoin_miner(t, restarted=True)
            continue
        nonce = hex(random.randint(0, 2**32 - 1))[2:].zfill(8)
        blockheader = ctx.version + ctx.prevhash + merkle_root + ctx.ntime + ctx.nbits + nonce + '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'
        hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
        hash = binascii.hexlify(hash).decode()
        ctx.total_hashes_computed += 1  
        this_hash = int(hash, 16)
        difficulty = _diff / this_hash
        if difficulty > best_difficulty:
            best_difficulty = difficulty
        if ctx.nHeightDiff[work_on + 1] < difficulty:
            ctx.nHeightDiff[work_on + 1] = difficulty
        if hash < target:
            payload = bytes('{"params": ["' + address + '", "' + ctx.job_id + '", "' + ctx.extranonce2 + '", "' + ctx.ntime + '", "' + nonce + '"], "id": 1, "method": "mining.submit"}\n', 'utf-8')
            sock.sendall(payload)
            ret = sock.recv(1024)
            time.sleep(1)
            return True
        if difficulty >= 16:
            share_payload = {
                "params": [address, ctx.job_id, ctx.extranonce2, ctx.ntime, nonce],
                "id": 1,
                "method": "mining.submit"
            }
            share_payload = json.dumps(share_payload) + '\n'
            sock.sendall(share_payload.encode())
            response = sock.recv(1024).decode()
            share_difficulty = _diff / this_hash
        if share_difficulty < best_share_difficulty:
            best_share_difficulty = share_difficulty
            best_share_hash = hash
        if ctx.nHeightDiff[work_on + 1] < share_difficulty:
            ctx.nHeightDiff[work_on + 1] = share_difficulty
def block_listener(t) :
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.connect((pool , port))
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    ctx.sub_details , ctx.extranonce1 , ctx.extranonce2_size = response['result']
    sock.sendall(b'{"params": ["' + address.encode() + b'", "x"], "id": 2, "method": "mining.authorize"}\n')
    response = b''
    while response.count(b'\n') < 4 and not (b'mining.notify' in response) : response += sock.recv(1024)
    responses = [json.loads(res) for res in response.decode().split('\n') if
                 len(res.strip()) > 0 and 'mining.notify' in res]
    ctx.job_id , ctx.prevhash , ctx.coinb1 , ctx.coinb2 , ctx.merkle_branch , ctx.version , ctx.nbits , ctx.ntime , ctx.clean_jobs = \
        responses[0]['params']
    ctx.updatedPrevHash = ctx.prevhash
    while True :
        t.check_self_shutdown()
        if t.exit :
            break
        response = b''
        while response.count(b'\n') < 4 and not (b'mining.notify' in response) : response += sock.recv(1024)
        responses = [json.loads(res) for res in response.decode().split('\n') if
                     len(res.strip()) > 0 and 'mining.notify' in res]
        if responses[0]['params'][1] != ctx.prevhash :
            ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = responses[0]['params']
class CoinMinerThread(ExitedThread) :
    def __init__(self , arg = None) :
        super(CoinMinerThread , self).__init__(arg , n = 0)
    def thread_handler2(self , arg) :
        self.thread_bitcoin_miner(arg)
    def thread_bitcoin_miner(self , arg) :
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try :
            ret = bitcoin_miner(self)
        except Exception as e :
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False
    pass
class NewSubscribeThread(ExitedThread) :
    def __init__(self , arg = None) :
        super(NewSubscribeThread , self).__init__(arg , n = 1)
    def thread_handler2(self , arg) :
        self.thread_new_block(arg)
    def thread_new_block(self , arg) :
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try :
            ret = block_listener(self)
        except Exception as e :
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False
    pass
def StartMining() :
    subscribe_t = NewSubscribeThread(None)
    subscribe_t.start()
    time.sleep(4)
    miner_t = CoinMinerThread(None)
    miner_t.start()
if __name__ == '__main__':
    ctx.total_hashes_computed = 0
    ctx.mining_time_per_block = []
    signal(SIGINT, handler)
    StartMining()
