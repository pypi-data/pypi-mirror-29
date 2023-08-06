from __future__ import absolute_import, division, print_function, unicode_literals

from future import standard_library

standard_library.install_aliases()

from builtins import *

import re
from copy import copy

try:
    from typing import Optional
except ImportError:
    pass


import gepir.elements


class ReturnCodeError(Exception):

    code_value = -1  # type: int
    code_name = 'Return code error'  # type: str
    code_definition = ''  # type: str

    def __init__(
        self,
        envelope=None  # type: Optional[gepir.elements.Envelope]
    ):
        # type: (...) -> None
        super().__init__(
            '%s (return code %s): %s\n%s' % (
                self.code_name,
                str(self.code_value),
                self.code_definition,
                str(envelope)
            )
        )
        self.envelope = envelope


class NoDataReturned(ReturnCodeError):

    pass


class Unavailable(ReturnCodeError):

    pass


class Restricted(ReturnCodeError):

    pass


class InternalUseOnlyPrefix(Unavailable, NoDataReturned):

    pass


class MissingOrInvalidParameters(NoDataReturned):

    code_value = 1
    code_name = 'Missing or invalid parameters'
    code_definition = (
        'One or more parameters is missing or incorrect. This might be wrong length, invalid GS1 check digit, ' +
        'nonnumeric characters in a number, etc. No data is returned.'
    )


class RecordNotFound(Unavailable, NoDataReturned):

    code_value = 2
    code_name = 'Record not found'
    code_definition = (
        'No record exists in the MO database for this key or these search parameters. No data is returned.'
    )


class NoExactMatchOnRequestedKey(Unavailable):

    code_value = 3
    code_name = 'No exact match on Requested Key'
    code_definition = (
        'No record was found for this Requested Key. The data' +
        'held in the MO database for this company prefix is returned.'
    )


class TooManyHits(ReturnCodeError):

    code_value = 4
    code_name = 'Too many hits'
    code_definition = 'Over twenty records match the search criteria. Only twenty are returned.'


class UnknownGS1Prefix(Unavailable, NoDataReturned):

    code_value = 5
    code_name = 'Unknown GS1 Prefix'
    code_definition = 'The GS1 prefix (3 digit country code) does not exist.'


class IncompleteResponse(ReturnCodeError):

    code_value = 6
    code_name = 'Response may be incomplete'
    code_definition = (
        'One or more servers failed to respond for the global search (“zz”). ' +
        'Such data as is available is returned.'
    )


class RequestTimedOut(NoDataReturned):

    code_value = 7
    code_name = 'Request timed out'
    code_definition = 'There was a timeout somewhere in the server chain. No data is returned.'


class NoCatalogExists(NoDataReturned):

    code_value = 8
    code_name = 'No catalogue exists'
    code_definition = (
        'A request has been made for GTIN information, but there is no server for this company. No data is returned.'
    )


class CompanyInformationWithheld(Restricted, NoDataReturned):

    code_value = 9
    code_name = 'Company information withheld'
    code_definition = (
        'The company prefix in the request exists, but the company has not released its information for publication. ' +
        'The name and address of the responsible MO is returned.'
    )


class PrefixNoLongerSubscribed(Unavailable, NoDataReturned):

    code_value = 10
    code_name = 'Prefix no longer subscribed'
    code_definition = (
        'The company prefix in the request exists, but the company is no longer a member of GS1 under this ' +
        'prefix. The name and address of the responsible MO is returned.'
    )


class CountryNotInGEPIR(Unavailable, NoDataReturned):

    code_value = 11
    code_name = 'Country not on the GEPIR network'
    code_definition = (
        'There is no GEPIR MO server for this country. This should only be used with Get Party by Name.'
    )


class ItemInformationWithheld(Restricted, NoDataReturned):

    code_value = 12
    code_name = 'Item information withheld'
    code_definition = (
        'The GTIN in the request exists, but the company has not released its information for publication.'
    )


class UnauthorizedNumber(Restricted, NoDataReturned):

    code_value = 13
    code_name = 'Unauthorised number'
    code_definition = (
        'The company prefix in the request is known to be unauthorised. The name and address of the responsible MO ' +
        'is returned.'
    )


class DailyRequestLimitExceeded(NoDataReturned):

    code_value = 14
    code_name = 'Daily request limit exceeded'
    code_definition = (
        'The user has exceeded the number of ‘free’ requests permitted (30) and the request is rejected. No data is ' +
        'is returned. The ‘responderGln’ element is set by the node refusing the request.'
    )


class GLNNotAssigned(Unavailable, NoDataReturned):

    code_value = 15
    code_name = 'GS1 Key is valid; GLN not assigned'
    code_definition = 'GS1 Key is valid; GLN not assigned'


