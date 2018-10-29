#!/usr/bin/env python
# Written by Tchakatak

import subprocess
import optparse
import re
import random

#Parsing the user entry
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to apply")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address or RANDOM for a random mac")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default="false", help="Activate verbose mode")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
        exit(0)
    elif not options.new_mac:
        parser.error("[-] Please specify a mac address or autogen a random mac, use --help for more info.")
        exit(0)
    return options

#Generate the random numbers
def gen_hex(length):
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))

#Generate mac using gen_hex for each pair
def gen_00mac():
    generated = '00' + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2) + ":" + gen_hex(2)
    return generated

#Change mac to given arguments
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#Get current mac of the interface provided by user
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

#Grab arguments and get previous mac
options = get_arguments()

#Get the current mac used by selected interface
current_mac = get_current_mac(options.interface)
previous_mac = current_mac

if options.verbose == True :
    print("[+] Verbose On")

print("[+] Current MAC of" + str(options.interface) + " is " + str(current_mac))

#If user select RANDOM as argument for mac, generate a random mac
if options.new_mac == "RANDOM":
    #if options.verbose == "yes" :
    #

    print('[+] User selected RANDOM as an argument, Generating MAC')
    rand_mac = gen_00mac()
    options.new_mac = rand_mac
    print("[+] Random MAC Generated : " + str(options.new_mac))

#Change mac
change_mac(options.interface, options.new_mac)

#Get the current mac used by selected interface
current_mac = get_current_mac(options.interface)

#Check if the mac address was changed and print a message for the user
if current_mac != previous_mac:
    print("[+] MAC address was successfully changed to " + str(current_mac))
else:
    print("[-] MAC address did not get changed.")
