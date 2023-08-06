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
from datetime import datetime


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoSpaceDataReaderAvailable(Error):
    """When no space data's reader is available to the given space api version

    Attributes:
         message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class StatusIcon:
    """Icons that show the status graphically

    Attributes:
    - opened_url (str): The URL to the customized space logo showing
      an open space
    - closed_url (str): The URL to the customized space logo showing
      an closed space
    """
    def __init__(self, opened_url='', closed_url=''):

        self.opened_url = opened_url
        self.closed_url = closed_url


class Status:
    """Status about the space

    Attributes:
    - is_open (bool): A flag which indicates if the space is currently
      open or closed
    - last_change (DateTime): The Unix timestamp when the space status
      changed most recently
    - trigger_person (str): The person who lastly changed the state
      (opened or closed the space, or changed the message)
    - message (str): An additional free-form string, could be something
      like 'open for public', 'members only' or whatever you want it to be
    - icon (space.StatusIcon): Icons that show the status graphically
    """
    def __init__(self, is_open=False, last_change=None, trigger_person='',
                 message='', icon=None):
        self.is_open = is_open
        self.last_change = last_change
        self.trigger_person = trigger_person
        self.message = message
        self.icon = icon


class Location:
    """Position data such as a postal address or geographic coordinates

    Attributes:
    - address (str): The postal address of the space
    - latitude (float): Latitude of the space location,
      in degree with decimal places
    - longitude (float): Longitude of the space location,
      in degree with decimal places
    """
    def __init__(self, address='', latitude=None, longitude=None):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class Contact:
    """Contact information about the space

    Attributes:
    - phone (str): hone number, including country code with a
      leading plus sign
    - sip (str): URL for Voice-over-IP via SIP
    - irc (str): URL of the IRC channel, in the
      form irc://example.org/#channelname
    - jabber (str): A public Jabber/XMPP multi-user chatroom
    - twitter (str): Twitter handle, with leading @
    - identica (str): Identi.ca or StatusNet account, in the form
      yourspace@example.org
    - mailing_list (str): The e-mail address of your mailing list
    - email (str): E-mail address for contacting your space
    - issue_email (str): A seperate email address for issue reports
    """
    def __init__(self, phone='', sip='', irc='', jabber='',
                 twitter='', identica='',
                 mailing_list='', email='', issue_email=''):
        self.phone = phone
        self.sip = sip
        self.irc = irc
        self.jabber = jabber
        self.twitter = twitter
        self.identica = identica
        self.mailing_list = mailing_list
        self.email = email
        self.issue_email = issue_email


class Space:
    """A hackerspaces, makerspaces, fablabs, chaostreffs and the like

    Attributes:
    - name (str): The name of the space
    - logo_url (str): URL to the space logo
    - website (str): URL to the space website
    - status (space.Status): Status about the space
    - location (space.Location): Position data such as a postal address or
      geographic coordinates
    - contact (space.Contact): Contact information about the space
    - data: List of all data get by space json
    """
    def __init__(self, name='', logo_url='', website_url='', status=None,
                 location=None, contact=None, data={}):
        self.name = name
        self.logo_url = logo_url
        self.website_url = website_url
        self.status = status
        self.location = location
        self.contact = contact
        self.data = data
        if self.data:
            self.__read_data()

    def __read_data(self):
        """Read space data and load it in object properties"""
        schema_version = self.data['api']
        if schema_version == '0.13':
            self.__read_data_v0_13()
        else:
            raise NoSpaceDataReaderAvailable(
                'no data reader is available to the given space api version'
            )

    def __read_data_v0_13(self):
        """Read space data and load it in object properties,
        with a  data schema's version 0.13
        """
        self.name = self.data.get('space')
        self.logo_url = self.data.get('logo')
        self.website_url = self.data.get('url')
        state_data = self.data.get('state')
        if state_data:
            self.status = Status(
                is_open=state_data.get('open'),
                last_change=datetime.fromtimestamp(
                    state_data.get('lastchange')
                ),
                trigger_person=state_data.get('trigger_person'),
                message=state_data.get('message'),
            )
            state_icon_data = state_data.get('icon')
            if state_icon_data:
                status_icon = StatusIcon(
                    opened_url=state_icon_data.get('open'),
                    closed_url=state_icon_data.get('closed'),
                )
                self.status.icon = status_icon
        location_data = self.data.get('location')
        if location_data:
            self.location = Location(
                address=location_data.get('address'),
                latitude=location_data.get('lat'),
                longitude=location_data.get('lon'),
            )
        contact_data = self.data.get('contact')
        self.contact = Contact(
            phone=contact_data.get('phone'),
            sip=contact_data.get('sip'),
            irc=contact_data.get('irc'),
            jabber=contact_data.get('jabber'),
            twitter=contact_data.get('twitter'),
            identica=contact_data.get('identica'),
            mailing_list=contact_data.get('ml'),
            email=contact_data.get('email'),
            issue_email=contact_data.get('issue_mail'),
        )
