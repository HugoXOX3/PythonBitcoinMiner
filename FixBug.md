#Fix Error

---
Error 1
---
```
PS C:\Users\user\Desktop\Other>  & 'c:\Users\user\AppData\Local\Programs\Python\Python312\python.exe' 'c:\Users\user\.vscode\extensions\ms-python.debugpy-2024.4.0-win32-x64\bundled\libs\debugpy\adapter/../..\debugpy\launcher' '51020' '--' 'C:\Users\user\Desktop\Other\SoloMiner.py'
Use Stored Address:(Y/N)Y
Opening Address.txt
Other Pool like public-pool or nerdminers pool
Mining Pool that you want:public-pool.io
Mining Pool Port:21496
  BTC WALLET:  bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth 
 [ 16:04:41.041601 ]  [*] Subscribe thread started.
 [   [ 16:04:45.042747 ]  [*] Miner()16:04:45.042747
 ]  [*] Bitcoin Miner Thread Started
 --------------~~(   HCMLXOX   )~~--------------
Traceback (most recent call last):
  File "C:\Users\user\Desktop\Other\SoloMiner.py", line 231, in thread_bitcoin_miner
    ret = bitcoin_miner(self)
          ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\user\Desktop\Other\SoloMiner.py", line 108, in bitcoin_miner
    target = (ctx.nbits[2 :] + '00' * (int(ctx.nbits[:2] , 16) - 3)).zfill(64)
              ~~~~~~~~~^^^^^
TypeError: 'NoneType' object is not subscriptable
```
Image:

![Error1](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/Error1.png)

Reason:

1.Type in wrong mining pool host,check it again.

2.Mining Pool not support in your country.Try to use a VPN or Proxy.

