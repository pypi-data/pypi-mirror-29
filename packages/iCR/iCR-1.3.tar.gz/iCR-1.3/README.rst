iCR
===

This is a python module to simplify using iControl REST.

Install using pip:

``pip install iCR``

As simple as:

#!/usr/bin/env python
from iCR import iCR
bigip = iCR("172.24.9.132","admin","admin")
virtuals = bigip.get("ltm/virtual")
for vs in virtuals['items']:
  print vs['name']
This prints out a list of Virtual Servers.

Supported methods:

init(hostname,username,password,[timeout,port,icontrol_version,folder,token,debug])
get(url,[select,top,skip]) -> returns data or False
create(url,data) -> returns data or False
modify(url,data,[patch=True]) -> returns data or False
delete(url) -> returns True or False
upload(file) -> file is a local file eg /var/tmp/test.txt, returns True or False
download(file) -> files are located in /shared/images, returns True or False
create_cert(files) -> files is an array containing paths to cert and key. Returns name of cert or False
create_ssl_profile(name,cert,key) -> name is the name of the profile, cert and key are cert and key objects. Returns name of profile or False
get_asm_id(name) -> name is the name of a policy. Returns an array of IDs or False

Module Variables:

icr_session - the link to the requests session
raw - the raw returned JSON
code - the returned HTTP Status Code eg 200
error - in the case of error, the exception error string
headers - the response headers
icontrol_version - set this to specify a specific version of iControl
debug - boolean True or False to set debugging on or off
port - set the port ( 443 by default )
folder - set this to create in a specific partition
token - use this to set a specific iWorkflow token
select - use this with get to select the returned data
top - use this with get to return a set number of records
skip - use this to skip to a specific record number

----

Examples
========

#Create a Virtual Server
vs_config = {'name':'test_vs'}
createvs = bigip.create("ltm/virtual",vs_config,timeout=5)

# Retrieve the VS we just created
virt = bigip.get("ltm/virtual/test_vs",select="name")
print "Virtual Server created: " + virt['name']

# set the timeout
bigip.timeout = 20

# Now delete the VS we just created
delvs = bigip.delete("ltm/virtual/test_vs")

# Retrieve ASM policy to ID mapping
policies = bigip.get("asm/policies",select="name,id")
# Print  a table of ASM policies with learning mode
print
print "Policy Name                  Learning Mode"
print "------------------------------------------"
for item in policies['items']:
    enabled = bigip.get("asm/policies/" + item['id'] + "/policy-builder",select="learningMode")
    print '{:32}'.format(item['name']) + enabled['learningMode']

# file upload
fp = "/home/pwhite/input.csv"
if bigip.upload(fp):
  print "File " + fp + " uploaded"

# File download
file="BIGIP-12.1.2.0.0.249.iso"
download = bigip.download(file)
if not download:
  print "File " + file + " download error"

# SSL Certificate creation
# In different folder
bigip.folder = "TestFolder"
files = ("TestCert.crt","TestCert.key")
cert = bigip.create_cert(files)
if cert:
  print "Certificate " + cert + " created" 

# Turn on debugging
bigip.debug = True

# SSL profile creation
profile = bigip.create_ssl_profile("TestProfile",files[0],files[1])

# Retrieve ASM policy IDs
asm = bigip.get_asm_id("dummy_policy")
print len(asm) + " IDs returned"
print "ID: " + str(asm[0])
