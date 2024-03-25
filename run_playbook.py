import ansible_runner
import requests


with open("./secrets/id_rsa", "r") as pKey:
    key = pKey.read()

# Run the hello.yml playbook 
runner = ansible_runner.run(
    private_data_dir='.',  
    playbook='hello.yml',  
    inventory= 'hosts.yml',
    ssh_key = key
)

 
# Verify the response
if runner.status == 'successful':
    print("The playbook was executed successfully")

    url_list = ("http://0.0.0.0:3000", "http://0.0.0.0:3001", "http://0.0.0.0:3002")
    for url in url_list:
        #Send get request to server
        response = requests.get(url)
        #Check response
        if response.status_code == 200:
            print(f"Server has successfully responded from {url}.")
        else:
            print(f"Failed to get a successful response from {url}. \nStatus Code: {response.status_code}")
else:
    print("The playbook was not executed successfully")