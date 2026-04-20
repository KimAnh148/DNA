# 🧬 DNA-GET/GDT: DNA-Based Genetic Encryption & Decryption

This program simulates the algorithm presented in the research paper by Nitya Sree.P (17MIS1007).I have further extended this implementation to support both Text and Audio data processing. 
It is a symmetric encryption system that combines **DNA computing** with **genetic algorithm operators** (crossover and mutation) to encrypt and decrypt arbitrary text data.

---

## 📖 Overview

This project implements two complementary algorithms:

- **DNA-GET** *(DNA Genetic Encryption Technique)* — encrypts plaintext into a DNA base sequence using genetic operations.
- **DNA-GDT** *(DNA Genetic Decryption Technique)* — reverses the process to recover the original plaintext from the encrypted DNA sequence and a key file.

The core idea is to represent binary data as DNA base sequences (`A`, `C`, `G`, `T`) and then apply biologically-inspired transformations — crossover and mutation — across multiple rounds to produce ciphertext that is difficult to reverse without the key.

---

## 🔬 How It Works

### Encryption (DNA-GET)

```
Input Data (Text / Image / Audio)
   │
   ▼
Binarize → Convert to DNA bases
   │
   ▼  ┌─────────────── N rounds ───────────────┐
   ├──► XOR with secret key                    │
   ├──► Reshape → Chromosome population        │
   ├──► Crossover (rotate / single-point / both)│
   └──► Mutation (complement + alter DNA bases) ┘
   │
   ▼
Encrypted DNA sequence  +  Key file
```

### Decryption (DNA-GDT)

Decryption runs the same rounds **in reverse order**, undoing each operation using parameters stored in the key file:

```
Encrypted DNA sequence  +  Key file
   │
   ▼  ┌─────────────── N rounds (reversed) ────┐
   ├──► Reshape → Chromosome population        │
   ├──► Reverse Mutation                       │
   └──► Reverse Crossover                     ┘
   │
   ▼
XOR with secret key → DNA → Binary → Original Data (Text / Image / Audio)
```

### Key Components

| Component | Description |
|-----------|-------------|
| **XOR encryption** | Data XORed with a randomly generated binary key each round |
| **Reshape** | DNA sequence split into chromosomes of random length |
| **Rotate crossover** | Each chromosome rotated left or right by a random offset |
| **Single-point crossover** | Adjacent chromosome pairs swapped around a random crossover point |
| **Mutation – complement** | Bits between two random points are flipped |
| **Mutation – alter DNA bases** | DNA bases mapped to each other (e.g. `A↔T`, `C↔G`) between two random points |

All parameters (number of rounds, crossover points, rotation offsets, mutation tables, etc.) are serialized into a **key file** during encryption and consumed during decryption.

---

## 📁 Project Structure

```
.
├── dna_get.py              # Encryption algorithm with Image(DNA-GET)
├── dna_gdt.py              # Decryption algorithm with Image (DNA-GDT)
├── enc_dec_exec.py         # Entry point: runs encryption then decryption with Image
├── utils.py                # Shared utilities: bit/DNA conversion, XOR, tables, delimiters
├── DNATEXT/                # Folder of encryption and decryption algorithm with text
├── DNAath/                 # Folder of encryption and decryption algorithm with audio
├── DNA_key/                # Stored key files
├── key/                    # Key files generated during encryption
├── encrypted_dna/          # Encrypted DNA sequences (text)
├── encrypted_image/        # Encrypted image data
├── decrypted_binary/       # Decrypted binary output files
├── decrypted_image/        # Recovered image output files
├── original_binary/        # Original binary input files
└── original_image/         # Original image input files

```

---

## ⚙️ Requirements

- Python 3.7+
- No third-party libraries required (uses only `ast`, `random`, `string`, `time` from the standard library)

---

## 🚀 Usage

### Run Encryption + Decryption (end-to-end)

```bash
python enc_dec_exec.py
```

This will:
1. Encrypt the hardcoded sample text and write the result to the encrypted file.
2. Decrypt it back and verify the output matches the original.

### Run Encryption Only

```bash
python dna_get.py
```

Outputs:
- `original.txt` — the original plaintext
- `encrypted.txt` — the encrypted DNA sequence
- `key.txt` — the key file needed for decryption

### Run Decryption Only

```bash
python dna_gdt.py
```

Reads `encrypted.txt` and `key.txt`, then writes the recovered text to `decrypted.txt`.

---

## 🔑 Key File Format

The key file is a structured string containing all parameters needed for decryption, including:

- The binary XOR key
- Number of rounds
- Per-round: reshape info, crossover type & parameters, mutation table, complement points, and alter points

This file must be kept secret — it is equivalent to the encryption key.

---

## 📝 Customization

To encrypt your own text, edit the `text` variable in `dna_get.py`:

```python
text = "Your secret message here"
```

To change the key length (default: 128-bit / 16 ASCII characters):

```python
key = str2bin(''.join(random.SystemRandom().choice(...) for _ in range(16)))
#                                                                       ^^
#                                                              change key length here
```

The number of encryption rounds is chosen **randomly** (odd number between 3 and 11) on each run.

---

## 🧪 Example Output

```
######## ENCRYPTION ########

DNA-GET is running...

Initial DNA sequence: ACGTACGT...
Final DNA sequence: TGCATGCA...
Total execution time: 0.0032s

######## DECRYPTION ########

DNA-GDT is running...

Decrypted text: In computer science and operations research...
Decryption succeeded.
```

---

## 📚 Background

This project is inspired by research on DNA-based cryptography of Nitya Sree.P (17MIS1007), which leverages:

- The vast information density of DNA (4 bases vs 2 binary digits)
- The parallel nature of biological processes
- Genetic algorithm operators (crossover, mutation) as transformation primitives

The approach encodes binary data using a two-bits-per-base mapping and applies multiple randomized transformations per round, with the full transformation sequence stored in the key.


