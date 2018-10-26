#!/usr/bin/env python
# Written by Tchakatak

import subprocess
import optparse
import re
import random


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to apply")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address or RANDOM for a random mac")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
        exit(0)
    elif not options.new_mac:
        parser.error("[-] Please specify a mac address or autogen a random mac, use --help for more info.")
        exit(0)
    return options


def gen_hex(length):
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def gen_00mac():
    generated = '00' + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2)
    return generated


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
previous_mac = current_mac

print("[+] Current MAC of" + str(options.interface) + " is " + str(current_mac))

if options.new_mac == "RANDOM":
    rand_mac = gen_00mac()
    options.new_mac = rand_mac
    print("[+] Random MAC specified : " + str(options.new_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac != previous_mac:
    print("[+] MAC address was successfully changed to " + str(current_mac))
else:
    print("[-] MAC address did not get changed.")
