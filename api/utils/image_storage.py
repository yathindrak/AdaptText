from filestack import Client


class ImageStorage:
    def __init__(self):
        self.client = Client("A2BIWbSEXSUKDLgjKn6fgz")

    def upload(self, img_path):
        store_params = {
            "mimetype": "image/png"
        }
        img_url = self.client.upload(filepath=img_path, store_params=store_params)

        return img_url.url
