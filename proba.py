import requests

url = "https://api.telegram.org/bot911229343:AAH3m3tdbeKlnzp5OV-JOZwM0ZPVZs_BHTo/"

def get_updates_json(request):
	response = requests.get(request + 'getUpdates')
	return response.json()

def last_update(data):
	results = data['result']
	total_updates = len(results) - 1
	return results[total_updates]

def send_mess(chat, text):
	#params = {'chat-id': chat, 'text': text}
	response = requests.post(url + 'sendMessage?chat_id=' + str(chat) + '&text=' + text)
	return response

txt = 'Huetiki'

chat_id = last_update(get_updates_json(url))['message']['chat']['id']

#print(chat_id)
#print(last_update(get_updates_json(url)))

print(send_mess(chat_id, txt))
#print(get_updates_json(url))


#print("Hello, world!")
