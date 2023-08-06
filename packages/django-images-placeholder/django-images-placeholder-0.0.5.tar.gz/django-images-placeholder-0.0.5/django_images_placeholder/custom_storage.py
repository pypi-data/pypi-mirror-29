import urllib2
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.http import Http404


class OverwritingStorage(FileSystemStorage):
    """
    File storage that allows overwriting of stored files.
    """

    VALID_IMAGE_EXTENSIONS = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
    ]

    def valid_url_extension(self, url, extension_list=VALID_IMAGE_EXTENSIONS):
        for ext in extension_list:
            if url.endswith(ext):
                return ext
        return None

    def open(self, name, mode='rb'):
        """
        Retrieves the specified file from storage.
        """

        try:
            file_name = os.path.join(settings.MEDIA_ROOT, name)
            return self._open(file_name, mode)
        except:
            if self.valid_url_extension(name) is not None:
                try:
                    file_path = os.path.join(settings.ALTERNATIVE_MEDIA_URL, name)
                    img_file = urllib2.urlopen(file_path)

                except urllib2.HTTPError as e:
                    if e.code == 404 or e.code == 500:
                        return None

                try:
                    file_name = os.path.join(settings.MEDIA_ROOT, name)
                    dirname = os.path.dirname(file_name)

                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    with open(file_name, "wb") as new_image_file:
                        new_image_file.write(img_file.read())

                    return self._open(name, mode)

                except:
                    return None