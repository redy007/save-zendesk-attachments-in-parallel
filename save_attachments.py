import requests, json, sys, os, shutil, asyncio, concurrent.futures
#!/usr/bin/python3

class Dbvisit:

	def is_standby(ticket):
		dropbox_folder_base='E:\\save\\files'
		zd_login='zd_login'
		zd_password='zd_password'
		company = 'CHANGE';
		tag_param = 'find_your_tag'
		ticket_url= 'https://' + company  + '.zendesk.com/api/v2/tickets/' + str(ticket) + '/'
		headers = {
		    'content-type': 'application/json',
		}

		params = (
		    ('priority', 'normal'),
		)
		r=requests.get(ticket_url, headers=headers, params=params, auth=(zd_login, zd_password))
		#r.raise_for_status()
		
		if r.status_code != 404:
			json_data = json.loads(r.text)
			tags=json_data["ticket"]["tags"]
			for tag in tags:
				if tag == tag_param:
					with open("standby_tickets_list_n.txt", "a", encoding='utf-8') as myfile:
						myfile.write(str(ticket) + '\n')
					ticket_url='https://' + company  + '.zendesk.com/api/v2/tickets/' + str(ticket) + '/comments.json'
					r=requests.get(ticket_url, headers=headers, params=params, auth=(zd_login, zd_password))
					r.raise_for_status()
					json_data = json.loads(r.text)
					#json_string = json.dumps(json_data,indent=4)
					attachments=json_data["comments"]
					for attachment in attachments:
						if attachment["attachments"] != []:
							for file in attachment["attachments"]:
								dropbox_folder=os.path.join(dropbox_folder_base,str(ticket))
								if not os.path.isdir(dropbox_folder):
									os.makedirs(dropbox_folder)
								url=file["content_url"]
								file_name=os.path.join(dropbox_folder,file["file_name"])
								if not os.path.isfile(file_name):
									print("Downloading from: ",url)
									print("Saving to file: ", file_name)
									response = requests.get(url, stream=True, auth=(zd_login, zd_password))
									response.raise_for_status()
									with open(file_name, 'wb') as handle:
										shutil.copyfileobj(response.raw, handle)
										#for block in response.iter_content(1024*1024):
										#	handle.write(block)
								else:
									print("File {file} already exists".format(file=file_name))

if __name__ == "__main__":
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		#future_to_url = {executor.submit(Dbvisit.is_standby, x): x for x in range(11275, 12000)}
		future_to_url = {executor.submit(Dbvisit.is_standby, x): x for x in range(12101, 13085)}