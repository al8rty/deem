import os
import subprocess
import requests

def is_installed(pkg_name):
    try:
        subprocess.run(["dpkg", "-s", pkg_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(pkg_name):
    print(f"Install {pkg_name}...")
    os.system(f"apt install -y {pkg_name}")

def print_version(command, name):
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        print(f"{name} install: {result}")
    except subprocess.CalledProcessError:
        print(f"Error {name}!")

if not is_installed("docker.io"):
    install_package("docker.io")
else:
    print("Docker already installed.")

if not is_installed("docker-compose"):
    install_package("docker-compose")
else:
    print("Docker Compose already installed.")

print_version("docker --version", "Docker")
print_version("docker-compose --version", "Docker Compose")

home_dir = os.path.expanduser("~")
wiki_yml_path = os.path.join(home_dir, "wiki.yml")
wiki_url = "https://raw.githubusercontent.com/al8rty/wiki/main/wiki.yml"

print("Install wiki.yml...")
try:
    response = requests.get(wiki_url, timeout=10)
    response.raise_for_status()
    with open(wiki_yml_path, "w") as file:
        file.write(response.text)
    print("File wiki.yml successfuly install!")
except requests.RequestException as e:
    print(f"Error install wiki.yml: {e}")
    exit(1)

os.chdir(home_dir)
print("open wiki.yml ...")
os.system(f"docker-compose -f {wiki_yml_path} up -d")

print("Install is finished!")
