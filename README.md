# Bitcoin Solo Miner

---

## Latest Version

[Version Beta v2.0.0](https://github.com/HugoXOX3/PythonBitcoinMiner/releases/tag/Minerv2.0.0)

This is still a debug version which fixes all the bugs in version v1.x.x.

However, it may have some new bugs or errors.

Please report any issues at [Issues](https://github.com/HugoXOX3/PythonBitcoinMiner/issues) to help improve and fix the program.

## Bitcoin Solo Miner Version 1.x.x and Documentation

---

## Details

This SoloMiner does not request any development fee and connects to the blockchain API to get details like TxIndex to alternate RPC server. As a result, we do not need to run a Bitcoin core locally, and we can send our accepted shares to your mining pool like ckpool.

---

## Error Occurred?

[Go here](https://github.com/HugoXOX3/PythonMiner/blob/main/FixBug.md) to find out the reason and how to fix it.

---

## Need Help?

[Go here](https://github.com/HugoXOX3/PythonMiner/discussions)

---

## Requirements

- Python 3.x
  - [Download Python](https://www.python.org/)
- Create your own Bitcoin Address:
  - [Bitcoin Core](https://bitcoin.org/en/bitcoin-core/)
  - [Electrum](https://electrum.org/?ref=hackernoon.com) 
  - (Just prepare an address that you want to use)

---

## Download the Release

First, download the latest miner from [releases](https://github.com/HugoXOX3/BTCSoloMiner/releases)

# Mining BTC with

- [Windows/Linux/Mac](https://github.com/HugoXOX3/PythonMiner#for-windows-linux-mac)
- [Hide Console Version](https://github.com/HugoXOX3/PythonMiner#for-hide-console-version)
- [Android & IOS](https://github.com/HugoXOX3/PythonMiner#androidios)
- [UNIX](https://github.com/HugoXOX3/PythonMiner/blob/main/UNIX.md)

# For Windows/Linux/Mac

## How to Use

1. Change the settings:
   ```python
   # Setting
   # Mining Address **Change Me**
   address = 'xxx'
   # Mining Pool
   pool = "solo.ckpool.org"
   port = 3333
   ```

2. Run the program:
   ```sh
   python3 SoloMiner.py
   ```

![Windows example](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/Windows%20Version.png)

# For Hide Console Version

1. Change the settings:
   ```python
   # Setting
   # Mining Address **Change Me**
   address = 'xxx'
   # Mining Pool
   pool = "solo.ckpool.org"
   port = 3333
   ```

2. Run the program:

Double-click `main.pyw` to start the program or type in terminal/cmd:
   ```sh
   main.pyw
   ```
You can confirm it is running in Task Manager (look for python.exe).

Windows users can also drag this file into `shell:startup` so that mining will start automatically when the PC is on.

# Android & iOS

The way to run this miner on Android and iOS is to run a Linux Terminal on them, like Termux & iSH.

---

## Android

1. [Go to the Play Store and download Termux](https://play.google.com/store/apps/details?id=com.termux)

2. Open Termux and type:
   ```sh
   pkg update
   pkg upgrade
   pkg install python3
   pkg install git
   pip3 install requests colorama
   git clone https://github.com/HugoXOX3/PythonMiner.git
   cd PythonMiner
   ```

3. Change the wallet in this program to yours using nano or vim:
   ```python
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

4. Run the program:
   ```sh
   python3 SoloMiner.py
   ```

5. Input your Bitcoin address and enjoy mining.

---

## iOS

1. Download the app [iSH](https://apps.apple.com/cn/app/ish-shell/id1436902243) from the App Store and launch it.

2. Type to install stuff:
   ```sh
   apk add python3
   apk add git
   git clone https://github.com/HugoXOX3/PythonMiner.git
   cd PythonMiner
   ```

3. Change the wallet in this program to yours using nano or vim:
   ```python
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

4. Run the miner:
   ```sh
   python3 SoloMiner.py
   ```

5. Input your Bitcoin address and enjoy mining.

![example](https://github.com/HugoXOX3/PythonMiner/blob/main/Image/IOS.jpeg)

---

## Warning

⚠️ Mining Bitcoin on a mobile device with poor cooling may damage your device.

---

## Credits

- [BitcoinSoloPy](https://github.com/DaCryptoRaccoon/BitcoinSoloPy)
- [SoloMinerV2](https://github.com/Pymmdrza/SoloMinerV2)

---

## Done

- ✅ Mining with iOS (I already have some ideas to mine on it by using [iSH](https://github.com/ish-app/ish))
- ✅ Save Address Function
- ✅ Customize Solo Mining Pool (Bug Fix)
