# coding: utf-8
from __future__ import absolute_import, unicode_literals


from django.conf import settings
from django.http import FileResponse
import os
from PIL import Image, ImageFont, ImageDraw
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_relative_media_url():
    return urlparse(settings.MEDIA_URL).path.strip('/')


def extract_relative_media_path(path):
    relative_media_url = get_relative_media_url()
    return path.replace(relative_media_url, '').strip('/')


def generate_image(width=300, height=300):
    if width < height:
        font_size = width / 7
    else:
        font_size = height / 7

    # text and image
    image_text = "{width} x {height}".format(width=width, height=height)
    path = "generated/{width}-{height}.png".format(width=width, height=height)
    image_name = os.path.join(settings.MEDIA_ROOT, path)
    image_dir = os.path.dirname(image_name)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # create image
    image_file = Image.new('RGBA', (width, height), color='rgb(220,220,220)')

    # create text
    draw = ImageDraw.Draw(image_file)
    # TODO: abstract font file path
    font_path = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf"
    fnt = ImageFont.truetype(font_path, font_size)
    w, h = draw.textsize(image_text, font=fnt)
    size = ((width - w) / 2, (height - h) / 2)
    draw.text(size, image_text, font=fnt, fill="black")

    # TODO: draw some borders

    # save image
    image_file.save(image_name, "PNG")

    with open(image_name, "rb") as f:
        return FileResponse(f, content_type="image/jpeg")



# from django.core.cache import cache
# from filer.fields.image import Image as ImageField
        # # TODO: abstract database check to a implementation of a `MediaSource` interface. Make it optional and configurable
        # image_field = ImageField.objects.filter(file=image_path).first()
        #
        # if image_field:
        #     return_image = cache.get("{width}-{height}".format(width=image_field._width, height=image_field._height))
        #     if not return_image:
        #         return_image = generate_image(image_field._width, image_field._height)
        #         cache.add("{width}-{height}".format(width=image_field._width, height=image_field._height), return_image)
        #
        # else:
        #     # TODO: abstract remote check to a implementation of a `MediaSource` interface. Make it optional
        #     try:

                # return_image = cache.get(path)
                # if not return_image:
                #     # TODO: refactor url path join
                #     image_url = settings.ALTERNATIVE_MEDIA_URL + image_path
                #     return_image = urllib2.urlopen(image_url)
                #     return_image = return_image.read()
                #     cache.add(path, return_image)

                # except urllib2.HTTPError as e:
                #     if e.code == 404:
                #         raise Http404("File not found.")
