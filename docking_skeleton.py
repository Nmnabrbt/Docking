import sys
import os
import platform
import subprocess
import shutil
import tempfile
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile
from tarfile import TarFile, open as taropen

def is_conda_available():
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def download_file(url, dst):
    print(f"Downloading {url} to {dst} ...")
    urlretrieve(url, dst)
    print("Download complete.")

def extract_archive(archive_path, extract_to):
    print(f"Extracting {archive_path} to {extract_to}")
    if archive_path.endswith(".zip"):
        with ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith((".tar.gz", ".tar", ".tgz")):
        with taropen(archive_path, "r:*") as tar_ref:
            tar_ref.extractall(path=extract_to)
    else:
        raise ValueError("Unsupported archive format")

def move_binaries(src_dir, dst_dir, binaries):
    os.makedirs(dst_dir, exist_ok=True)
    for binary in binaries:
        src_path = os.path.join(src_dir, binary)
        dst_path = os.path.join(dst_dir, binary)
        print(f"Moving {src_path} to {dst_path}")
        shutil.move(src_path, dst_path)
        if not platform.system().startswith("Windows"):
            os.chmod(dst_path, 0o755)

def install_autodock_macos():
    url = "https://autodock.scripps.edu/download-autodock4/autodocksuite-4.2.6-MacOSX.tar"
    tmp_dir = tempfile.mkdtemp()
    archive_path = os.path.join(tmp_dir, "autodock_mac.tar")
    download_file(url, archive_path)
    extract_dir = os.path.join(tmp_dir, "autodock_extracted")
    extract_archive(archive_path, extract_dir)
    # Binaries usually under MacOSX/
    src_bin_dir = os.path.join(extract_dir, "MacOSX")
    dst_bin_dir = "/usr/local/bin"  # Requires sudo, user may need to change
    move_binaries(src_bin_dir, dst_bin_dir, ["autodock4", "autogrid4"])
    print("AutoDock4 and AutoGrid4 installed to /usr/local/bin. You may need admin rights.")

def install_autodock_linux():
    url = "https://autodock.scripps.edu/download-autodock4/autodocksuite-4.2.6-Linux_x64.tar.gz"
    tmp_dir = tempfile.mkdtemp()
    archive_path = os.path.join(tmp_dir, "autodock_linux.tar.gz")
    download_file(url, archive_path)
    extract_dir = os.path.join(tmp_dir, "autodock_extracted")
    extract_archive(archive_path, extract_dir)
    src_bin_dir = extract_dir
    dst_bin_dir = "/usr/local/bin"
    binaries = ["autodock4", "autogrid4"]
    move_binaries(src_bin_dir, dst_bin_dir, binaries)
    print("AutoDock4 and AutoGrid4 installed to /usr/local/bin. You may need admin rights.")

def install_autodock_windows():
    print("AutoDock4 typical installation on Windows requires manual steps or use of pre-compiled binaries. Please install manually from:")
    print("https://autodock.scripps.edu/download-autodock4/")
    # Optionally open web page automatically
    import webbrowser
    webbrowser.open("https://autodock.scripps.edu/download-autodock4/")

def install_pymol_conda():
    print("Installing PyMOL via conda...")
    try:
        subprocess.run(["conda", "install", "-y", "-c", "schrodinger", "pymol"], check=True)
        print("PyMOL installed successfully via conda.")
    except Exception as e:
        print(f"Failed to install PyMOL via conda: {e}")

def install_pymol_pip():
    print("Installing PyMOL via pip. Note: This may be limited or experimental on some platforms.")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pymol"], check=True)
        print("PyMOL installed successfully via pip.")
    except Exception as e:
        print(f"Failed to install PyMOL via pip: {e}")

def main():
    system = platform.system()
    print(f"Detected OS: {system}")

    # Install AutoDock/AutoGrid
    if system == "Darwin":
        install_autodock_macos()
    elif system == "Linux":
        install_autodock_linux()
    elif system == "Windows":
        install_autodock_windows()
    else:
        print("Unsupported OS for automatic AutoDock installation")

    # Install PyMOL
    if is_conda_available():
        install_pymol_conda()
    else:
        install_pymol_pip()

if __name__ == "__main__":
    main()
