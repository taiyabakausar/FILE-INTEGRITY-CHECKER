import hashlib
import os

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # Read the file in chunks to avoid memory issues with large files
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_sha256.update(byte_block)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    return hash_sha256.hexdigest()

def check_file_integrity(file_path, stored_hash):
    """Check if the current file hash matches the stored hash."""
    current_hash = calculate_file_hash(file_path)
    if current_hash is None:
        return False
    return current_hash == stored_hash

def main():
    # Specify the file to monitor and the hash file
    file_to_monitor = 'example.txt'  # Change this to your target file
    hash_file = 'file_hash.txt'  # File to store the hash value

    # Check if the hash file exists
    if not os.path.exists(hash_file):
        # Calculate and store the hash if it doesn't exist
        file_hash = calculate_file_hash(file_to_monitor)
        if file_hash:
            with open(hash_file, 'w') as f:
                f.write(file_hash)
            print(f"Hash for {file_to_monitor} stored in {hash_file}.")
        else:
            print("Could not calculate hash. Exiting.")
            return

    # Read the stored hash
    with open(hash_file, 'r') as f:
        stored_hash = f.read().strip()

    # Check file integrity
    if check_file_integrity(file_to_monitor, stored_hash):
        print(f"No changes detected in {file_to_monitor}.")
    else:
        print(f"Changes detected in {file_to_monitor}!")

if __name__ == "__main__":
    main()