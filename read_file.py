from ftplib import FTP
import re

ftp_address = 'ftp.infinetwireless.com'
ftp_path = '/pub/Firmware/MINT/readme.txt'
output_file = 'readme.en.txt'
regex = '\s~{19}\s([\s\S]+?)\s~{19}\s'


with FTP(ftp_address) as ftp:
	ftp.login()
	with open(output_file, 'wb') as f:
		ftp.retrbinary('RETR ' + ftp_path, f.write)

with open(output_file) as f:
	text = f.read()

match = re.search(regex, text)
print(match.group(1))
#print(text)
