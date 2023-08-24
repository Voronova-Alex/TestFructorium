import urllib.request
from urllib.parse import urlparse

import requests
from celery import shared_task
from django.core.files import File
from opengraph import opengraph
from bs4 import BeautifulSoup

from apps.bookmark.models.bookmark import Bookmark
from apps.image.models import Image


def get_info(validated_data):
    data_json = opengraph.OpenGraph(url=validated_data["url"])
    list_types = [i for i in Bookmark.UrlTypes.values]
    if "title" in data_json and "description" in data_json and "type" in data_json:
        validated_data["title"] = data_json["title"][:50]
        validated_data["description"] = data_json["description"]
        if data_json["type"] in list_types:
            validated_data["type_url"] = data_json["type"]
        else:
            validated_data["type_url"] = Bookmark.UrlTypes.WEBSITE
        if "image" in data_json:
            image = Image()
            name = urlparse(data_json["image"]).path.split("/")[-1]
            content = urllib.request.urlretrieve(data_json["image"])
            url = content[0]
            image.img.save(name, File(open(url, "rb")), save=True)
            validated_data["image"] = image
    elif "title" not in data_json and "description" not in data_json:
        data = requests.get(validated_data["url"])
        soup = BeautifulSoup(data.text, features="html.parser")
        titles = soup.find_all("title")
        meta_descriptions = soup.find_all("meta description")
        validated_data["type_url"] = Bookmark.UrlTypes.WEBSITE
        if titles:
            validated_data["title"] = ". ".join([title.get_text() for title in titles])[
                :50
            ]
        if meta_descriptions:
            validated_data["description"] = ". ".join(
                [meta_description.get_text() for meta_description in meta_descriptions]
            )
    return validated_data
