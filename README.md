# **IF YOU ARE USING THIS FOR A TOURNAMENT, PLEASE PROVIDE CREDIT AS A LINK TO THIS REPO. THANKS!**

[![Discord](https://img.shields.io/badge/discord-join-7389D8?style=flat&logo=discord)](https://discord.gg/uGuswsZwAT)

# ggsheet
 automatic generation of valorant esports post-game stats sheets

![b2ab433e-3ac4-46d3-bc8f-1c147b04de07](https://user-images.githubusercontent.com/42125428/144948070-98fe383f-3c0e-4dc6-b3f9-6d11a2ac4793.png)

## Usage

### Prerequisites
Python >= 3.7

### 1. Clone GitHub Repository
[Download](https://github.com/colinhartigan/ggsheet/archive/refs/heads/master.zip) or clone the repo:
```
git clone https://github.com/colinhartigan/ggsheet.git
```

### 2. Install Python packages
```cmd
python -m pip install -r requirements.txt
```

### 3. Set region
In `src/valorant_manager.py` change `Client(region="na")` to your region.

Valid regions are: `na, eu, latam, br, ap, kr, pbe`

### 4. Run
```cmd
python main.py
```
Images are outputted in `/output` with the file name being the match uuid
