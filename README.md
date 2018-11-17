# Hetzner Cloud - Floating IP switchover - keepalived

This is a little script for switching over a Floating IP at Hetzner Cloud.  
Because of `multiprocessing` a switchover of multiple Floating IPs would run simultaniously.  
I am using this script in combination with [keepalived](http://www.keepalived.org).

**Credits:** [r3vival](https://github.com/r3vival) | [lehuizi](https://github.com/lehuizi)  
**License:** MIT


## How to

**1. Clone the repo**
```
git clone https://github.com/lehuizi/hcloud-failover-keepalived.git
```

**2. Install requirements**
```
apt install python3 python3-pip
pip3 install -r requirements.txt
```

**3. Copy config.json.sample to config.json**
```
cp config.json.sample config.json
```

**4. Fill config.json**

---

Command:  
```
python3 /path/to/hcloud_failover.py [type] [name] [endstate]
```
