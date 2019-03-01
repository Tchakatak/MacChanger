#!/usr/bin/env python2

import subprocess
import optparse
import re
import random


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface")
    parser.add_option("-m", "--mac", dest="new_mac",
                      help="Set your new mac,\
                      leave it for a random generated mac")
    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose", default="false",
                      help="Activate verbose mode")
    parser.add_option("-l", "--legacy", action="store_true", default="false",
                      dest="legacy",
                      help="Legacy, use old ifconfig instead of ip")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(
            "[-] Please specify an interface -i [INTERFACE],\
             use --help for more info.")
        exit(0)
    elif not options.new_mac:
        parser.error(
            "[-] Please specify a mac address or autogen a random mac using -m\
            option, use --help for more info.")
        exit(0)
    return options


def gen_hex(length):  # Generate the random numbers

    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def gen_00mac():  # Generate mac using gen_hex for each pair
    generated = '00' + ":" + \
        gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2) + \
        ":" + gen_hex(2) + ":" + gen_hex(2)
    return generated


def change_mac(interface, new_mac):  # Change mac (ip)
    print("[+] Changing MAC address for "
          + interface + " to " + new_mac + " using ip")
    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", interface, "up"])


def change_mac_legacy(interface, new_mac):  # Change mac (ifconfig)
    print("[+] Changing MAC address for " + interface
          + " to " + new_mac + " using ifconfig")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface, legacy):  # Get mac from the origine iface
    if legacy is True:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
    else:
        ifconfig_result = subprocess.check_output(
            ["ip", "link", "show", interface])

    mac_address_search_result = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface, options.legacy)
previous_mac = current_mac

if options.verbose is True:
    print("[+] Verbose On")

print("[+] Current MAC of" + str(options.interface) + " is\
    " + str(current_mac))

if options.new_mac == "RANDOM":  # Random Mac Gen

    print('[+] User selected RANDOM as an argument, Generating MAC')
    rand_mac = gen_00mac()
    options.new_mac = rand_mac
    print("[+] Random MAC Generated : " + str(options.new_mac))

if options.legacy is True:  # Change Mac
    change_mac_legacy(options.interface, options.new_mac)
else:
    change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface, options.legacy)

if current_mac != previous_mac:
    print("[+] MAC address was successfully changed to " + str(current_mac))
else:
    print("[-] MAC address did not get changed.")
