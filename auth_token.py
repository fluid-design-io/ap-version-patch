from boxsdk import Client, OAuth2

auth = OAuth2(
    client_id='sg16oqvkvgklcsgeq8wkzpvwu67pf4yc',
    client_secret='',
    access_token='Af21eR2XXVgR1gCPNOy670GJ22NCnQhE',
)
client = Client(auth)

me = client.user().get()
print(f'My user ID is {me.id}')

folder_id = '180672032035'
new_file = client.folder(folder_id).upload('test.txt')
print(f'File "{new_file.name}" uploaded to Box with file ID {new_file.id}')