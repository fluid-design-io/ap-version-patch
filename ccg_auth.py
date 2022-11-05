from boxsdk import Client, CCGAuth
from yaspin import yaspin
from upload_file import upload_file_to_box

auth = CCGAuth(
  client_id="egkrr2d915ry6y70i83vjopp0j310dr4",
  client_secret="rPViiMNUOZERGzm2Te4lancNcpWFMl4m",
  enterprise_id="956673804"
)

client = Client(auth)

me = client.user().get()

if not me:
  print("Unable to authenticate user")
  exit(1)

# subfolder = client.folder('0').create_subfolder('AP Images')
# print(f'Created subfolder with ID {subfolder.id}')

folder_id = '180673298837'

file_id = upload_file_to_box(client, folder_id, 'test.txt')
    
with yaspin(text="Creating sharing link", color="yellow") as spinner:
    url = client.file(file_id).get_shared_link(access='open', allow_download=True, allow_edit=True)
    spinner.text = ""
    spinner.color = "green"
    spinner.ok(f"You can view the file via: {url}")
