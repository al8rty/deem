import os
import subprocess
import sys
import paramiko
import time

HQ_IP = "172.16.4.2"
HQ_USER = "root"
HQ_PASSWORD = "Test123"

br_commands = [
    "sudo ip tunnel add gre-tun mode gre local 172.16.5.2 remote 172.16.4.2 ttl 255",
    "sudo ip addr add 10.0.0.2/30 dev gre-tun",
    "sudo ip link set gre-tun up"
]

hq_commands = [
    "sudo ip tunnel add gre-tun mode gre local 172.16.4.2 remote 172.16.5.2 ttl 255",
    "sudo ip addr add 10.0.0.1/30 dev gre-tun",
    "sudo ip link set gre-tun up"
]

def install_required_packages():
    print("\n Checking for the necessary packages...\n")

    if not shutil.which("python3"):
        print("Python3 don't founded, installing...")
        subprocess.run("sudo apt update && sudo apt install -y python3", shell=True)
    else:
        print("Python3 already installed")

    if not shutil.which("pip3"):
        print("pip don't founded, installing...")
        subprocess.run("sudo apt install -y python3-pip", shell=True)
    else:
        print("pip already installed")

    try:
        import paramiko
        print("paramiko already installed")
    except ImportError:
        print("paramiko don't founded, installing...")
        subprocess.run("pip3 install paramiko", shell=True)

def execute_local(commands):
    print("\n Setting GRE-tunn on br-rtr (local)...\n")
    for cmd in commands:
        print(f"DO: {cmd}")
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if process.returncode == 0:
            print("Successfully!")
        else:
            print(f"Error!: {process.stderr}")

def execute_remote(ip, username, password, commands):
    print("\n Connecting to HQ-RTR and setting GRE...\n")
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        for cmd in commands:
            print(f"DO on {ip}: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print("Output is:\n", output)
            if error:
                print("Error:\n", error)

        client.close()
        print("\n Setting HQ-RTR finished!")
    
    except Exception as e:
        print(f"\n Connection error to {ip}: {e}")

def check_gre_status():
    print("\n Testing GRE-tunn...\n")
    result = subprocess.run("ip addr show gre-tun", shell=True, capture_output=True, text=True)

    if "state UP" in result.stdout:
        print("Gre-tunn active!")
        return True
    else:
        print("GRE-tunn not active!")
        return False

def test_ping(target_ip):
    print(f"\n Testing connection to host: ping {target_ip}...\n")
    result = subprocess.run(f"ping -c 4 {target_ip}", shell=True, capture_output=True, text=True)

    if "0% packet loss" in result.stdout:
        print("Ping is successfully! GRE work normal!")
    else:
        print("Ping is didn't went! Check your settings.")

install_required_packages()

execute_local(br_commands)

execute_remote(HQ_IP, HQ_USER, HQ_PASSWORD, hq_commands)

time.sleep(5)

if check_gre_status():
    test_ping("10.0.0.1")

print("\n GRE-tunn is work well, you very well!\n")
