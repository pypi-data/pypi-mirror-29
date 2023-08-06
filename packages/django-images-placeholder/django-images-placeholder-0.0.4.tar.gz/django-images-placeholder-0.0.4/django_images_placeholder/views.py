import urllib2

from django.conf import settings
from django.http import Http404, FileResponse
# TODO: Move this dependency to an isolated module, where a builtin
# `MediaSource` for `filer` will be implemented
import logging
import os

from .utils import extract_relative_media_path


logger = logging.getLogger(__name__)


def serve_image_placeholder(request):
    path = request.path_info
    media_path = extract_relative_media_path(path)

    # TODO: Create mechanism to check `MediaSource`s instead os this bunch of
    # `if`s and `try`s
    try:
        fpath = os.path.join(settings.MEDIA_ROOT, media_path)
        return FileResponse(open(fpath, 'rb'), content_type='image/jpeg')
    except IOError:
        logger.info('File not found on local file system.')

        try:
            response = urllib2.urlopen(settings.ALTERNATIVE_MEDIA_URL + media_path)
        except urllib2.HTTPError as e:
            if e.code == 404 or e.code == 500:
                raise Http404('File not found.')
        try:
            file_name = os.path.join(settings.MEDIA_ROOT, media_path)
            dirname = os.path.dirname(file_name)
            content = response.read()

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(file_name, 'wb') as new_image_file:
                new_image_file.write(content)
            return FileResponse(open(file_name, 'rb'), content_type='image/jpeg')
        except Exception as e:
            logger.exception(e)

    raise Http404("File not found.")
