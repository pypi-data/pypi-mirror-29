# Copyright (C) 2018  Sébastien Gendre

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from spacedirectory import space, tools


DIRECTORY_JSON_URL = 'https://spaceapi.fixme.ch/directory.json'


# Error class
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SpaceNotExist(Error):
    """When a space not exist on the directory

    Attributes:
         message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class SpaceApiNotExist(Error):
    """When a json url not exist on the directory for a given space name

    Attributes:
         message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class NoSpaceData(Error):
    """When no space data is available to build a space.Space object

    Attributes:
         message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


# Module functions
def get_spaces_list():
    """
    Return the list of spaces as a dictionary:
    - Keys are spaces names
    - Values are corresponding space json url
    """
    return tools.get_json_data_from_url(DIRECTORY_JSON_URL)


def get_space_from_data(space_data=None):
    "Return a space.Space object from the space data given"
    if not space_data:
        raise NoSpaceData(
            'no space data available to build a space.Space object'
        )
    else:
        return space.Space(data=space_data)


def get_space_from_name(space_name=''):
    "Return a space.Space object from the space name given"
    spaces_list = get_spaces_list()
    if space_name not in spaces_list.keys():
        raise SpaceNotExist('Space asked does not exist on the directory')
    space_json_url = spaces_list.get(space_name)
    if not space_json_url:
        raise SpaceApiNotExist(
            'Json url for asked space does not exist on the directory'
        )
    else:
        data = tools.get_json_data_from_url(space_json_url)
        return get_space_from_data(data)
