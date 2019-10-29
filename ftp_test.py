from ftplib import FTP
import yaml
import datetime
import requests
import time

FW_FILE = 'firmware.yaml'
FW_TREE = ['stable', 'beta']
FTP_SERVER = 'ftp.infinetwireless.com'
URL = 'https://api.telegram.org/bot911229343:AAH3m3tdbeKlnzp5OV-JOZwM0ZPVZs_BHTo/'
CHAT = '193596632'
TXT = 'Братишка! Для семейста {} вышла новая {}-прошивка с номером {}'
SLEEPTIME = 30*60

def send_mess(url, chat, text):
	req = url + 'sendMessage?chat_id=' + chat + '&text=' + text
	return requests.post(req)

def get_updates(url):
	req = url + 'getUpdates'
	return requests.post(req).json()

def add_abonents(url, fw_struct):
	updates = get_updates(url)

	if updates['result']:
		abonents = set(fw_struct['abonents'])

	for message in updates['result']:
		abonents.add(str(message['message']['chat']['id']))

	fw_struct['abonents'] = list(abonents)

def ftp_fw_check(server_address, fw_struct):
	with FTP(server_address) as ftp:
		ftp.login()

		for tree in FW_TREE:
			for family in fw_struct[tree].keys():
				ftp.cwd(fw_struct[tree][family]['path'])
				print(fw_struct[tree][family]['path'])
				print(ftp.retrlines('LIST'))

with open(FW_FILE) as f:
	fw_cur = yaml.safe_load(f)

#Eto nado
#add_abonents(URL, fw_cur)

ftp_fw_check(FTP_SERVER, fw_cur)




with open(FW_FILE, 'w') as f:
	yaml.dump(fw_cur, f)


#abonents = set(fw_cur['abonents'])
#print(abonents)

#print(fw_cur)
#print(get_updates(URL)['result'][1]['message']['chat']['id'])

