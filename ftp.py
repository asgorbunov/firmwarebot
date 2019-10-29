from ftplib import FTP
import yaml
import datetime
import requests
import time

FW_FILE = 'firmware.yaml'
FTP_SERVER = 'ftp.infinetwireless.com'
URL = 'https://api.telegram.org/bot911229343:AAH3m3tdbeKlnzp5OV-JOZwM0ZPVZs_BHTo/'
CHAT = '193596632'
TXT = 'Братишка! Для семейста {} вышла новая {}-прошивка с номером {}'
SLEEPTIME = 30*60

def send_mess(chat, url, text):
	req = url + 'sendMessage?chat_id=' + chat + '&text=' + text
	return requests.post(req)

def ftp_fw_check(fw_path):
	ftp = FTP(FTP_SERVER)
	ftp.login()
	ftp.cwd(fw_path)

	ftp_fw_records = []
	ftp.retrlines('LIST',ftp_fw_records.append)
	return ftp_fw_records

def fw_version_check(fw_type, family, separator):
	fw_cur_date = datetime.datetime.strptime(
		fw_cur[fw_type][family]['date'],
		'%Y-%m-%d')

	ftp_fw = ftp_fw_check(fw_cur[fw_type][family]['path'])

	for fw in ftp_fw:
		_, _, _, _, _, month, day, year, filename = fw.split()

		if filename[-4:] == '.bin':
			if ':' in year:
				year = '2019'

			ftp_fw_date = datetime.datetime.strptime(
				year+'-'+month+'-'+day,
				'%Y-%b-%d')

			if ftp_fw_date.date() > fw_cur_date.date():
				print('New!')
				fw_cur[fw_type][family]['version'] = filename.split(separator)[1].split('.bin')[0]
				fw_cur[fw_type][family]['date'] = str(ftp_fw_date.date())

				txt = TXT.format(family, fw_type, fw_cur[fw_type][family]['version'])
				print(send_mess(CHAT, URL, txt))

i=0

while 1:
	with open(FW_FILE) as f:
		fw_cur = yaml.safe_load(f)

	for fw_type in list(fw_cur.keys()):
		for family in list(fw_cur[fw_type].keys()):
			fw_version_check(fw_type, family,
				fw_cur[fw_type][family]['separator'])

	with open(FW_FILE, 'w') as f:
		yaml.dump(fw_cur, f)

	print(i)
	i+=1
	time.sleep(SLEEPTIME)
