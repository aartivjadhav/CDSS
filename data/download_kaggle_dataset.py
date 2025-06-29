import os
import zipfile
import subprocess

# Define constants
KAGGLE_DATASET = "tboyle10/medicaltranscriptions"
DOWNLOAD_DIR = "data"
ZIP_FILE = "medicaltranscriptions.zip"

def ensure_kaggle_json():
    """
    Ensure that the Kaggle API token is correctly set up.
    """
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_json_path):
        raise FileNotFoundError(
            f"Missing Kaggle API token at {kaggle_json_path}. "
            "Download it from https://www.kaggle.com/account and place it in ~/.kaggle/"
        )

def download_dataset():
    """
    Download dataset using Kaggle CLI.
    """
    print(f"Downloading dataset: {KAGGLE_DATASET} ...")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", KAGGLE_DATASET,
        "-p", DOWNLOAD_DIR
    ], check=True)

def unzip_dataset():
    """
    Unzip the downloaded dataset.
    """
    zip_path = os.path.join(DOWNLOAD_DIR, ZIP_FILE)
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found at {zip_path}")

    print(f"Unzipping: {zip_path} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)
    print("Unzipped successfully.")

def main():
    ensure_kaggle_json()
    download_dataset()
    unzip_dataset()
    print("✅ Dataset ready at:", os.path.abspath(DOWNLOAD_DIR))

if __name__ == "__main__":
    main()