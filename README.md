# Bitcoin Solo Miner

---
Updatest Version
---
[Version Beta v2.0.0](https://github.com/HugoXOX3/PythonBitcoinMiner/releases/tag/Minerv2.0.0)

It is still a debug version which fix all the bug in version v1.x.x.

However,it may have some new bugs or errors.

Please report it at [Issues](https://github.com/HugoXOX3/PythonBitcoinMiner/issues) to improve and fix the program.

---
Details of Bitcoin Solo Miner Version 1.x.x and Document
---

This SoloMiner doesnt request any developing fee and it connect to blockchain api the get details like TxIndex to alternate RPC server.As a result,we dont need to run a bitcoin core in local and we can sent our accept share into your mining pool like ckpool


---
Error Occur?
---

[Go to here](https://github.com/HugoXOX3/PythonMiner/blob/main/FixBug.md) to find out the reason and fix it.


---
Ask for help?
---
[Go to here](https://github.com/HugoXOX3/PythonMiner/discussions)

---
Requirement
---

Python3.x
[Go Download](https://www.python.org/)

Create your own Bitcoin Address:[Bitcoin Core](https://bitcoin.org/en/bitcoin-core/)/[Electrum](https://electrum.org/?ref=hackernoon.com) etc(Just prepare address that you want to)

---
Download the relase
---

First,Download the latest miner from [release](https://github.com/HugoXOX3/BTCSoloMiner/releases)

# Mining BTC with

[Windows/Linux/Mac](https://github.com/HugoXOX3/PythonMiner#for-windows-linux-mac)

[Hide Console Version](https://github.com/HugoXOX3/PythonMiner#for-hide-console-version)

[Android & IOS](https://github.com/HugoXOX3/PythonMiner#androidios)

[UNIX](https://github.com/HugoXOX3/PythonMiner/blob/main/UNIX.md)


# For Windows  Linux  Mac

# How to use

1. Change the setting 
```
#Setting
# Mining Address **Change Me**
address = 'xxx'
# Mining Pool
pool = "solo.ckpool.org"
port = 3333
```

2. run the programme like:
```
python3 SoloMiner.py
```


![Windows example](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/Windows%20Version.png)


# For Hide Console Version

1. Change the setting
```
#Setting
# Mining Address **Change Me**
address = 'xxx'
# Mining Pool
pool = "solo.ckpool.org"
port = 3333
```

2. Run programme

Double click 'main.pyw' to start programme or type in terminal/cmd like :
```
main.pyw
```
You can confirm it run in Task Manager(Find the usage of python.exe).

BTW,Windows User can also drag this file into'shell:startup' so that mining will start automaticlly when PC is on


# Android&IOS

The ways I find out to run this miner on Android and IOS is to run a Linux Terminal on them like Termux & Ish

---
Android
---
[First,Go to play store and downlaod Termux](https://play.google.com/store/apps/details?id=com.termux)

Next,open Termux and type:

```
pkg update
pkg upgrade
pkg install python3
pkg install git
pip3 install requests colorama
git clone https://github.com/HugoXOX3/PythonMiner.git
cd PythonMiner
```

Then,you need to change the wallet in this programme to yours by using nano or vim
```
# Python Bitcoin Solo Miner
import requests
import socket
.
.
.

## Mining Address **Change Me**
address = 'Change this to your wallet'
pool = 'stratum.solomining.io'
port = 7777
```


After that,You can run the programe like:
```
python3 SoloMiner.py
```

Finally,Just input your Bitcoin address an enjoy mining

---
IOS
---
First,download app [ish](https://apps.apple.com/cn/app/ish-shell/id1436902243) in appstore and launch it

Next,type to install stuff
```
apk add python3
apk add git
git clone https://github.com/HugoXOX3/PythonMiner.git
cd PythonMiner
```

Also you need to change the wallet in this programme to yours by using nano or vim
```
# Python Bitcoin Solo Miner
import requests
import socket
.
.
.

## Mining Address **Change Me**
address = 'Change this to your wallet'
pool = 'stratum.solomining.io'
port = 7777
```

After that type this to run miner 
```
python3 SoloMiner.py
```

Finally,type in your Bitcoin Address and Enjoy mining

Like:

![example](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/IOS.jpeg)

---
Warning
---

⚠️ Mining Bitcoin on a mobile device with a bad cooling may damage your device

---
Credits
---

[BitcoinSoloPy](https://github.com/DaCryptoRaccoon/BitcoinSoloPy)

[SoloMinerV2](https://github.com/Pymmdrza/SoloMinerV2)

---
Done
---

✅Mining with IOS(I already have some ideas to mine on it by using [ish](https://github.com/ish-app/ish)

✅Save Address Function

✅Customise Solo Mining pool(Bug Fix)

