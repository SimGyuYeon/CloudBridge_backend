from datetime import datetime


def upload_to_today(instance, filename):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"uploads/{today}/{filename[:-4]}/{filename}"


def images_to_today(instance, folder_path, imagename):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{folder_path}/{imagename}"
