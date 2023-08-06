"""Utility functions for tvmaze"""

import requests
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class ApiError(Exception):
    """Error class for all api calls"""


def make_request(url):
    """Return JSON data from request or error

    :param url: Url to make get request
    :return: Return JSON data from request or error
    """
    r = requests.get(url)
    data = r.json()
    if r.status_code > 400:
        raise ApiError({"message": data['message'] if 'message' in data else 'Not found', "statusCode": r.status_code})
    return data


def get_list(obj, lst, url, make_class=None):
    """Helper function to get list of data"""
    attr = getattr(obj, lst)
    if attr:
        return attr
    try:
        if make_class:
            new_list = [make_class(**item) for item in make_request(url)]
        else:
            new_list = make_request(url)
    except ApiError as e:
        raise e
    else:
        setattr(obj, lst, new_list)
        return new_list


def json_to_init(url, item_name, file=None):
    item = requests.get(url).json()
    with open('{}{}empty_file.py'.format(dir_path, os.path.sep), 'w') as file:
        for key in item.keys():
            file.write('self.{key_name} = {item_key}["{key_name}"] \n'.format(key_name=key, item_key=item_name))
