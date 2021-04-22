from filestack import Client


class ImageStorage:
    """Manage images"""
    def __init__(self):
        self.__client = Client("A2BIWbSEXSUKDLgjKn6fgz")

    def upload(self, img_path):
        """
        Upload image to FileStack
        :param img_path: image path
        :type img_path: str
        :return: hosted url
        :rtype: str
        """
        store_params = {
            "mimetype": "image/png"
        }
        img_url = self.__client.upload(filepath=img_path, store_params=store_params)

        return img_url.url
