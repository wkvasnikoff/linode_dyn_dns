#!/usr/bin/env python
import urllib2, urllib, json

def request(params):
    url = "https://api.linode.com/"
    params = urllib.urlencode(params)
    response = urllib2.urlopen(url, params)
    obj = json.load(response, encoding="utf-8")
    return obj

def load_config():
    f = open("config.json", "r")
    config = json.load(f, encoding="utf-8")
    f.close()
    return config

def main():
    config = load_config()

    api_key = config["api_key"]
    domains = config["domains"]

    post = {
        "api_key": api_key,
        "api_action": "domain.list"
    }

    domain_id_list = [];

    # ****** get the domain_ids ********
    obj = request(post)

    for item in obj["DATA"]:
        if item["DOMAIN"] in domains:
            domain_id_list.append(item["DOMAINID"])

    # ****** get the ip address *******
    url_get_ip = "http://icanhazip.com"
    response = urllib2.urlopen(url_get_ip)
    ip = response.read()

    # ***** get resource ******
    for domain_id in domain_id_list:
        # find the A records
        post = {
            "api_key": api_key,
            "api_action": "domain.resource.list",
            "DomainID": domain_id,
        }
        obj = request(post)

        for item in obj["DATA"]:
            if item["TYPE"] != "A":
                continue

            resource_id = item["RESOURCEID"]

            # update the A record to IP
            update_post = {
                "api_key": api_key,
                "api_action": "domain.resource.update",
                "DomainID": domain_id,
                "ResourceID": resource_id,
                "Target": ip,
            }
            output = request(update_post)

main()
