from ftplib import FTP
import yaml
import datetime
import requests
import time
import re

FW_FILE = 'firmware.yaml'
CHANGELOG_FILE = 'changelog.txt'
FW_TREE = ['stable', 'beta']
FTP_SERVER = 'ftp.infinetwireless.com'
URL = 'https://api.telegram.org/bot911229343:AAH3m3tdbeKlnzp5OV-JOZwM0ZPVZs_BHTo/'
CHAT = '193596632'
TXT = 'Братик, вышла новая прошивка!\n  - ветка: {}\n  - семейство: {}\n  - версия: {}\n  - дата: {}\n' + 9*'~' + '\nChangelog:\n{}'
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


def read_changelog(ftp_con, file_path, output_file, version):
	regex = version + '\s([\s\S]+?)\s~{19}\s'

	with open(output_file, 'wb') as f:
		ftp_con.retrbinary('RETR ' + file_path, f.write)

	with open(output_file) as f:
		text = f.read()

	match = re.search(regex, text)
	changelog_text = '\n'.join(match.group(1).split('\n')[1:-1])

	return changelog_text

def ver_check(family, version_str):
	if family == 'xg' or family == 'octopus':
		return version_str
	elif family == 'mint':
		ver = version_str[0] + '.' + version_str[1:]
		return ver
	elif family == 'tdma':
		ver = version_str[0] + '.' + version_str[2:]
		return ver

def ftp_fw_list(server_address, fw_struct):
	with FTP(server_address) as ftp:
		ftp.login()

		for tree in FW_TREE:
			for family in fw_struct[tree].keys():
				ftp.cwd(fw_struct[tree][family]['path'])
				ftp_dir_list = []
				ftp.retrlines('LIST', ftp_dir_list.append)
				fw_check(ftp_dir_list, fw_struct, tree, family, ftp)

def fw_check(file_list, fw_struct, tree, family, ftp_con):
	for file in file_list:
		if '.bin' in file:
			_, _, _, _, _, month, day, year, filename = file.split()

			if ':' in year:
				year = '2019'

			file_date = datetime.datetime.strptime(
				year + '-' + month + '-' + day,
				'%Y-%b-%d')
			fw_ideal_date = datetime.datetime.strptime(
				fw_struct[tree][family]['date'],
				'%Y-%m-%d')

			if file_date.date() > fw_ideal_date.date():
				print('New!')

				fw_struct[tree][family]['version'] = filename.split(fw_struct[tree][family]['separator'])[1].split('.bin')[0]
				fw_struct[tree][family]['date'] = str(file_date.date())

				if tree == 'stable':
					ver = ver_check(family, fw_struct[tree][family]['version'])
					changelog = read_changelog(ftp_con, fw_struct[tree][family]['changelog'], CHANGELOG_FILE, ver)

				notification = TXT.format(tree, family, fw_struct[tree][family]['version'], str(file_date.date()), changelog)

				for abonent in fw_struct['abonents']:
					print(send_mess(URL, abonent, notification))

				break

i = 0
while 1:
	with open(FW_FILE) as f:
		fw_cur = yaml.safe_load(f)

	add_abonents(URL, fw_cur)

	ftp_fw_list(FTP_SERVER, fw_cur)

	with open(FW_FILE, 'w') as f:
		yaml.dump(fw_cur, f)

	print(i)
	i+=1
	time.sleep(SLEEPTIME)
