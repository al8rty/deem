import os
import subprocess

def is_installed(package):
    result = subprocess.run(["dpkg", "-l", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def install_package(package):
    os.system(f"apt install -y {package}")

def get_version(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def main():
    if not is_installed("docker.io"):
        print("Install Docker...")
        install_package("docker.io")
    docker_version = get_version(["docker", "--version"])
    print(f"\033[91m{docker_version}\033[0m")

    if not is_installed("docker-compose"):
        print("Install Docker Compose...")
        install_package("docker-compose")
    compose_version = get_version(["docker-compose", "--version"])
    print(f"\033[91m{compose_version}\033[0m")

    print("Create volume dbvolume...")
    os.system("docker volume create --name=dbvolume")

    wiki_file = os.path.expanduser("~/wiki.yml")
    os.system(f"wget -O {wiki_file} https://raw.githubusercontent.com/al8rty/wiki/main/wiki.yml")

    print("Start container...")
    os.chdir(os.path.expanduser("~"))
    os.system("docker-compose -f wiki.yml up -d")

if __name__ == "__main__":
    main()
