# Hetzner Cloud - Floating IP and Private IP switchover - keepalived

This is a little script for switching the assigned VM of Floating IPs. It's also possible to modify assigned Alias IPs to also use the private networks feature of Hetzner Cloud.

I am using this script in combination with [keepalived](http://www.keepalived.org). It is tested on Debian based Systems.

**Credits:** [r3vival](https://github.com/r3vival) | [lehuizi](https://github.com/lehuizi)  
**License:** MIT


## How to

**1. Clone the repo** 
```
apt install git
git clone https://github.com/lehuizi/hcloud-failover-keepalived.git /opt/hcloud-failover
```

**2. Install requirements**  
```
apt install python3 python3-pip keepalived
pip3 install -r /opt/hcloud-failover/requirements.txt
```

**3. Copy config.json.sample to config.json**  
```
cd /opt/hcloud-failover
cp config.json.sample config.json
```

**4. Generate API Key in Hetzner Cloud Console**  
1. Login to Hetzner Cloud Console
2. Click on your project, choose "Access" in the left menu bar and switch to "API-Tokens"
3. Click on "Create API Token" and give it a description (eg. Keepalived Failover) 
4. Copy the key and insert it into the `/opt/hcloud-failover/config.json` file (on all servers)

**5. Fill in the server id**  
It is important, that you insert the server id of the current system you are working on. You can find the id on the overview page of each server directly under the type of the server (eg. CX11).

**6. Configure the floating ips**  
You can configure as much floating ips as you want. Just copy the floating ip id from the hcloud command line utility (personally I don't know a way to fetch the ip from the webinterface). 

`hcloud floating-ip list`  

Now also add the ip address to the config file and remove the additional block from the sample config file if you don't need it.

**7. Fill in the remaining parameters**  
1. The wan interface is the interface name of the primary interface of the server you are currently working on (eg. `ens18` or `eth0`)

**8. Configure private ip failover (optional)**  
1. If you also want to failover private ip addresses, fill in the required private ips into the "private-ips" array and make sure the "use-private-ips" parameter is set to `true`. Initially you should configure the required ip addresses via webinterface on one of the servers.
2. Now you have to insert **all** server id's into the array called "server-ids".
3. Now you have to insert the id of your private network into "network-id". You can fetch this through the url of the webinterface (by clicking on the private network and copying the last id in the url or you copy the id from the hcloud command line interface `hcloud network list`.
4. Finally fill in the name of your private network interface (eg. `eth10`)

---

Command:  
```
python3 /path/to/hcloud_failover.py [type] [name] [endstate]
```
