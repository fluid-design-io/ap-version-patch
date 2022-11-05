from boxsdk import Client, CCGAuth

auth = CCGAuth(
  client_id="egkrr2d915ry6y70i83vjopp0j310dr4",
  client_secret="rPViiMNUOZERGzm2Te4lancNcpWFMl4m",
  enterprise_id="956673804"
)

client = Client(auth)

me = client.user().get()
print(f'My user ID is {me.id}')

subfolder = client.folder('0').create_subfolder('AP Images')
print(f'Created subfolder with ID {subfolder.id}')

folder_id = subfolder.id
new_file = client.folder(folder_id).upload('test.txt')
print(f'File "{new_file.name}" uploaded to Box with file ID {new_file.id}')
file_id = new_file.id

url = client.file(file_id).get_shared_link(access='open', allow_download=True, allow_edit=True)
print(f'The file shared link URL is:')
print(url)