class InternalUseOnlyPrefix02Or04(InternalUseOnlyPrefix):

    code_value = 16
    code_name = 'Prefix 020-029 or 040-049 for internal use only'
    code_definition = (
        'Prefix 020-029 or 040-049 are for company internal use. No information can be returned. The name and ' +
        'address of the MO inquired is returned.'
    )


class InternalUseOnlyPrefix20(InternalUseOnlyPrefix):

    code_value = 17
    code_name = 'Prefix 200-299 for internal use only'
    code_definition = (
        'Prefix 200-299 is for company internal use. No information can be returned. The name and address of the MO ' +
        'inquired is returned.'
    )


class SerialPublicationPrefix(Unavailable, NoDataReturned):

    code_value = 18
    code_name = 'Prefix 977 (ISSN)'
    code_definition = (
        'Prefix 977 is used for serial publications (ISSN). No information can be returned. The name and address of ' +
        'the MO inquired is returned.'
    )


class BookPrefix(Unavailable, NoDataReturned):

    code_value = 19
    code_name = 'Prefix 978-979 (ISBN)'
    code_definition = (
        'Prefixes 978-979 are used for books (ISBN). No information can be returned. The name and address of the MO ' +
        'inquired is returned.'
    )


class CouponPrefix(Unavailable, NoDataReturned):

    code_value = 20
    code_name = 'Coupon Prefix'
    code_definition = (
        'Prefixes 050-059 and 990-999 are used for coupons. No information can be returned. The name and address ' +
        'of the MO inquired is returned.'
    )


class PrefixNeverAllocated(Unavailable, NoDataReturned):

    code_value = 21
    code_name = 'Prefix never allocated'
    code_definition = (
        'No record exists in the MO database for this key. No data is returned. This code can only be used when ' +
        'historical data is available.'
    )


class UnsupportedRequestForThisVersion(NoDataReturned):

    code_value = 97
    code_name = 'Unsupported request for this version.'
    code_definition = (
        'The request contains elements which cannot be processed by a GEPIR Router on this version.'
    )


class AuthorizationFailed(Restricted, NoDataReturned):

    code_value = 98
    code_name = 'Authorization failed'
    code_definition = 'The Authorization process has failed and access is not granted'


class ServerError(NoDataReturned):

    code_value = 99
    code_name = 'Server error'
    code_definition = (
        'Router is functional, however, there is no access to the data. The ‘responderGln’ element is ' +
        'set by the node detecting the error.'
    )


# A map of return codes to their corresponding exceptions

RETURN_CODES_EXCEPTIONS = {}

for k, v in copy(locals()).items():
    if (
        k[0] != '_' and
        isinstance(v, type) and
        hasattr(v, 'code_value') and
        hasattr(v, 'code_name') and
        hasattr(v, 'code_definition')
    ):
        code_value = getattr(v, 'code_value')  # type: int
        if code_value > 0:
            RETURN_CODES_EXCEPTIONS[str(code_value)] = v


class Fault(Exception):

    code = None

    def __init__(self, envelope, request=None):
        # type: (Envelope, Optional[Request]) -> None
        self.string = envelope.body.fault.fault_string
        self.actor = envelope.body.fault.fault_actor
        self.detail = envelope.body.fault.detail
        message = []
        if request is not None:
            s = str(request.data, encoding='utf-8')
            s = re.sub(
                r'(<(?:[^:>]*:)?mtomRef\b[^>]*>).*(</(?:[^:>]*:)?mtomRef\b[^>]*>)',
                r'\1...\2',
                s
            )
            message.append(
                'Request: \n' +
                ('    %s: %s\n        ' % (request.get_method(), request.full_url)) +
                '\n        '.join(
                    '%s: %s' % (k, v)
                    for k, v in request.header_items()
                ) + (
                    ('\n    ' + s)
                    if request.data is not None
                    else ''
                )
            )
        message.append(
            self.__class__.__name__.split('.')[-1] + ':\n' + '\n'.join((
                '    - Code: ' + (self.code or ''),
                '    - Actor: ' + (self.actor or ''),
                '    - String: ' + (
                    '' if self.string is None
                    else '\n      '.join(tuple(
                        self.string.split('\n')
                    ))
                ),
                '    - Detail: ' + (
                    '' if self.detail is None
                    else '\n      '.join(tuple(
                        self.detail.split('\n')
                    ))
                ),
                '',
                str(envelope)
            ))
        )
        super().__init__('\n\n'.join(message))



class VersionMismatchFault(Fault):

    code = 'VersionMismatch'


class MustUnderstandFault(Fault):

    code = 'MustUnderstand'


class ClientFault(Fault):

    code = 'Client'


class ServerFault(Fault):

    code = 'Server'


FAULT_CODES_ERRORS = dict(
    VersionMismatch=VersionMismatchFault,
    MustUnderstand=MustUnderstandFault,
    Client=ClientFault,
    Server=ServerFault
)