# Blum-blum-shub-app

## Setting up the program (CLI Version)
 
 1. Run ```pip install -r requirements.txt```
 
## CLI Commands
- ```python main.py``` - Shows options
- ```python main.py key-gen``` - Generates a key in hexidecimal that can be copied to use as a key
- ```python main.py encrypt {key in hex} {plaintext-file-path} {encrypted-folder-directory}```
- ```python main.py decrypt {key in hex} {ciphertext-file-path} {decrypted-folder-directory}```

## Examples
- ```4cd66d14e0ebd63aab475ecf68b9c4b2``` generated using  ```python main.py key-gen``` 
- ```python main.py encrypt 4cd66d14e0ebd63aab475ecf68b9c4b2 test_data/recording.mp4 test_data```
- ```python main.py decrypt 4cd66d14e0ebd63aab475ecf68b9c4b2 test_data/recording.mp4.enc test_data```