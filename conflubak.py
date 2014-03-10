#!/usr/bin/python3

import sys
import re
import argparse
import xmlrpc.client

# Argument parser
parser = argparse.ArgumentParser(description='Export a Confluence instance as XML.')

parser.add_argument('-s', '--server', type=str, required=True, 
                   help='URI of the XMLRPC server, e.g. http://confluence.example.com/rpc/xmlrpc')
parser.add_argument('-u', '--user', type=str, required=True, 
                   help='Confluence user; must have administrator permissions')
parser.add_argument('-p', '--password', type=str, required=True, )
parser.add_argument('-a', '--include-attachments', action='store_true',
                   help='Include attachments in backup')

args = parser.parse_args()


# Log in
sys.stderr.write("Connecting to " + args.server + " ...\n")
server = xmlrpc.client.ServerProxy(args.server)

try:
    token = server.confluence1.login(args.user, args.password)
except:
    sys.stderr.write("Login failed:" + sys.exc_info()[1] + "\n")
    sys.exit(1)
else:
    sys.stderr.write("Logged in. Starting export...\n")

# Request XML export
try:
    reply = server.confluence1.exportSite(token, False)
except:
    sys.stderr.write("Error creating backup:" + sys.exc_info()[1] + "\n")
    sys.exit(1)
else:
    path = re.search("/\S*\.zip", reply)
    
# Could the path be extracted?
if path is None:
    sys.stderr.write("Error parsing server reply.\n")
    sys.exit(1)
else:
    print(path.group(0))
