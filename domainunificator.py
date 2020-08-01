import sys
from urllib import parse
import re
import os

description='''\
	           _     _
	 ___ ___ _| |___| |_ _ _ ___ ___ ___
	|  _| . | . | -_| . | | |- _| -_|   |
	|___|___|___|___|___|_  |___|___|_|_|
	.    https://dsda.ru|___|           .
	|                                   |
	|desc: Unique domains list from file|
	+-----------------------------------+
'''

print(description)


if (len(sys.argv)==1):
	print('Usage: '+sys.argv[0]+' list.txt out.txt [scheme[0|1]] [path[0|1]]')
	print('       out.txt always appended'+"\n")
	print('       scheme (default 0) - https://sitename.tld and http://sitename.tld are equal'+"\n")
	print('       path (default 1) - sitename.tld/path1 and sitename.tld/path2 are euqal'+"\n")
	exit()


if (os.path.isdir(sys.argv[1])):
	domainslist = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]
	domainslistline = []
	for i in domainslist:
		try:
			domainslistline_f = open(i, 'r')
		except IOError:
			print("File "+sys.argv[1]+" not accessible!\n")
			exit()
		domainslistline += domainslistline_f.readlines()
		domainslistline_f.close()
else:
	try:
		domainslistline_f = open(sys.argv[1], 'r') 
	except IOError:
		print("File "+sys.argv[1]+" not accessible!\n")
		exit()
	domainslistline = domainslistline_f.readlines() 
	domainslistline_f.close()

print(str(len(domainslistline)) + ' Lines in memory!')

try:
	domainsout = open(sys.argv[2], 'w') 
except IOError:
	print("File "+sys.argv[2]+" not accessible!\n")
	exit()

if len(sys.argv)<3:
	print("Output file must be specify!\n")
	exit()

d_scheme = 0
if (len(sys.argv)>3 and (int(sys.argv[3])==1 or int(sys.argv[3])==0)):
	d_scheme = int(sys.argv[3])

if d_scheme==1:
	print(' - Ignore scheme!')

d_path = 1
if (len(sys.argv)>4 and (int(sys.argv[4])==1 or int(sys.argv[4])==0)):
	d_path = int(sys.argv[4])

if d_path==1:
	print(' - Ignore path!')


domains_unique = []
for u in domainslistline:
	url = u.strip()
	is_scheme = re.search('^http[s]?://', url)
	if (is_scheme is None):
		url = 'http://'+url
	
	url_parsed = parse.urlparse(url)
	url_combined = ''
	
	if (d_scheme==1):
		url_combined = url_parsed.netloc
	else:
		url_combined = url_parsed.scheme + '://' + url_parsed.netloc
	if (d_path==0):
		url_combined = url_combined + url_parsed.path
	
	url_combined = url_combined.strip('/')


	if (url_combined not in domains_unique):
		# print('Add: '+url_combined)
		domains_unique.append(url_combined)

for i in domains_unique:
	domainsout.write(i+"\n")
print(str(len(domains_unique)) + ' Lines in result list!')

print('> All done!')