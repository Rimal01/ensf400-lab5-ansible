import ansible_runner
import yaml
import re


#Load Inventory
filePath = 'hosts.yml'
with open(filePath, 'r') as inventoryFile:
    inventory = yaml.safe_load(inventoryFile)


#Print: Names, IP Addresses, and Group Names
for group, info in inventory.items():
        if group == "ungrouped":
            continue
        print(f"Group: {group}")
        for host, details in info.get('hosts', {}).items():
            ip_address = details.get('ansible_host', 'Unknown')
            print(f"  Host: {host} ({ip_address})")


# Create an Ansible Runner object
result = ansible_runner.interface.run_command("ansible", [
    "-i", "./hosts.yml",
    "--private-key", "./secrets/id_rsa",
    "all:localhost",
    "-m", "ping"
])

output_tuple = result

# Extracting host names using regular expressions from the successful pings
pinged_hosts = re.findall(r'(?:managedhost-app-\d+|localhost) \| SUCCESS', output_tuple[0])

# Printing only the hosts that were successfully pinged
print("Pinged Hosts:")
for host in pinged_hosts:
    print(host)