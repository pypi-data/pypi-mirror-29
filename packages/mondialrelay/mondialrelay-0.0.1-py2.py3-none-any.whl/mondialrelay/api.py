#This file is part of mondialrelay. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from mondialrelay.utils import mondialrelay_url
import urllib2
import os
import socket
from genshi import template

loader = template.TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'template'),
    auto_reload=True)


class API(object):
    """
    Generic API to connect to mondialrelay
    """
    __slots__ = (
        'url',
        'username',
        'password',
        'customerid',
        'culture',
        'output_type',
        'output_format',
        'version',
        'timeout',
        )

    def __init__(self, username, password, customerid, culture='fr-FR',
            output_type='PdfUrl', output_format='A5', version='v1',
            timeout=None, debug=False):
        """
        This is the Base API class which other APIs have to subclass. By
        default the inherited classes also get the properties of this
        class which will allow the use of the API with the `with` statement

        Example usage ::

            from mondialrelay.api import API

            with API(username, password, customerid) as mondialrelay_api:
                return mondialrelay_api.test_connection()

        :param username: MondialRelay API username
        :param password: MondialRelay API password
        :param customerid: MondialRelay API CustomerID
        :param culture: Language. Default, fr-FR
        :param output_type: ZplCode, PdfUrl or IplCode. Default PdfUrl
        :param output_format: A4, A5 or 10x15. Default A5
        :param version: API version
        :param timeout: int number of seconds to lost connection
        :param debug: bool debug mode
        """
        self.url = mondialrelay_url(debug)
        self.username = username
        self.password = password
        self.customerid = customerid
        self.culture = culture
        self.output_type = output_type
        self.output_format = output_format
        self.version = version
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def connect(self, xml):
        """
        Connect to the Webservices and return XML data from mondialrelay
        :param xml: XML data.
        Return XML object
        """
        headers = {
            'Content-Type': 'application/soap+xml; charset=utf-8',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(xml),
            }
        try:
            request = urllib2.Request(self.url, xml, headers)
            response = urllib2.urlopen(request, timeout=self.timeout)
            return response.read()
        except socket.timeout as err:
            return
        except socket.error as err:
            return

    def test_connection(self):
        """
        Test connection to MondialRelay webservices
        Send XML to MondialRelay and return error send data
        """
        return 'MondialRelay test is not available'
