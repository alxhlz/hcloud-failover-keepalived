# How to configure keepalived

## 1. Install keepalived  
```
apt install keepalived
```

## 2. Configure keepalived  
Copy the following config to `/etc/keepalived/keepalived.conf` and change it to fit your needs.

```
vrrp_instance LB_1 {
    state MASTER
    interface eth0
    virtual_router_id 1
    priority 100

    unicast_src_ip 1.1.1.1
    unicast_peer {
        1.1.1.2
    }

    authentication {
        auth_type PASS
        auth_pass imasupersecurepassword
    }

    notify "/bin/sudo /opt/hcloud-failover/hcloud_failover.py"
}
```

On the second (and all other servers) change:  
* the name of the vrrp instance (LB_1)
* the state (to BACKUP)
* the virtual_router_id to something unique
* the priority to something that matches your needs
* the unicast_src_ip to the ip of the local system
* the unicast_peer array to the ip addresses of all other systems

## 3. Create a service user
```
adduser keepalived_script
```

## 4. Install and configure sudo
```
apt install sudo
vim /etc/sudoers.d/90-keepalived
```

```
keepalived_script ALL=NOPASSWD: /bin/ip*, /opt/hcloud-failover/hcloud_failover.py*
```

## 5. Make sure keepalived is enabled and started
```
systemctl enable keepalived --now
```

## 6. Done
Enjoy :)
