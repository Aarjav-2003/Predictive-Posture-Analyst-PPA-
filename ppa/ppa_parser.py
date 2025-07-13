import os
import re
import json

DATA_DIR = "collected_data"

def read_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"[!] Missing: {filename}")
        return ""
    with open(path, "r") as f:
        return f.read()

# ---------- 1. Network Interfaces ----------
def parse_network_interfaces():
    raw = read_file("network_interfaces.txt")
    interfaces = []
    current_interface = None

    for line in raw.splitlines():
        if re.match(r"\d+: \w+", line):
            if current_interface:
                interfaces.append(current_interface)
            current_interface = {"name": line.split(":")[1].strip(), "details": []}
        elif current_interface:
            current_interface["details"].append(line.strip())

    if current_interface:
        interfaces.append(current_interface)

    return interfaces

# ---------- 2. Open Ports ----------
def parse_open_ports():
    raw = read_file("open_ports.txt")
    ports = []
    for line in raw.splitlines():
        if re.search(r"(tcp|udp).*LISTEN", line):
            ports.append(line.strip())
    return ports

# ---------- 3. Users (passwd) ----------
def parse_passwd():
    raw = read_file("passwd_file.txt")
    users = []
    for line in raw.splitlines():
        parts = line.split(":")
        if len(parts) >= 1:
            users.append({
                "username": parts[0],
                "uid": parts[2] if len(parts) > 2 else None,
                "home": parts[5] if len(parts) > 5 else None,
                "shell": parts[6] if len(parts) > 6 else None
            })
    return users

# ---------- 4. Sudo Privileges ----------
def parse_sudo_privileges():
    raw = read_file("sudo_privileges.txt")
    return raw.strip().splitlines()

# ---------- 5. SSH Config ----------
def parse_sshd_config():
    raw = read_file("sshd_config")
    config = {}
    for line in raw.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split()
            if len(parts) >= 2:
                config[parts[0]] = " ".join(parts[1:])
    return config

# ---------- 6. Groups ----------
def parse_groups():
    raw = read_file("group_file.txt")
    groups = {}
    for line in raw.splitlines():
        parts = line.split(":")
        if len(parts) >= 4:
            group_name = parts[0]
            members = parts[3].split(",") if parts[3] else []
            groups[group_name] = members
    return groups

# ---------- 7. Running Processes ----------
def parse_running_processes():
    raw = read_file("running_processes.txt")
    processes = []
    for line in raw.splitlines()[1:]:  # Skip header
        parts = line.split()
        if len(parts) > 10:
            processes.append({
                "user": parts[0],
                "pid": parts[1],
                "cpu": parts[2],
                "mem": parts[3],
                "command": " ".join(parts[10:])
            })
    return processes

# ---------- 8. Services ----------
def parse_service_status():
    raw = read_file("service_status_all.txt")
    services = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("[ + ]") or line.startswith("+"):
            service = line.split()[-1]
            services.append(service)
    return services

# ---------- 9. Crontab ----------
def parse_cronjobs():
    raw = read_file("user_crontab.txt")
    return raw.strip().splitlines()

# ---------- 10. Firewall Rules ----------
def parse_firewall_rules():
    raw = read_file("iptables_rules.txt")
    return raw.strip().splitlines()

# ---------- Main ----------
def main():
    structured_data = {
        "network_interfaces": parse_network_interfaces(),
        "open_ports": parse_open_ports(),
        "users": parse_passwd(),
        "groups": parse_groups(),
        "sudo_privileges": parse_sudo_privileges(),
        "running_processes": parse_running_processes(),
        "services": parse_service_status(),
        "cronjobs": parse_cronjobs(),
        "firewall_rules": parse_firewall_rules(),
        "sshd_config": parse_sshd_config(),
    }

    print(json.dumps(structured_data, indent=4))

    # Save to file
    with open("normalized_output.json", "w") as f:
        json.dump(structured_data, f, indent=4)
        print("\n[+] Structured data saved to normalized_output.json")


if __name__ == "__main__":
    main()
