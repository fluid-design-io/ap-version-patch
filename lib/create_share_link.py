from boxsdk import Client
from yaspin import yaspin


def create_share_link(client: Client, file_id, spinner):
    spinner.text = 'Creating sharing link'
    url = client.file(file_id).get_shared_link(
        access='open', allow_download=True, allow_edit=True)
    spinner.text = ""
    spinner.color = "green"
    spinner.ok(f"You can view the file via: {url}")
