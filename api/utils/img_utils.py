from io import BytesIO
from filestack import Client


class ImageUtils:
    def __init__(self):
        self.client = Client("A2BIWbSEXSUKDLgjKn6fgz")

    def upload(self, bin_content):
        img_url = self.client.upload(file_obj=BytesIO(bin_content))
        return img_url
