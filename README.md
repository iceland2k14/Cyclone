# 🚀 Cyclone: The World's Fastest CPU Satoshi Puzzle Solver

Cyclone is the fastest CPU Satoshi puzzle solver in the world, leveraging the power of modern CPU instructions such as **AVX2** and **AVX512** to achieve unparalleled performance. Designed to run on **Linux** and **Windows**, Cyclone is optimized for speed and accuracy, making it the ideal tool for solving cryptographic puzzles.
Secp256k1 math are based on the excellent work from JeanLucPons/VanitySearch (https://github.com/JeanLucPons/VanitySearch), with a few modifications.
I extend our gratitude to Jean-Luc Pons for his foundational contributions to the cryptographic community.

---

## ⚡ Key Features

- **Blazing Fast Performance**: Cyclone utilizes **AVX2** and **AVX512** instructions to deliver unmatched CPU speed in solving Satoshi puzzles.
- **Accurate Calculations**: Cyclone ensures full and correct computation of compressed public keys and **hash160**, with parallel processing for batches of 8 hashes (AVX2) and 16 hashes (AVX512).
- **Flexible Implementations**: Choose between **AVX2** and **AVX512** implementations based on your hardware capabilities.
- **Linux Compatibility**: Cyclone is designed to run seamlessly on Linux systems or Ubuntu Windows WSL 2.
- **Progress saving**: Progress is saved every 5 minutes during work in the **progress.txt** file.
- **Probabilistik search**: You can add -j key and jump forward after partial match between generated Hash160 and given Hash160
- **Partial match**: You can add -p key and save all of the partial match Hash160 to the candidates.txt file
- **Save candidates**: Only when -s key is add.
- **Threads**: You can add -t key for starting Cyclone on a few threads, not on total CPU threads.
- **Skipping public key**: Skipping and not hashing public keys if they do not match the mask (--publc-deny 2 - skip each public key which starts 2 leading zeroes).  

---

## 📊 Results Comparison

- **Processor**: Ryzen 7 5800H (8 cores, 16 threads)
- **Memory**: 32 GB DDR4 (2x16 GB)
- **Virtualization Software**: VMware® Workstation 17 (Home)

| Solver             | Speed (Mkeys/s) | Notes                                                                                      |
|--------------------|-----------------|--------------------------------------------------------------------------------------------|
| **Vanity Search**  | 35.91           | No option to select a range of private keys for search.                                    |
| **Keyhunt**        | 43              |  Computes hashes and addresses by omitting the Y coordinates for compress mode  |
| **Cyclone AVX2**   | 51.21           | Full and correct computation of compressed public keys, computing 8 hash160 per batch      |

- **Processor**: Ryzen 9 7945HX (16 cores, 32 threads)
- **Memory**: 32 GB DDR5 (32 GB)
- **Ubuntu 24.04**

| Solver             | Speed (Mkeys/s) | Notes                                                                                      |
|--------------------|-----------------|--------------------------------------------------------------------------------------------|
| **Vanity Search**  | 120             | No option to select a range of private keys for search.                                    |
| **Cyclone AVX2**   | 139             | Computing 8 hash160 per batch                                                              |
| **Cyclone AVX512** | 159             | Computing 16 hash160 per batch                                                             |

- **NB!** The Windows version of Cyclone performs 6–8% slower than the Linux version! 

---
## 🔷 Example Output

Below is an example of Cyclone in action, solving a Satoshi puzzle:  
**Sequrntial search**
```bash
root@ubuntu:/mnt/hgfs/VM/Final Cyclone# ./Cyclone -a 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k -r 875:6FAC3875
================= WORK IN PROGRESS =================
Target Address: 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k
CPU Threads   : 16
Mkeys/s       : 51.21
Total Checked : 1792436224
Elapsed Time  : 00:00:35
Range         : 875:6fac3875
Progress      : 95.6703 %
Progress Save : 0
=================== FOUND MATCH! ===================
Private Key   : 0000000000000000000000000000000000000000000000000000000006AC3875
Public Key    : 031A864BAE3922F351F1B57CFDD827C25B7E093CB9C88A72C1CD893D9F90F44ECE
WIF           : KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7wBBz2KJQdASx
P2PKH Address : 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k
Total Checked : 1816678912
Elapsed Time  : 00:00:35
Speed         : 50.9930 Mkeys/s

```
**Probabilistik search**
```bash
root@DESKTOP-BD9V01U:/mnt/e/VM/Cyclone# ./Cyclone -a 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k -r FAC875:6FAC3875 -p 6 -j 10000000 -s
================= WORK IN PROGRESS =================
Target Address: 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k
CPU Threads   : 16
Mkeys/s       : 86.47
Total Checked : 1297055616
Elapsed Time  : 00:00:15
Range         : fac875:6fac3875
Progress      : 69.8422 %
Progress Save : 0
Candidates    : 43
Jumps         : 43
================== FOUND MATCH! ==================
Private Key   : 0000000000000000000000000000000000000000000000000000000006AC3875
Public Key    : 031A864BAE3922F351F1B57CFDD827C25B7E093CB9C88A72C1CD893D9F90F44ECE
WIF           : KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7wBBz2KJQdASx
P2PKH Address : 128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k

```
**Partial match saving**
```bash
000000000000000000000000000000000000000000000000000000006D5EBF34 036A8EAA5A03E6F7AF79D1BE98249F8734F53024960F4F0BA6712FDAA6BF13708E 0c7aafd38f34f5ccb1fa9aaea0eba122c1ba815f
0000000000000000000000000000000000000000000000000000000058BCE335 02B3D54D48AB49C09CF06F5787348DC65ECD17517668E1B23A9287EB63937CE980 0c7aafaf300f05d9e0eb18846fd27572927807c5
00000000000000000000000000000000000000000000000000000000297E826F 023A68273D96301A2D3D780F9D1521753A29EF82ED91F47A637EE3A93E04FF5F77 0c7aafc3c406bdf95a6f4bb56bd8f654322acd82
000000000000000000000000000000000000000000000000000000003DBB99C6 027DC22FB226F88AD60837E88E639A292945119AFEC876D035EB41E609852BD36A 0c7aaf9550a08a9ecad523f5b9b980ca450a4e24
0000000000000000000000000000000000000000000000000000000066A00845 02A1BE7AD6DFD68BEE90B6574B0112450398B8D0B4072850F6B7853794EA12F9EB 0c7aaff2aaf92d8837e9fb5b8232969cfa6a2717
000000000000000000000000000000000000000000000000000000005FC7B9EF 038E608258A758CD367782724A186AFB6C64065A5813EBF7ED2A2853968A63D577 0c7aaf157f41f21bf377678e7f44f95b8c7dc497
00000000000000000000000000000000000000000000000000000000439899C5 03DC27612EDC7072EF57569E5C05FDCDAE0F12DCA53F70878430D8585D42F97221 0c7aafa30797c31f7ffd4ff742183e905902e8ce
0000000000000000000000000000000000000000000000000000000037A4D5F5 0303C1B9C1C7B68BA5B9D588147031B309F4F2ADDD3EBA8A817173CB4D6F7F4D1A 0c7aaf56e9e06cd2ab6ad6438a0b89478d184243
0000000000000000000000000000000000000000000000000000000006AC3875 031A864BAE3922F351F1B57CFDD827C25B7E093CB9C88A72C1CD893D9F90F44ECE 0c7aaf6caa7e5424b63d317f0f8f1f9fa40d5560

```

Progress.txt sample
```bash
Progress Save #1 at 300 sec: TotalChecked=14548403200, ElapsedTime=00:04:55, Mkeys/s=49.32
Thread Key 0: 0000000000000000000000000000000000000000000000007FFFF0003769451A
Thread Key 1: 0000000000000000000000000000000000000000000000007FFFF10037363C56
Thread Key 2: 0000000000000000000000000000000000000000000000007FFFF20035B32EE8
Thread Key 3: 0000000000000000000000000000000000000000000000007FFFF30037BAE12C
Thread Key 4: 0000000000000000000000000000000000000000000000007FFFF4003775371C
Thread Key 5: 0000000000000000000000000000000000000000000000007FFFF5003719E4CA
Thread Key 6: 0000000000000000000000000000000000000000000000007FFFF60035ABDE40
Thread Key 7: 0000000000000000000000000000000000000000000000007FFFF7003768D788
Thread Key 8: 0000000000000000000000000000000000000000000000007FFFF80037533144
Thread Key 9: 0000000000000000000000000000000000000000000000007FFFF90035AD62BA
Thread Key 10: 0000000000000000000000000000000000000000000000007FFFFA003705ECD6
Thread Key 11: 0000000000000000000000000000000000000000000000007FFFFB0035A637EC
Thread Key 12: 0000000000000000000000000000000000000000000000007FFFFC0037B613FE
Thread Key 13: 0000000000000000000000000000000000000000000000007FFFFD00374EDF9A
Thread Key 14: 0000000000000000000000000000000000000000000000007FFFFE0037166A48
Thread Key 15: 0000000000000000000000000000000000000000000000007FFFFF0037270B96

Progress Save #2 at 600 sec: TotalChecked=29457986560, ElapsedTime=00:09:55, Mkeys/s=49.51
Thread Key 0: 0000000000000000000000000000000000000000000000007FFFF0006F2E0062
Thread Key 1: 0000000000000000000000000000000000000000000000007FFFF1006ECD7D46
Thread Key 2: 0000000000000000000000000000000000000000000000007FFFF2006BF8BEDC
Thread Key 3: 0000000000000000000000000000000000000000000000007FFFF3006FBD943E
Thread Key 4: 0000000000000000000000000000000000000000000000007FFFF4006F2B7EE6
Thread Key 5: 0000000000000000000000000000000000000000000000007FFFF5006E9339C4
Thread Key 6: 0000000000000000000000000000000000000000000000007FFFF6006BFBE1B6
Thread Key 7: 0000000000000000000000000000000000000000000000007FFFF7006F3CFB58
Thread Key 8: 0000000000000000000000000000000000000000000000007FFFF8006EFAE9AC
Thread Key 9: 0000000000000000000000000000000000000000000000007FFFF9006BECBCEA
Thread Key 10: 0000000000000000000000000000000000000000000000007FFFFA006E843ECE
Thread Key 11: 0000000000000000000000000000000000000000000000007FFFFB006BF02B78
Thread Key 12: 0000000000000000000000000000000000000000000000007FFFFC006FB43F9C
Thread Key 13: 0000000000000000000000000000000000000000000000007FFFFD006EFDE8AA
Thread Key 14: 0000000000000000000000000000000000000000000000007FFFFE006EA5CD1E
Thread Key 15: 0000000000000000000000000000000000000000000000007FFFFF006EBC9242


(base) C:\Continuum\Anaconda3\>python go.py

[+] Starting Program.... Please Wait !
[+] Search Mode: Sequential Random in each Loop. seq = 67,108,864
[+] Total Unsolved: 78 Puzzles in the bit range [71-160]
[+] Target Selected : Puzzle #81  with Address: 15qsCm78whspNQFydGJQk5rexzxTQopnHZ
[I: 112] [Puzz: 81] [T:7,516,192,768] [Time(h:m:s): 00:01:39.19]
[From: 1523AEE3C561B7F999923] [80.40186 bit]
[To  : 1523AEE3C561B83999923] [80.40186 bit]
SIGINT or CTRL-C detected. Exiting gracefully. BYE
```

## 🛠️ Getting Started

To get started with Cyclone, clone the repository and follow the installation instructions:

```bash
## AVX2 ##
git clone https://github.com/Dookoo2/Cyclone.git
cd Сyclone
cd Cyclone_avx2
g++ -std=c++17 -Ofast -funroll-loops -ftree-vectorize -fstrict-aliasing -fno-semantic-interposition -fvect-cost-model=unlimited -fno-trapping-math -fipa-ra -fipa-modref -flto -fassociative-math -fopenmp -mavx2 -mbmi2 -madx -o Cyclone Cyclone.cpp SECP256K1.cpp Int.cpp IntGroup.cpp IntMod.cpp Point.cpp ripemd160_avx2.cpp p2pkh_decoder.cpp sha256_avx2.cpp
## AVX512 ##
git clone https://github.com/Dookoo2/Cyclone.git
cd Сyclone
cd Cyclone_avx512
g++ -std=c++17 -Ofast -ffast-math -funroll-loops -ftree-vectorize -fstrict-aliasing -fno-semantic-interposition -fvect-cost-model=unlimited -fno-trapping-math -fipa-ra -mavx512f -mavx512vl -mavx512bw -mavx512dq -fipa-modref -flto -fassociative-math -fopenmp -mavx2 -mbmi2 -madx -o Cyclone Cyclone.cpp SECP256K1.cpp Int.cpp IntGroup.cpp IntMod.cpp Point.cpp ripemd160_avx2.cpp p2pkh_decoder.cpp sha256_avx2.cpp ripemd160_avx512.cpp sha256_avx512.cpp
```
To compile the program, you need MinGW (Minimalist GNU for Windows): **sudo apt install g++-mingw-w64-x86-64-posix**

For instructions on how to compile the program in Linux for Windows (via MinGW), refer to the top of the file Cyclone.cpp.

## 🚧**VERSIONS**
**V1.4**: Added the -t key, threads for Cyclone start. Also added --public-deny, it skips any public key whose compressed X-coordinate starts with K leading zero hex digits, preventing it from entering the AVX2 hashing pipeline. Speed up to 5% of search.  
**V1.3**: Added the -s key to save candidates into the candidates.txt file. Added Hash160 to the statistics output  (AVX2 version!)  
**V1.2**: Added keys: -p (partial match -> writes to the candidates.txt file, example -p 6 (comparison of the first 6 HEX) and -j (jump forward after partial match, example -j 1000000) (AVX2 version!)  
**V1.1**: Speed up to 20% (AVX2 version!)  
**V1.0**: Release

## ✌️**TIPS**
BTC: bc1qtq4y9l9ajeyxq05ynq09z8p52xdmk4hqky9c8n

