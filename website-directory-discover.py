#!/usr/bin/python

try:

	import sys
	import requests
	import socket
	import ssl

	#Display a summary of the tool to the user

	def splash():
		print "\n"
		print("This tool will check for subdirectories at the specified domain \n\n")
		print("Usage: \n python website-directory-discover.py rhost subdomainlist \n (e.g. python website-directory-discover.py urltocheck.com /home/path/to/directorylist)")
		print "\n\n"
		
	splash()

	#Tests the validity of the URL provided by the user.  Might like to prompt the user for this stuff in the future, and maybe include a 'default' option for common subdomains, and the option to use a user-supplied wordlist

	rhost = sys.argv[1]
	domainlist = sys.argv[2]

	print '[*] Checking RHOST... ',
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	wrappedsocket = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_OPTIONAL, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True)
#	try:
#		status = wrappedsocket.connect_ex((rhost, 443))
#		wrappedsocket.close()
#		if status == 0:
#			print '[DONE]'
#			pass
#		else:
#			print '[FAIL]'
#			print '[!] Error: Cannot Reach RHOST %s\n' %(rhost)
#			sys.exit(1)
#	except socket.error:
#		print '[FAIL]'
#		print '[!] Error: Cannot Reach RHOST: %s\n' %(rhost)
#		sys.exit(1)

	#End of URL validity checker 

	#Read the specified wordlist

	print '[*] Parsing domainlist... ',
	try:
		with open(domainlist) as file:
			to_check = file.read() .strip() .split('\n')
		print '[DONE]'
		print '[*] Total Paths to Check: %s' %(str(len(to_check)))
	except IOError:
		print '[FAIL]'
		print '[!] Error: Failed to read specified file.  Check path and permissions\n'
		sys.exit(1)

	#End read wordlist section

	#Path checking function

	def checkpath(path):
		try:
			response = requests.get('https://' + rhost + '/' + path + '/').status_code
		except Exception:
			print '[!] Error: An unexpected error occured'
			sys.exit(1)		
		if response == 200:
			print '[*] Valid path found: /%s' %(path)		



	#End path checking function

	#Iterate over the list of paths
	#Might need to change indentation here

	print '\n[*] Beginning Scan... \n'
	for i in range(len(to_check)):
		checkpath(to_check[i])
	print '\n[*] Scan Complete!'
except KeyboardInterrupt:
	print '\n[!] Error: User interrupted scan'
	sys.exit(1)
	



