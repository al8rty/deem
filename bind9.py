import os
import subprocess
import requests

def is_bind9_installed():
    try:
        subprocess.run(["dpkg", "-s", "bind9"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_bind9():
    if is_bind9_installed():
        print("bind9 is already installed.")
        return
    try: 
        print("Updating package list...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        print("Installing bind9...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "bind9"], check=True)
        
        print("bind9 installed successfully.")
    except subprocess.CalledProcessError as t:
        print(f"An error occurred during the installation process: {t}")
        exit(1)

def download_config(url, output_path):
    try:
        print(f"Downloading {output_path}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(output_path, 'w') as file:
            file.write(response.text)
        print(f"Downloaded {output_path}")
    except Exception as e:
        print(f"Error downloading {output_path}: {e}")
        exit(1)

def setup_zones():
    zones_dir = "/etc/bind/zones"
    
    if not os.path.exists(zones_dir):
        print(f"Creating directory: {zones_dir}")
        os.makedirs(zones_dir)
    
    zones_files = {
        "db.au-team.irpo": "https://raw.githubusercontent.com/al8rty/bind9/main/db.au-team.irpo",
        "db.192.168.2": "https://raw.githubusercontent.com/al8rty/bind9/main/db.192.168.2",
        "db.192.168.1": "https://raw.githubusercontent.com/al8rty/bind9/main/db.192.168.1",
        "db.172.16.4": "https://raw.githubusercontent.com/al8rty/bind9/main/db.172.16.4",
        "db.172.16.5": "https://raw.githubusercontent.com/al8rty/bind9/main/db.172.16.5",
        "db.172.16.10": "https://raw.githubusercontent.com/al8rty/bind9/main/db.172.16.10",
        "db.10.0.137": "https://raw.githubusercontent.com/al8rty/bind9/main/db.10.0.137"
    }
    
    for filename, url in zones_files.items():
        output_path = os.path.join(zones_dir, filename)
        download_config(url, output_path)

def confirm_bind9():
    if not is_bind9_installed():
        print("bind9 is not installed. Installing now...")
        install_bind9()
    
    config_files = {
        "/etc/bind/named.conf.local": "https://raw.githubusercontent.com/al8rty/bind9/main/named.conf.local",
        "/etc/bind/named.conf.options": "https://raw.githubusercontent.com/al8rty/bind9/main/named.conf.options"
    }
    
    for path, url in config_files.items():
        download_config(url, path)
    
    setup_zones()
    
    try:
        subprocess.run(["sudo", "systemctl", "restart", "bind9"], check=True)
        print("bind9 configured and restarted successfully.")
    except subprocess.CalledProcessError as g:
        print(f"Error restarting bind9: {g}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires superuser privileges. Please run as root or use sudo.")
    else:
        confirm_bind9()
