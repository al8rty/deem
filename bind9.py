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
        print("Downloading configuration file...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(output_path, 'w') as file:
            file.write(response.text)
        print(f"Configuration file downloaded to {output_path}")
    
    except Exception as E:
        print(f"Error downloading configuration file: {E}")
        exit(1)

def setup_zones():
    zones_dir = "/etc/bind/zones"

    if not os.path.exists(zones_dir):
        print(f"Creating directory: {zones_dir}")
        os.makedirs(zones_dir)

        zones_file = {
            "db.au-team.irpo": "https://raw.githubusercontent.com/al8rty/bind9/main/db.au-team.irpo",
            "db.192.0.2": "https://raw.githubusercontent.com/al8rty/bind9/main/db.192.0.2"
        }

        for filename, url in zones_file.items():
            output_path = os.path.join(zones_dir, filename)
            download_config(url, output_path)

def confirm_bind9():
    if not is_bind9_installed():
        print("bind9 is not installed. Installing now...")
        install_bind9()

    config_url = "https://raw.githubusercontent.com/al8rty/bind9/main/named.conf.local"
    config_path = "/etc/bind/named.conf.local"

    download_config(config_url, config_path)

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

