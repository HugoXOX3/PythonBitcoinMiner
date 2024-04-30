# Bitcoin Solo Miner

---
Details
---

Fee of Miner is 0%

Support Mutilple device like IOS,Android,ARM device,etc

Keep upgrading

Solo project

---
Pool Setting
---

Deafult Pool is [Ckpool](https://solo.ckpool.org)

Can Customise Solo Miner Pool(Still recommend ckpool Cuz it has the highest compatibility)

Password is 'x' cuz most pool didnt have passwd or ignore it

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


# For Normal Version(Windows.zip/Other.zip)


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

![Windows example](https://github.com/HugoXOX3/PythonMiner/blob/main/Windows%20Version.png)


# For Hide Console Version
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
pip3 install traceback
pip3 install signal
pip3 install requests
pip3 install colorama
pip3 install lxml
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
git clone https://github.com/HugoXOX3/PythonMiner.git
pip3 install traceback
pip3 install signal
pip3 install requests
pip3 install colorama
pip3 install lxml
cd PythonMiner
python3 SoloMiner.py
```
Finally,type in your Bitcoin Address and Enjoy mining

Like:

![example](https://github.com/HugoXOX3/PythonMiner/blob/main/IOS.jpeg)

---
Comming Soon
---

*More lighter than before
*Pefromance for better.

---
Warning
---

⚠️Coming soon(bruh)

---
Thx for all
---
That for all.If you want to view your stats of miner you can go to [solo.ckpool.org](https://solo.ckpool.org/)

[D0nate me with BTC:bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth](bitcoin:bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth?message=Donate)

![Donation](https://github.com/HugoXOX3/PythonMiner/blob/main/Donate.jpeg)

---
Done & unpossible
---

✅Mining with IOS(I already have some ideas to mine on it by using [ish](https://github.com/ish-app/ish)

✅Save Address Function

✅Customise Solo Mining pool(Bug Fix)

