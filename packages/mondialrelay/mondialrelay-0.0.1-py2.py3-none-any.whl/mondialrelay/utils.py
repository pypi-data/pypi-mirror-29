#This file is part of mondialrelay. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

MRELAY_VERSION = ['v1']
MRELAY_CULTURE = ['fr-FR']
MRELAY_LABEL_FORMAT = ['ZplCode', 'PdfUrl', 'IplCode']
MRELAY_PDF_FORMAT = ['A4', 'A5', '10x15']


def mondialrelay_url(debug=False):
    """
    MondialRelay URL connection

    :param debug: If set to true, use Envialia test URL
    """
    if debug:
        return 'http://Connect.API.Sandbox.mondialRelay.com/api/shipment'
    else:
        return 'https://connect-api.mondialrelay.com/api/shipment'


def services():
    return {
        # Collection
        'CCC': 'Merchant collection',
        'CDR': 'Home collection for the standard shipments',
        'CDS': 'Home collection for heavy or bulky shipments',
        'REL': 'Point Relais collection',
        # Delivery
        'LCC': 'Merchant delivery',
        'HOM': 'Home delivery',
        'HOC': 'Home delivery (specific for spain)',
        'LD1': 'Home delivery for standard shipments',
        'LDS': 'Home delivery for heavy or bulky shipments',
        '24R': 'Point Relais delivery',
        '24L': 'Point Relais XL delivery',
        '24X': 'Point Relais XXL delivery',
        '24C': 'Locker delivery',
        'DRI': 'Colisdrive delivery',
        }
