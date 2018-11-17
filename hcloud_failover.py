#!/usr/bin/env python3
# (c) 2018 Maximilian Siegl

import sys
import json
import os
import requests
from multiprocessing import Process

CONFIG_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "config.json")


def del_ip(ip_bin_path, floating_ip, interface):
    os.system(ip_bin_path + " addr del " + floating_ip + " dev " + interface)


def add_ip(ip_bin_path, floating_ip, interface):
    os.system(ip_bin_path + " addr add " + floating_ip + " dev " + interface)


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


def main(arg_type, arg_name, arg_endstate):
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)

    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + config["api-token"]
    }

    payload = '''{"server": ''' + str(config["server-id"]) + "}"

    print("Perform action for transition to " + arg_endstate + " state")

    for ips in config["ips"]:
        url = config["url"].format(ips["floating-ip-id"])
        Process(target=change_request, args=(arg_endstate, url, header, payload,
                                             config["ip_bin_path"], ips["floating-ip"], config["interface"])).start()


if __name__ == "__main__":
    main(arg_type=sys.argv[1], arg_name=sys.argv[2], arg_endstate=sys.argv[3])
