from boxsdk import Client

# Source: https://stackoverflow.com/questions/16800055/box-v2-api-for-overwriting-a-file-or-checking-one-exists-before-trying-to-upload


def upload_file_to_box(client: Client, folder_id, filename, spinner):
    try:
        folder = client.folder(folder_id=folder_id)
        items = folder.get_items()
    except Exception as e:
        spinner.fail(f"Error: {e}")
        return
    for item in items:
        if item.name == filename:
            updated_file = client.file(item.id).update_contents(item.name)
            spinner.color = "green"
            spinner.text = ""
            spinner.ok('✅ File "{0}" has been updated'.format(
                updated_file.name))
            return updated_file.id
    try:
        uploaded_file = folder.upload(filename)
    except Exception as e:
        spinner.fail(f"Error: {e}")
        return
    spinner.color = "green"
    spinner.text = ""
    spinner.ok('✅ File "{0}" has been uploaded'.format(uploaded_file.name))
    return uploaded_file.id
