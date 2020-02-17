#!/usr/bin/env python3
# (c) 2018 Maximilian Siegl

import sys
import json
import os
import requests
from multiprocessing import Process

CONFIG_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "config.json")


def del_ip(ip_bin_path, ip, interface):
    os.system(ip_bin_path + " addr del " + ip + "/32 dev " + interface)


def add_ip(ip_bin_path, ip, interface):
    os.system(ip_bin_path + " addr add " + ip + "/32 dev " + interface)


def change_request(endstate, url, header, payload, ip_bin_path, floating_ip, interface):
    if endstate == "BACKUP":
        del_ip(ip_bin_path, floating_ip, interface)
    elif endstate == "FAULT":
        del_ip(ip_bin_path, floating_ip, interface)

    elif endstate == "MASTER":
        add_ip(ip_bin_path, floating_ip, interface)
        print("Post request to: " + url)
        print("Header: " + str(header))
        print("Data: " + str(payload))
        r = requests.post(url, data=payload, headers=header)
        print("Response:")
        print(r.status_code, r.reason)
        print(r.text)
    else:
        print("Error: Endstate not defined!")


def change_aliases(url, header, network_id, alias_ips):
    payload_raw = {
        "network": network_id,
        "alias_ips": alias_ips
    }
    payload = json.dumps(payload_raw)

    print("Post request to: " + url)
    print("Header: " + str(header))
    print("Data: " + str(payload))
    r = requests.post(url, data=payload, headers=header)
    print("Response:")
    print(r.status_code, r.reason)
    print(r.text)


def main(arg_type, arg_name, arg_endstate):
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)

    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + config["api-token"]
    }

    payload_floating_raw = {
        "server": config["server-id"]
    }
    payload_floating = json.dumps(payload_floating_raw)

    print("Perform action for transition to " + arg_endstate + " state")

    for ip in config["floating-ips"]:
        url = config["url-floating"].format(ip["floating-ip-id"])
        Process(target=change_request, args=(arg_endstate, url, header, payload_floating,
                                             config["ip-bin-path"], ip["floating-ip"], config["interface-wan"])).start()

    if config["use-private-ips"] == True:
        if arg_endstate == "MASTER":
            for server_id in config["server-ids"]:
                url = config["url-alias"].format(server_id)
                Process(change_aliases(
                    url, header, config["network-id"], []))

            url = config["url-alias"].format(config["server-id"])
            change_aliases(
                url, header, config["network-id"], config["private-ips"])

            for private_ip in config["private-ips"]:
                add_ip(config["ip-bin-path"], private_ip,
                       config["interface-private"])

        else:
            for private_ip in config["private-ips"]:
                del_ip(config["ip-bin-path"], private_ip,
                       config["interface-private"])


if __name__ == "__main__":
    main(arg_type=sys.argv[1], arg_name=sys.argv[2], arg_endstate=sys.argv[3])
