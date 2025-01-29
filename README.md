# Bitcoin Solo Miner

---

## Latest Version

[Version v2.0.0](https://github.com/HugoXOX3/PythonBitcoinMiner/releases)

Please report any issues at [Issues](https://github.com/HugoXOX3/PythonBitcoinMiner/issues) to help improve and fix the program.

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
- [Android & IOS](https://github.com/HugoXOX3/PythonMiner#androidios)

# For Windows/Linux/Mac

## How to Use

1. Change the settings:
   ```json
    {
     "pool_address":"public-pool.io",
     "pool_port": 21496,
     "user_name":"bc1qp84qrxsntmpyekp9vzdenlt8khnj0h4wqafeqe",
     "password":"x",
     "min_diff":0.01
    }
   ```

2. Run the program:
   ```sh
   python3 SoloMiner.py
   ```

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
   pip3 install -r requirements.txt
   git clone https://github.com/HugoXOX3/PythonMiner.git
   cd PythonMiner
   ```

3. Change the wallet in this program to yours using nano or vim:
   ```json
    {
     "pool_address":"public-pool.io",
     "pool_port": 21496,
     "user_name":"bc1qp84qrxsntmpyekp9vzdenlt8khnj0h4wqafeqe",
     "password":"x",
     "min_diff":0.01
    }
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
   apk add py3-pip
   pip3 install -r requirements.txt
   git clone https://github.com/HugoXOX3/PythonMiner.git
   cd PythonMiner
   ```

3. Change ```config.json``` into your personal information
   ```json
    {
     "pool_address":"public-pool.io",
     "pool_port": 21496,
     "user_name":"bc1qp84qrxsntmpyekp9vzdenlt8khnj0h4wqafeqe",
     "password":"x",
     "min_diff":0.01
    }
   ```

4. Run the miner:
   ```sh
   python3 SoloMiner.py
   ```

5. Input your Bitcoin address and enjoy mining.

---

## Warning

⚠️ Mining Bitcoin on a mobile device with poor cooling may damage your device.

---

## Donation

BTC:bc1qk5tpd68l4gfj6uzkq7u0l998dzvzyjpzhgpvnm
