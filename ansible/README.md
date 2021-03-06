# Hello
## Start
#### Config
- inventory.yml : Add Kibana public IP
- ssh.cfg : Add Kibana public IP
#### Run 
- ansible -i inventory.yml -m ping all -u administrateur
- ansible-playbook -i inventory.yml ./playbooks/...
## Todo
