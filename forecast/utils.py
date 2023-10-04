from datetime import datetime


def upload_to_today(instance, filename):
    # today = datetime.now().strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return f"uploads/{today}/{filename[:-4]}/{filename}"


def images_to_today(instance, folder_path, imagename):
    return f"{folder_path}/{imagename}"
