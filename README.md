# Bitcoin Solo Miner

---
Details
---

Fee of Miner is 0%

Support Mutilple device like IOS,Android,ARM device,etc

Keep upgrading

Solo project

A part of code is base on [BitcoinSoloPy](https://github.com/DaCryptoRaccoon/BitcoinSoloPy) and [SoloMinerV2](https://github.com/Pymmdrza/SoloMinerV2)

---
Error Occur?
---

[Go to here](https://github.com/HugoXOX3/PythonMiner/blob/main/FixBug.md) to find out the reason and fix it.

---
Requirement
---

Python3.x
[Go Download](https://www.python.org/)

Create your own Bitcoin Address:[Bitcoin Core](https://bitcoin.org/en/bitcoin-core/)/[Electrum](https://electrum.org/?ref=hackernoon.com) etc(Just prepare address that you want to)

---
Download the relase
---

First,Download the latest miner from [release(Windows.zip/Other.zip/Hide_consoele_version.zip)](https://github.com/HugoXOX3/BTCSoloMiner/releases)

# Mining BTC with

[Windows/Linux](https://github.com/HugoXOX3/PythonMiner#for-normal-versionwindowszipnormalzip)

[Hide Console Version](https://github.com/HugoXOX3/PythonMiner#for-hide-console-version)

[Android & IOS](https://github.com/HugoXOX3/PythonMiner#androidios)

[UNIX](https://github.com/HugoXOX3/PythonMiner/blob/main/UNIX.md)


# For Normal Version(Windows.zip/Other.zip)(Stop update)


---
To install requirement with pip
---
Next,If you are windows user than run :
```
build.bat
```
Linux and Mac user run :
```
bash build.sh
```
---
Run programme
---
Then,run "SoloMiner.exe" for windows user:
```
SoloMiner.exe
```

Linux and Mac user run:
```
python Solominer.py
```
After that,input your btc address in cmd or terminal.

Example:

![Windows example](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/Windows%20Version.png)


# For Hide Console Version(Stop update)
---
Latest release
---
[Python BTC Solo Miner v1.3.1]((https://github.com/HugoXOX3/PythonMiner/releases/tag/Minerv1.3.1)

---
Requriment
---

Remeber to install python3,pip3,and lxml like normal

---
Change the address in main.pyw
---
Using VIM,NANO or other IDLE to change my wallet'bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth' to yours btc address.

---
Run programme
---

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
git clone https://github.com/HugoXOX3/PythonMiner.git
cd PythonMiner
```

Then,you need to type to install requirement
```
pip3 install tqdm tabulate requests colorama
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
apk add py3-pip
apk add git
apk add py3-psutil
git clone https://github.com/HugoXOX3/PythonMiner.git
pip3 install tqdm tabulate requests colorama
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
Comming Soon
---

*Pefromance be better.

---
Warning
---

⚠️Coming soon(Just Kidding)

---
Thx for all
---
That for all.If you want to view your stats of miner you can go to [solo.ckpool.org](https://solo.ckpool.org/)

[D0nate with BTC:bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth](bitcoin:bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth?message=Donate)

<img src="https://github.com/HugoXOX3/PythonMiner/blob/main/Image/Donate.jpeg" width="449" height=579>

---
Contact me
---

[Telegrame](https://t.me/iamnotniko)

---
Done
---

✅Mining with IOS(I already have some ideas to mine on it by using [ish](https://github.com/ish-app/ish)

✅Save Address Function

✅Customise Solo Mining pool(Bug Fix)

