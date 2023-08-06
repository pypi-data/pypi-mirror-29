#This file is part of mondialrelay. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from mondialrelay.api import API
from xml.dom.minidom import parseString
import os
import urllib2
from genshi import template

loader = template.TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'template'),
    auto_reload=True)


class Picking(API):
    """
    Picking API
    """
    __slots__ = ()

    def create(self, data):
        """
        Create delivery to MondialRelay

        :param data: Dict
        :return: reference (str), label(base64), error (str)
        """
        reference = None
        label = None
        errors = []

        tmpl = loader.load('%s_picking_send.xml' % self.version)

        vals = {
            'username': self.username,
            'password': self.password,
            'customerid': self.customerid,
            'culture': self.culture,
            'output_type': self.output_type,
            'output_format': self.output_format,
            'OrderNo': data.get('OrderNo', ''),
            'CustomerNo': data.get('CustomerNo', ''),
            'ParcelCount': data.get('ParcelCount', '1'),
            'DeliveryMode': data.get('DeliveryMode', '24R'),
            'DeliveryLocation': data.get('DeliveryLocation', ''),
            'CollectionMode': data.get('CollectionMode', 'CCC'),
            'CollectionLocation': data.get('CollectionLocation', ''),
            'ParcelContent': data.get('ParcelContent', ''),
            'Weight': data.get('Weight', '100'),
            'WeightUnit': data.get('WeightUnit', 'gr'),
            'DeliveryInstruction': data.get('DeliveryInstruction', ''),
            'SenderTitle': data.get('SenderTitle', ''),
            'SenderFirstname': data.get('SenderFirstname', ''),
            'SenderLastname': data.get('SenderLastname', ''),
            'SenderStreetname': data.get('SenderStreetname', ''),
            'SenderHouseNo': data.get('SenderHouseNo', ''),
            'SenderCountryCode': data.get('SenderCountryCode', ''),
            'SenderPostCode': data.get('SenderPostCode', ''),
            'SenderCity': data.get('SenderCity', ''),
            'SenderAddressAdd1': data.get('SenderAddressAdd1', ''),
            'SenderAddressAdd2': data.get('SenderAddressAdd2', ''),
            'SenderAddressAdd3': data.get('SenderAddressAdd3', ''),
            'SenderPhoneNo': data.get('SenderPhoneNo', ''),
            'SenderMobileNo': data.get('SenderMobileNo', ''),
            'SenderEmail': data.get('SenderEmail', ''),
            'RecipientTitle': data.get('RecipientTitle', ''),
            'RecipientFirstname': data.get('RecipientFirstname', ''),
            'RecipientLastname': data.get('RecipientLastname', ''),
            'RecipientStreetname': data.get('RecipientStreetname', ''),
            'RecipientHouseNo': data.get('RecipientHouseNo', ''),
            'RecipientCountryCode': data.get('RecipientCountryCode', ''),
            'RecipientPostCode': data.get('RecipientPostCode', ''),
            'RecipientCity': data.get('RecipientCity', ''),
            'RecipientAddressAdd1': data.get('RecipientAddressAdd1', ''),
            'RecipientAddressAdd2': data.get('RecipientAddressAdd2', ''),
            'RecipientAddressAdd3': data.get('RecipientAddressAdd3', ''),
            'RecipientPhoneNo': data.get('RecipientPhoneNo', ''),
            'RecipientMobileNo': data.get('RecipientMobileNo', ''),
            'RecipientEmail': data.get('RecipientEmail', ''),
            }

        xml = tmpl.generate(**vals).render()
        result = self.connect(xml)
        if not result:
            return reference, label, None

        dom = parseString(result)
        for status in dom.getElementsByTagName('Status'):
            code = status.attributes['Code'].value
            if code == '0':
                shipment, = dom.getElementsByTagName('Shipment')
                reference = shipment.attributes['ShipmentNumber'].value

                output, = dom.getElementsByTagName('Output')
                output = output.firstChild.data

                if self.output_type == 'PdfUrl':
                    pdfuri = output.replace('&amp;', '&')
                    response = urllib2.urlopen(pdfuri, timeout=self.timeout)
                    label = response.read()
                else:
                    label = output
            else:
                level = status.attributes['Level'].value
                code = status.attributes['Code'].value
                message = status.attributes['Message'].value
                errors.append('%s %s %s' % (level, code, message))

        return reference, label, '\n'.join(errors)

    def label(self, data):
        """
        Get PDF label from MondialRelay service

        :param data: Dictionary of values
        :return: label
        """
        # TODO
        pass
