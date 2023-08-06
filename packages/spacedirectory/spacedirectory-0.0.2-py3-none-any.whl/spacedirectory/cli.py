#!/usr/bin/env python3
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
import sys
from pprint import pprint
import argparse
from colors import color

from spacedirectory import directory, description, space, tools


def print_infos(space_required='', print_json=False):
    """Print infos of the given space

    Parameters:
    - space_required (space.Space): The space required by the user
    - print_json (bool): Print his json
    """
    if print_json:
        pprint(space_required.data)
        return

    # Print name and website
    print('')
    print(color(space_required.name, style='bold'))
    print(color('='*len(space_required.name), style='bold'))
    if space_required.website_url:
        print(color('Website:', style='bold'),
              space_required.website_url)
        print('')

    # Print status
    if space_required.status:
        status = space_required.status
        print(color('Status', style='bold+underline'))
        if status.is_open:
            open_message = (color('Open', 'green'))
        else:
            open_message = (color('Close', 'red'))
        print(color('The space is:', style='bold'),
              open_message)
        if status.message:
            print(color('Message:', style='bold'),
                  status.message)
        if status.last_change:
            print(color('Last change:', style='bold'),
                  status.last_change.strftime('%Y-%m-%d %a %H:%M'))
        if status.trigger_person:
            print(color('Changed by:', style='bold'),
                  status.trigger_person)
        print('')

    # Print location
    if space_required.location:
        location = space_required.location
        print(color('Location', style='bold+underline'))
        if location.address:
            print(color('Address:', style='bold'),
                  location.address)
        if location.longitude is not None or location.latitude is not None:
            latitude_hemishere = 'N' if location.latitude > 0 else 'S'
            longitude_hemisphere = 'E' if location.longitude > 0 else 'W'
            print(color('Geographic coord.:', style='bold'),
                  "lat. {0:.6f} {1}".format(
                      location.latitude,
                      latitude_hemishere
                  ),
                  '/',
                  "lon. {0:.6f} {1}".format(
                      location.longitude,
                      longitude_hemisphere
                  ))
        print('')

    # Print contact
    if space_required.contact:
        contact = space_required.contact
        print(color('Contact', style='bold+underline'))
        if contact.phone:
            print(color('Phone:', style='bold'),
                  contact.phone)
        if contact.sip:
            print(color('SIP:', style='bold'),
                  contact.sip)
        if contact.irc:
            print(color('IRC:', style='bold'),
                  contact.irc)
        if contact.jabber:
            print(color('Jabber MUC:', style='bold'),
                  contact.jabber)
        if contact.twitter:
            print(color('Twitter:', style='bold'),
                  contact.twitter)
        if contact.identica:
            print(color('Identica/StatusNet/Mastodon:', style='bold'),
                  contact.identica)
        if contact.mailing_list:
            print(color('Mailing list:', style='bold'),
                  contact.mailing_list)
        if contact.email:
            print(color('Email:', style='bold'),
                  contact.email)
        if contact.issue_email:
            print(color('Issue email:', style='bold'),
                  contact.issue_email)
        print('')


def print_spaces_list():
    """Print the list of spaces"""
    for space_name in directory.get_spaces_list().keys():
        print(space_name)


def main():
    """Function called by the command line tool
    Parse the command line arguments and do what arguments request"""
    # Create a parser and config it
    argument_parser = argparse.ArgumentParser(
        description=description,
    )
    argument_parser.add_argument(
        '-l',
        '--list-spaces',
        action="store_true",
        help='Get only the list of spaces (default action)',
    )
    argument_parser.add_argument(
        '-a',
        '--api',
        dest="api_url",
        help='Get infos of the given space api',
    )
    argument_parser.add_argument(
        'space_name',
        nargs='?',
        default=None,
        help='Get infos of the given space name',
    )
    argument_parser.add_argument(
        '-j',
        '--json',
        action="store_true",
        help='Get a dump of an asked space infos in JSON',
    )

    # Parse the command line arguments
    arguments = argument_parser.parse_args()

    # and do what arguments request
    if arguments.list_spaces:
        print_spaces_list()
        return
    elif arguments.space_name:
        try:
            space_required = directory.get_space_from_name(
                arguments.space_name
            )
        except directory.SpaceNotExist as error:
            sys.stderr.write(error.message+'\n')
            raise SystemExit(1)
        print_infos(space_required=space_required, print_json=arguments.json)
    elif arguments.api_url:
        space_data = tools.get_json_data_from_url(arguments.api_url)
        space_required = space.Space(data=space_data)
        print_infos(space_required=space_required, print_json=arguments.json)
    else:
        print_spaces_list()


if __name__ == '__main__':
    main()
