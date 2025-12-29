# IMAGE STEGANOGRAPHY

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Security](https://img.shields.io/badge/AES--256-KMS-00FFFF?style=for-the-badge)

A high-performance cybersecurity tool developed for secure data concealment. This project implements a **Dual-Layer Security Protocol** by combining **AES-256 Bit Encryption** with **Vectorized LSB (Least Significant Bit) Steganography**.

## Security Architecture

Standard steganography is often vulnerable to simple LSB analysis. STEGO-KMS mitigates this risk through a layered defense:

1.  **KMS Layer (Key Management):** Uses SHA-256 to derive a deterministic 32-byte key from a user-defined password.
2.  **Encryption Layer:** Encrypts the plaintext payload into an AES-256 (Fernet) cipher-text.
3.  **Stego Layer:** Injects the encrypted binary data into the LSBs of the carrier image using high-speed NumPy vectorization.



## Key Features

* **Dark Terminal Interface:** Professional high-contrast UI designed for security monitoring environments.
* **Vectorized Performance:** Optimized with NumPy to handle high-resolution 4K images in milliseconds.
* **Early-Exit Decoding:** Advanced scanning logic that stops the moment the data delimiter is detected.
* **Zero-Log Protocol:** No data or images are stored on the server; all processing happens in-memory.
* **Integrity Verification:** Built-in error handling for corrupted artifacts or invalid authorization keys.

## Technology Stack

- **Core:** Python 3.9+
- **Frontend:** Streamlit (Custom CSS Dark Theme)
- **Image Processing:** NumPy, Pillow (PIL)
- **Cryptography:** Cryptography.io (Fernet/AES-256)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gourav1612/stego_minor_project
   cd stego_minor_project
