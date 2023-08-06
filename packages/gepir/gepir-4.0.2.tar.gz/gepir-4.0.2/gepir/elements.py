from __future__ import absolute_import, division, print_function, unicode_literals

from future import standard_library

standard_library.install_aliases()

from builtins import *

import re
from base64 import b64decode, b64encode
from collections import OrderedDict
from decimal import Decimal, InvalidOperation
from itertools import chain
from xml.etree.ElementTree import XML, Element, tostring, ParseError

from datetime import datetime, date

try:
    from typing import Sequence, Union, Optional, List
except ImportError:
    pass

from copy import deepcopy

from gepir.errors import RETURN_CODES_EXCEPTIONS


class UnknownAttribute(Warning):

    pass


class UnknownValue(Warning):

    pass


NAME_SPACES = dict(
    gepir='http://gepir4.ws.gs1.org/',
    soap='http://www.w3.org/2003/05/soap-envelope',
)


_DATE_OFFSET_RE = re.compile(r'([\-+]\d\d):?(\d\d)$')
_DATE_DECIMAL_RE = re.compile(r'(\.\d\d\d\d\d\d)\d+')


def str2datetime(s):
    # type: (str) -> datetime
    """
    Convert an XML *dateTime* string to a python *datetime* object.

    >>> print(str2datetime('2001-10-26T21:32:52+02:00'))
    2001-10-26 21:32:52+02:00

    >>> print(str2datetime('2016-03-28T23:33:41.3116627-0500'))
    2016-03-28 23:33:41.311662-05:00
    """
    dtf = "%Y-%m-%d"
    if 'T' in s:
        dtf += "T%H:%M:%S"
        if '.' in s:
            dtf += '.%f'
            s = _DATE_DECIMAL_RE.sub(
                r'\1',
                s
            )
    if s[-1] in 'Zz':
        s = s[:-1]
    if _DATE_OFFSET_RE.search(s):
        dtf += "%z"
        s = _DATE_OFFSET_RE.sub(
            r'\1\2',
            s
        )
    return datetime.strptime(
        s,
        dtf
    )


def str2date(s):
    # type: (str) -> date
    """
    Convert an XML *date* string to a python *date* object.

    >>> print(str2date('2001-10-26'))
    2001-10-26
    """
    d = str2datetime(s)
    return date(
        year=d.year,
        month=d.month,
        day=d.day
    )


def datetime2str(dt):
    # type: (datetime) -> str
    s = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return s


def date2str(d):
    # type: (date) -> str
    s = d.strftime('%Y-%m-%d')
    return s


TYPES_BASES = OrderedDict()


def bases(t):
    # type: (type) -> Set[type]
    """
    Retrieves a set containing all classes (`type` instances) from which the given class inherits.

        :param t: An instance type.

        :return: A set containing all types from which this type inherits (directly and indirectly).
    """
    if t not in TYPES_BASES:
        bs = set()
        for b in t.__bases__:
            for bb in bases(b):  # type: Set[type]
                bs.add(bb)
            bs.add(b)
        TYPES_BASES[t] = bs
    return TYPES_BASES[t]


def space_name(s):
    # type: (str) -> str
    """
    This function returns the un-qualified name of an XML element or attribute.

    :param s:
        An tag or attribute name.
    :return:
        The unqualified name of the XML element or attribute.
    :rtype:
        str
    """
    return re.match(
        r'^(?:\{(.*?)\})?(.*)$',
        s
    ).groups()


class SOAPElement(object):

    """
    This is a base class for building objects to represent SOAP XML elements.

    Child classes should each have the following properties:

        elements_properties:

            This should be an `OrderedDict` object which maps sub-element XML tag names (not including a name space) to
            a tuple containing the corresponding property name + type.

        xmlns:

            The full URL of the element's default name space.

    Child classes should initialize each of the properties from their static `elements_properties` property in their
    `__init__` method with a value of `None` (for properties corresponding to elements which can occur only once) or an
    empty list (for properties which correspond to elements which can occur more than once).
    """

    elements_properties = OrderedDict([])  # type: Dict[str, Sequence[str, type]]

    xmlns = None

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str, HTTPResponse]],
        tag=None  # type: Optional[str]
    ):
        # type: (...) -> None
        """
        Initializes a `SOAPElement` instance, optionally deriving property values from provided XML data.

        :param xml:

            (optional) An instance of `str` or `xml.etree.ElementTree.Element` which represents an XML element, or an
            ``HTTPResponse`` object containing the same information.
            If provided, the tag name of the given element will override the `tag` parameter below.

        :param tag:

            (optional) The tag name of the element (not including the name space). This is needed only if no
            `xml` is provided.
        """
        self._string = None
        self._element = None
        self.response = None
        self.tag = tag or self.__class__.__name__
        if xml is not None:
            namespace = None
            if isinstance(xml, str):
                self._string = xml
                try:
                    self._element = XML(xml)
                except ParseError as e:
                    e.args = tuple(chain(
                        (
                            ((e.args[0] + '\n\n') if e.args else '') +
                            xml
                        ),
                        e.args[1:] if e.args and len(e.args) > 1 else tuple()
                    ))
                    raise e
                namespace, self.tag = space_name(self._element.tag)
            elif isinstance(xml, Element):
                self._element = xml
                namespace, self.tag = space_name(self._element.tag)
            elif hasattr(xml, 'read'):
                self.response = xml
                self._string = str(xml.read(), 'utf-8', errors='ignore')
                try:
                    self._element = XML(self._string)
                except ParseError as e:
                    e.args = tuple(chain(e.args, (self._string,)))
                    raise e
                namespace, self.tag = space_name(self._element.tag)
            else:
                raise TypeError(xml)
            if self.elements_properties is not None:
                namespaces_prefixes = {}
                for a, p_t in self.elements_properties.items():
                    if a[:7] == '@xmlns:':
                        prefix = a[7:]
                        p, t = p_t
                        v = getattr(self, p)
                        if v is not None:
                            namespaces_prefixes[prefix] = v
                            if v == namespace:
                                self.tag = '%s:%s' % (prefix, self.tag)
                tags_elements_properties_types = []
                for a, v in self._element.attrib.items():
                    a_ns, a = space_name(a)
                    if a_ns in namespaces_prefixes:
                        nsp_a = '%s:%s' % (namespaces_prefixes[a_ns], a)
                        if nsp_a in self.elements_properties:
                            a = nsp_a
                    tn = '@' + a
                    if tn in self.elements_properties:
                        p, t = self.elements_properties[tn]
                        tags_elements_properties_types.append((tn, v, p, t))
                    else:
                        raise UnknownAttribute('`%s` is not a recognized attribute of `%s`' % (
                            a,
                            self.__class__.__name__
                        ))
                v = self._element.text
                if v:
                    if '.' in self.elements_properties:
                        p, t = self.elements_properties['.']
                        tags_elements_properties_types.append(
                            ('.', v, p, t)
                        )
                    elif v.strip():
                        raise UnknownAttribute(
                            'No mapping was found for the text content of a `%s` element.' % self.tag
                        )
                for element in self._element:
                    ns, tn = space_name(element.tag)
                    if tn in self.elements_properties:
                        p, t = self.elements_properties[tn]
                        tags_elements_properties_types.append((tn, element, p, t))
                    else:
                        success = True
                        for e_a, e_v in element.attrib.items():
                            ns_a, e_a = space_name(e_a)
                            tn_a = '%s@%s' % (tn, e_a)
                            if tn_a in self.elements_properties:
                                p, t = self.elements_properties[tn_a]
                                tags_elements_properties_types.append((tn_a, e_v, p, t))
                            else:
                                success = False
                                break
                        for sub_element in element:
                            se_ns, se_tn = space_name(sub_element.tag)
                            se_tn = '%s/%s' % (tn, se_tn)
                            if se_tn in self.elements_properties:
                                p, t = self.elements_properties[se_tn]
                                tags_elements_properties_types.append((se_tn, sub_element, p, t))
                            else:
                                success = False
                                break
                        if not success:
                            if '*' in self.elements_properties:
                                p, t = self.elements_properties['*']
                                if SOAPElement in bases(t):
                                    tags_elements_properties_types.append((tn, element, p, t))
                                else:
                                    raise UnknownAttribute(
                                        '`%s` is not a recognized child element of `%s`' % (tn, self.__class__.__name__)
                                    )
                            else:
                                raise UnknownAttribute(
                                    '`%s` is not a recognized child element of `%s`' % (tn, self.__class__.__name__)
                                )
                for tn, v, p, t in tags_elements_properties_types:
                    if isinstance(t, (tuple, list)):
                        t = t[0] if t else None
                        if SOAPElement in bases(t):
                            if isinstance(v, Element):
                                getattr(self, p).append(t(v))
                            else:
                                raise ValueError(v)
                        else:
                            if t is Element:
                                if not isinstance(v, (Element, SOAPElement)):
                                    raise ValueError(v)
                                getattr(self, p).append(v)
                            else:
                                if isinstance(v, Element):
                                    v = v.text
                                if t is bool:
                                    getattr(self, p).append(
                                        True if v.lower().strip() in ('true', '1', 'yes', 'y')
                                        else False
                                    )
                                elif t is int:
                                    try:
                                        v = int(Decimal(v))
                                    except InvalidOperation as e:
                                        error_message = (
                                            '%s.%s: %s could not be cast as an integer\n\n%s' % (
                                                self.__class__.__name__,
                                                p,
                                                repr(v),
                                                self._string or tostring(self._element)
                                            ) + (
                                                (
                                                    '\n\n' + (
                                                        e.args[0]
                                                        if isinstance(e.args[0], str)
                                                        else repr(e.args[0])
                                                    )
                                                ) if e.args else ''
                                            )
                                        )
                                        e.args = tuple(chain(
                                            (error_message,),
                                            e.args[1:] if e.args else tuple()
                                        ))
                                        raise e
                                    getattr(self, p, v).append(v)
                                elif t is date:
                                    getattr(self, p).append(str2date(v))
                                elif t is datetime:
                                    getattr(self, p).append(str2datetime(v))
                                elif t is bytes:
                                    getattr(self, p).append(b64decode(v))
                                else:
                                    getattr(self, p).append(t(v))
                    else:
                        if SOAPElement in bases(t):
                            if isinstance(v, (Element, SOAPElement)):
                                setattr(self, p, t(v))
                            else:
                                raise ValueError(
                                    '%s is not a valid value for `%s.%s`' % (
                                        repr(v),
                                        self.__class__.__name__,
                                        p
                                    )
                                )
                        else:
                            if t is Element:
                                if not isinstance(v, Element):
                                    raise ValueError(v)
                                setattr(self, p, v)
                            else:
                                if isinstance(v, Element):
                                    v = v.text
                                if isinstance(v, str):
                                    v = v.strip()
                                    if v == '':
                                        continue
                                if t is bool:
                                    setattr(
                                        self,
                                        p,
                                        True if v.lower().strip() in ('true', '1', 'yes', 'y') else False
                                    )
                                elif t is int:
                                    try:
                                        v = int(Decimal(v))
                                    except InvalidOperation as e:
                                        error_message = (
                                            '%s.%s: %s could not be cast as an integer\n\n%s' % (
                                                self.__class__.__name__,
                                                p,
                                                repr(v),
                                                self._string or tostring(self._element)
                                            ) + (
                                                (
                                                    '\n\n' + (
                                                        e.args[0]
                                                        if isinstance(e.args[0], str)
                                                        else repr(e.args[0])
                                                    )
                                                ) if e.args else ''
                                            )
                                        )
                                        e.args = tuple(chain(
                                            (error_message,),
                                            e.args[1:] if e.args else tuple()
                                        ))
                                        raise e
                                    setattr(self, p, v)
                                elif t is date:
                                    setattr(self, p, str2date(v))
                                elif t is datetime:
                                    setattr(self, p, str2datetime(v))
                                elif t is bytes:
                                    setattr(self, p, b64decode(v))
                                else:
                                    try:
                                        setattr(self, p, t(v))
                                    except TypeError as e:
                                        e.args = tuple(
                                            [
                                                '\n%s: %s' % (t.__name__, repr(e.args[0])) + (
                                                    '\n' + e.args[0] if e.args else ''
                                                )
                                            ] + (
                                                list(e.args[1:])
                                                if len(e.args) > 1
                                                else []
                                            )
                                        )
                                        raise e

    def __str__(self):
        # type: () -> str
        """
        Casting instances of this class as `str` objects returns a normalized XML representation of the object, suitable
        for comparison, hashing, or passing in a SOAP request.

        :return:

            A normalized XML representation of the `SOAPElement` instance.
        """
        e = self.tag
        attributes_values = []
        if self.xmlns is not None:
            attributes_values.append(('xmlns', self.xmlns))
        for a, p_t in self.elements_properties.items():
            if a and a[0] == '@':
                a = a[1:]
                p, t = p_t
                vs = getattr(self, p)
                if vs is None:
                    continue
                if isinstance(t, (tuple, list)):
                    if t:
                        t = t[0]
                    else:
                        t = None
                else:
                    vs = [vs]
                for v in vs:
                    if not isinstance(v, t):
                        raise TypeError(
                            '%s is not an instance of `%s` (encountered while parsing `%s.%s`)' % (
                                repr(v),
                                t.__name__,
                                self.__class__.__name__,
                                p
                            )
                        )
                    if isinstance(v, datetime):
                        v = datetime2str(v)
                    elif isinstance(v, date):
                        v = date2str(v)
                    elif isinstance(v, bool):
                        v = 'true' if v else 'false'
                    elif isinstance(v, bytes):
                        v = str(b64encode(v), encoding='ascii')
                    elif isinstance(v, str):
                        if '"' in v:
                            v = v.replace('"', r'\"')
                        if '&' in v:
                            v = v.replace('&', '&amp;')
                        if '<' in v:
                            v = v.replace('<', '&lt;')
                        if '>' in v:
                            v = v.replace('>', '&gt;')
                    else:
                        v = str(v)
                    attributes_values.append((a, v))
        s = [
            '<%s%s>' % (
                self.tag,
                ''.join(
                    ' %s="%s"' % (a, v)
                    for a, v in attributes_values
                )
            )
        ]
        for tn, p_t in self.elements_properties.items():
            if tn and (tn[0] == '@' or tn == '*'):
                continue
            p, t = p_t
            vs = getattr(self, p)
            if isinstance(t, (tuple, list)):
                if t:
                    t = t[0]
                else:
                    t = None
            else:
                vs = [] if vs is None else [vs]
            if vs is None:
                raise ValueError(
                    '`None` is not a valid value for `%s.%s`' % (
                        self.__class__.__name__,
                        p
                    )
                )
            for v in vs:
                if v is not None:
                    if not (
                        (isinstance(v, SOAPElement) and t is Element) or
                        isinstance(v, t)
                    ):
                        raise TypeError(
                            '`%s.%s`: `%s` is not an instance of `%s`' % (
                                self.__class__.__name__,
                                p,
                                repr(v),
                                t.__name__
                            )
                        )
                if isinstance(v, SOAPElement):
                    if tn == '.':
                        raise ValueError(
                            '`%s.%s`: A `SOAPElement` cannot be attributed to the text content of an element.' % (
                                self.__class__.__name__,
                                p
                            )
                        )
                else:
                    if isinstance(v, Element):
                        v = tostring(v, encoding='unicode')
                    elif isinstance(v, datetime):
                        v = datetime2str(v)
                    elif isinstance(v, date):
                        v = date2str(v)
                    elif isinstance(v, bool):
                        v = 'true' if v else 'false'
                    elif isinstance(v, bytes):
                        v = str(b64encode(v), encoding='ascii')
                    elif isinstance(v, str):
                        if '&' in v:
                            v = v.replace('&', '&amp;')
                        if '<' in v:
                            v = v.replace('<', '&lt;')
                        if '>' in v:
                            v = v.replace('>', '&gt;')
                    else:
                        v = str(v)
                if tn == '.':
                    s.append(v)
                else:
                    for tn in reversed(tn.split('/')):
                        if isinstance(v, SOAPElement):
                            v = str(v)
                        elif '@' in tn:
                            tn, ta = tn.split('@')
                            v = '<%(tn)s %(ta)s="%(v)s" />' % dict(
                                tn=tn,
                                ta=ta,
                                v=v
                            )
                        else:
                            v = '<%(tn)s>%(v)s</%(tn)s>' % dict(
                                tn=tn,
                                v=v
                            )
                    s.append(v)
        if '*' in self.elements_properties:
            for se in self._element:
                ns, tn = space_name(se.tag)
                if tn not in self.elements_properties:
                    s.append(str(se))
        s.append('</%s>' % e)
        return ''.join(s)

    def __bool__(self):
        # type: () -> bool
        return True

    def __eq__(self, other):
        # type: (object) -> bool
        return (
            hasattr(other, '__class__') and
            (self.__class__ is other.__class__) and
            str(self) == str(other)
        )

    def __ne__(self, other):
        # type: (object) -> bool
        return (
            False if self == other
            else True
        )

    def __hash__(self):
        return hash(str(self))

    def __copy__(self):
        nse = self.__class__(self._string or self._element)
        nse.response = self.response
        for p, t in self.elements_properties.values():
            setattr(nse, p, getattr(self, p))
        return nse

    def __deepcopy__(
        self,
        memo=None  # type: Optional[dict]
    ):
        nse = self.__class__(
            self._string or
            deepcopy(self._element) if self._element is not None
            else None
        )
        nse.response = deepcopy(self.response, memo=memo)
        for p, t in self.elements_properties.values():
            setattr(nse, p, deepcopy(getattr(self, p), memo=memo))
        return nse


class GS1Code(SOAPElement):
    """
    Parameters:
        
        - text (str): A GS1 code, for which possible values are determined by the sub-classification instantiated.
        - code_list_version (str): Which snapshot of the code-list was this code taken from?
    """

    elements_properties = OrderedDict([
        ('.', ('text', str)),
        ('@codeListVersion', ('code_list_version', str))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        text=None,  # type: Optional[str]
        code_list_version=None,  # type: Optional[str]
        tag=None  # type: Optional[str]
    ):
        self.text = text  # type: Optional[str]
        self.code_list_version = code_list_version  # type: Optional[str]
        if tag is None:
            tag = self.__class__.__name__
            if tag[:5] == 'GEPIR':
                tag = 'gepir' + tag[5:]
            else:
                tag = tag[0].lower() + tag[1:]
        super().__init__(xml=xml, tag=tag)


class GEPIRStatusCode(GS1Code):

    pass


class GEPIRVersionCode(GS1Code):

    pass


class GEPIRVersionCode(GS1Code):

    pass


class GEPIRReturnCode(GS1Code):
    """
    Parameters:
        
        - text (str): "0" indicates success, all other values indicate an error has occurred.
          + "0" (Query Successful): The request has been successfully completed and the response
            is in the body of the message.
          + "1" (Missing or invalid parameters): One or more parameters are missing or
            incorrect. This might be and  incorrect length, invalid check digit, a non-numeric
            characters in a number, etc. No data is returned.
          + "2" (Record not found): No record exists for this key or these search parameters. No
            data is returned.
          + "3" (No exact match on Requested Key): No record was found for this Requested Key.
            The data held in the MO database for this company prefix is returned.
          + "4" (Too many hits): Over twenty records match the search criteria. Only twenty are
            returned.
          + "5" (Unknown GS1 Prefix): The GS1 prefix (3 digit country code) does not exist.
          + "6" (Response may be incomplete): One or more servers failed to respond for the
            global search (“ZZ”). Such data as is available is returned.
          + "7" (Request timed out): There was a timeout somewhere in the server chain. No data
            is returned.
          + "8" (No catalogue exists): A request has been made for GTIN information, but there
            is no server for this company. No data is returned.
          + "9" (Company information withheld): The company prefix in the request exists, but
            the company has not released its information for publication. The name and address
            of the responsible MO is returned.
          + "10" (Prefix no longer subscribed): The company prefix in the request exists, but
            the company is no longer a member of GS1 under this prefix. The name and address of
            the responsible MO is returned.
          + "11" (Country not on the GEPIR network): There is no GEPIR MO server for this
            country. This should only be used with Get Party by Name.
          + "12" (Item information withheld): The GTIN in the request exists, but the company
            has not released its information for publication.
          + "13" (Unauthorised number): The company prefix in the request is known to be
            unauthorised. The name and address of the responsible MO is returned.
          + "14" (Daily request limit exceeded): The user has exceeded the number of "free"
            requests permitted (30) and the request is rejected. No data is returned. The
            ``responder_Gln`` element is set by the node refusing the request.
          + "15" (GLN not assigned): The provided GS1 Key is valid, however a GLN not assigned 
            to this key.
          + "16" (Internal use only): Prefixes 020-029 and 040-049 are for a company's internal
            use only, so no information can be returned. Returns only the name and address of 
            the MO which was queried.
          + "17" (Internal use only): Prefixes 200-299 are for a company's internal use only, so
            no information can be returned. Returns only the name and address of the MO which 
            was queried.
          + "18" (ISSN): Prefix 977 is used for serial publications (ISSN), so no information
            can be returned. Only the name and address of the MO queried is returned.
          + "19" (ISBN): Prefixes 978-979 are for books (ISBN), so no information can be 
            returned. Returns only the name and address of the MO which was queried.
          + "20" (Coupon Prefix): Prefixes 050-059 are for coupons, so no information
            can be returned. Returns only the name and address of the MO which was queried.
          + "21" (Prefix never allocated): No record exists for this key, so not data can be 
            returned. This code can only be used when historical data is available.
          + "97" (Unsupported request for this version): The request contains elements which 
            cannot be processed by a GEPIR Router of the current version.
          + "98" (Authorization failed): The Authorization process has failed and access is not
            granted.
          + "99" (Server error): The router is functional, however accessjng data is not 
            currently possible. The
            ``responder_gln`` is set by the node detecting the error.
        - code_list_version (str): Which snapshot of the code-list was this code taken from?
    """

    pass


class AdditionalPartyIdentificationCode(GS1Code):

    pass


class AdditionalTradeItemClassificationSystemCode(GS1Code):

    pass


class TradeItemUnitDescriptorCode(GS1Code):

    pass


class AdditionalConsignmentIdentificationTypeCode(GS1Code):

    pass


class AdditionalIndividualAssetIdentificationTypeCode(GS1Code):

    pass


class AdditionalLogisticUnitIdentificationTypeCode(GS1Code):

    pass


class AdditionalPartyIdentificationTypeCode(GS1Code):

    pass


class AdditionalReturnableAssetIdentificationTypeCode(GS1Code):

    pass


class AdditionalServiceRelationIdentificationTypeCode(GS1Code):

    pass


class AdditionalShipmentIdentificationTypeCode(GS1Code):

    pass


class AdditionalTradeItemIdentificationTypeCode(GS1Code):

    pass


class AllowanceChargeTypeCode(GS1Code):

    pass


class BarCodeTypeCode(GS1Code):

    pass


class CommunicationChannelCode(GS1Code):

    pass


class ContactTypeCode(GS1Code):

    pass


class CountryCode(GS1Code):

    pass


class CountrySubdivisionCode(GS1Code):

    pass


class CurrencyCode(GS1Code):

    pass


class DateFormatCode(GS1Code):

    pass


class EntityTypeCode(GS1Code):

    pass


class FinancialAccountNumberTypeCode(GS1Code):

    pass


class FinancialRoutingNumberTypeCode(GS1Code):

    pass


class IncotermsCode(GS1Code):

    pass


class LanguageCode(GS1Code):

    pass


class MeasurementUnitCode(GS1Code):

    pass


class NutrientTypeCode(GS1Code):

    pass


class PartyRoleCode(GS1Code):

    pass


class PaymentMethodCode(GS1Code):

    pass


class PaymentTermsTypeCode(GS1Code):

    pass


class TaxCategoryCode(GS1Code):

    pass


class TemperatureMeasurementUnitCode(GS1Code):

    pass


class TimeMeasurementUnitCode(GS1Code):

    pass


class AdditionalPartyIdentification(SOAPElement):

    elements_properties = OrderedDict([
        ('.', ('text', str)),
        ('@codeListVersion', ('code_list_version', str)),
        ('@additionalPartyIdentificationTypeCode', ('additional_party_identification_type_code', str))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        text=None,  # type: Optional[str]
        tag='additionalPartyIdentification',  # type: str
        code_list_version=None,  # type: Optional[str]
        additional_party_identification_type_code=None  # type: Optional[str]
    ):
        self.text = text  # type: Optional[str]
        self.code_list_version = code_list_version  # type: Optional[str]
        self.additional_party_identification_type_code = (
            additional_party_identification_type_code
        )  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GetItemByGTIN(SOAPElement):

    elements_properties = OrderedDict([
        ('requestedLanguage', ('requested_language', LanguageCode)),
        ('requestedGTIN', ('requested_gtin', (str,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getItemByGTIN',  # type: str
        requested_language=None,  # type: Optional[LanguageCode]
        requested_gtin=None,  # type: Sequence[str]
    ):
        self.requested_language = requested_language
        self.requested_gtin = requested_gtin or []
        super().__init__(xml=xml, tag=tag)


class Measurement(SOAPElement):

    elements_properties = OrderedDict([
        ('.', ('quantity', Decimal)),
        ('@measurementUnitCode', ('measurement_unit_code', str)),
        ('@codeListVersion', ('code_list_version', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='measurement',  # type: str
        quantity=None,  # type: Optional[Decimal]
        measurement_unit_code=None,  # type: Optional[str]
        code_list_version=None,  # type: Optional[str]
    ):
        self.quantity = quantity  # type: Optional[Decimal]
        self.measurement_unit_code = measurement_unit_code  # type: Optional[str]
        self.code_list_version = code_list_version  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class RequestedKeyCode(GS1Code):
    """
    Properties: 
    
        - text (str): This key code indicates the type of data contained in the requested key value.
    
            + "GTIN": A 14-digit Global Trade Item Number (GTIN), composed of numneric digits only.
            + "GLN": A 13-digit Global Location Number (GLN), composed of numeric digits only.
            + "SSCC": An 18-digit Serial Shipping Container Code (SSCC), composed of numeric digits only.
            + "GRAI": A 13-digit Global Returnable Asset Identifier (GRAI), composed of numeric digits only.
            + "GIAI": A 30-digit Global Individual Asset Identifier (GIAI), composed of numeric digits only.
            + "GSRN": An 18-digit Global Service Relation Number (GSRN), composed of numeric digits only.
            + "GDTI": A 13-digit Global Document Type Identifier (GDTI), composed of numeric digits only.
            + "GSIN": A 17-digit Global Shipment Identification Number (GSIN), composed of numeric digits only.
            + "GINC": A 30-digit Global Identification Number for Consignment (GINC), composed of numeric digits only.
            + "GCN": A 13-digit Global Coupon Number (GCN), composed of numeric digits only.
            
        - code_list_version (str)
    """

    pass


class GEPIRRequestedKey(SOAPElement):

    elements_properties = OrderedDict([
        ('requestedLanguage', ('requested_language', LanguageCode)),
        ('requestedKeyCode', ('requested_key_code', RequestedKeyCode)),
        ('requestedKeyValue', ('requested_key_value', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirRequestedKey',  # type: str
        requested_key_code=None,  # type: Optional[RequestedKeyCode]
        requested_key_value=None,  # type: Optional[str]
        requested_language=None  # type: Optional[LanguageCode]
    ):
        self.requested_key_code = requested_key_code
        self.requested_key_value = requested_key_value
        self.requested_language = requested_language
        super().__init__(xml=xml, tag=tag)


class AdditionalTradeItemClassification(SOAPElement):

    elements_properties = OrderedDict([
        (
            'additionalTradeItemClassificationSystemCode',
            (
                'additional_trade_item_classification_system_code',
                AdditionalTradeItemClassificationSystemCode
            )
        ),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        additional_trade_item_classification_system_code=None,  # type: Optional[str]
        tag='additionalTradeItemClassification'  # type: str
    ):
        self.additional_trade_item_classification_system_code = additional_trade_item_classification_system_code
        super().__init__(xml=xml, tag=tag)


class TradeItemClassification(SOAPElement):

    elements_properties = OrderedDict([
        ('gpcCategoryCode', ('gpc_category_code', str)),
        ('gpcCategoryDefinition', ('gpc_category_definition', str)),
        ('gpcCategoryName', ('gpc_category_name', str)),
        (
            'additionalTradeItemClassification', (
                'additional_trade_item_classification',
                (AdditionalTradeItemClassification,)
             )
        ),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='tradeItemClassification',  # type: str
        gpc_category_code=None,  # type: Optional[str]
        gpc_category_definition=None,  # type: Optional[str]
        gpc_category_name=None,  # type: Optional[str]
        additional_trade_item_classification=None  # type: Optional[Sequence[AdditionalTradeItemClassification]]
    ):
        self.gpc_category_code = gpc_category_code  # type: Optional[str]
        self.gpc_category_definition = gpc_category_definition  # type: Optional[str]
        self.gpc_category_name = gpc_category_name  # type: Optional[str]
        self.additional_trade_item_classification = (
            additional_trade_item_classification or []
        )  # type: Sequence[AdditionalTradeItemClassification]
        super().__init__(xml=xml, tag=tag)


class ResponderSpecificData(SOAPElement):

    elements_properties = OrderedDict([
        ('responderSpecificData', ('responder_specific_data', str)),
        ('responderSpecificDataUse', ('responder_specific_data_use', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='responderSpecificData',  # type: str
        responder_specific_data=None,  # type: Optional[str]
        responder_specific_data_use=None,  # type: Optional[str]
    ):
        self.responder_specific_data = responder_specific_data   # type: Optional[str]
        self.responder_specific_data_use = responder_specific_data_use  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class PartyContainment(SOAPElement):

    elements_properties = OrderedDict()

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='partyContainment',  # type: str
        party_child=None,  # type: Optional[GEPIRPartyInformation]
    ):
        self.party_child = party_child  # type: Optional[GEPIRPartyInformation]
        super().__init__(xml=xml, tag=tag)


class GEPIRPartyInformation(SOAPElement):

    elements_properties = OrderedDict([
        ('additionalPartyIdentification', ('additional_party_identification', (AdditionalPartyIdentification,))),
        ('gln', ('gln', str)),
        ('partyName', ('party_name', (str,))),
        ('partyRole', ('party_role', (PartyRoleCode,))),
        ('partyContainment', ('party_containment', (PartyContainment,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirPartyInformation',  # type: str
        additional_party_identification=None,  # type: Optional[Sequence[AdditionalPartyIdentification]]
        gln=None,  # type: Optional[str]
        party_name=None,  # type: Optional[Sequence[str]]
        party_role=None,  # type: Optional[Sequence[PartyRoleCode]]
        party_containment=None,  # type: Optional[Sequence[PartyContainment]]
    ):
        self.additional_party_identification = (
            additional_party_identification or []
        )  # type: Sequence[AdditionalPartyIdentification]
        self.gln = gln  # type: Optional[str]
        self.party_name = party_name or []  # type: Sequence[str]
        self.party_role = party_role or []  # type: Sequence[PartyRoleCode]
        self.party_containment = party_containment or []  # type: Sequence[PartyContainment]
        super().__init__(xml=xml, tag=tag)


PartyContainment.elements_properties['partyChild'] = ('party_child', GEPIRPartyInformation)


class ExternalFileLink(SOAPElement):

    xmlns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    elements_properties = OrderedDict([
        ('@xmlns:xsi', ('xmlns_xsi', str)),
        ('fileFormatName', ('file_format_name', str)),
        ('uniformResourceIdentifier', ('uniform_resource_identifier', str)),
        ('@xsi:nil', ('nil', bool)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='externalFileLink',  # type: str
        file_format_name=None,  # type: Optional[str]
        uniform_resource_identifier=None,  # type: Optional[str]
        nil=None,  # type: Optional[bool]
    ):
        self.file_format_name = file_format_name  # type: str
        self.uniform_resource_identifier = uniform_resource_identifier  # type: Optional[str]
        self.nil = nil  # type: Optional[bool]
        super().__init__(xml=xml, tag=tag)


class SizeCode(SOAPElement):

    elements_properties = OrderedDict([
        ('sizeCodeListCode', ('size_code_list_code', str)),
        ('sizeCodeListDescription', ('size_code_list_description', str)),
        ('codeListVersion', ('code_list_version', str)),
        ('sizeCodeListVersion', ('size_code_list_version', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='sizeCode',  # type: str
        size_code_list_code=None,  # type: Optional[str]
        size_code_list_description=None,  # type: Optional[str]
        code_list_version=None,  # type: Optional[str]
        size_code_list_version=None,  # type: Optional[str]
    ):
        self.size_code_list_code = size_code_list_code  # type: Optional[str]
        self.size_code_list_description = size_code_list_description  # type: Optional[str]
        self.code_list_version = code_list_version  # type: Optional[str]
        self.size_code_list_version = size_code_list_version  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class Description70(SOAPElement):

    elements_properties = OrderedDict([
        ('.', ('text', str)),
        ('@languageCode', ('language_code', str)),
        ('@codeListVersion', ('code_list_version', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='description',  # type: Optional[str]
        language_code=None,  # type: Optional[str]
        code_list_version=None,  # type: Optional[str]
        text=None  # type: Optional[str]
    ):
        self.language_code = language_code  # type: Optional[str]
        self.code_list_version = code_list_version  # type: Optional[str]
        self.text = text  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class Description80(Description70):

    pass


class Size(SOAPElement):

    elements_properties = OrderedDict([
        ('descriptiveSize', ('descriptive_size', Description80)),
        ('sizeCode', ('size_code', SizeCode)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='size',  # type: str
        descriptive_size=None,  # type: Optional[Description80]
        size_code=None,  # type: Optional[SizeCode]
    ):
        self.descriptive_size = descriptive_size
        self.size_code = size_code
        super().__init__(xml=xml, tag=tag)


class NextLowerLevelTradeItemInformation(SOAPElement):

    elements_properties = OrderedDict([
        ('quantityOfChildren', ('quantity_of_children', int)),
        ('totalQuantityOfNextLowerLevelTradeItem', ('total_quantity_of_next_lower_level_trade_item', int)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='nextLowerLevelTradeItemInformation',  # type: str
        quantity_of_children=None,  # type: Optional[int]
        total_quantity_of_next_lower_level_trade_item=None,  # type: Optional[int]
    ):
        self.quantity_of_children = quantity_of_children
        self.total_quantity_of_next_lower_level_trade_item = total_quantity_of_next_lower_level_trade_item
        super().__init__(xml=xml, tag=tag)


class ItemDataLine(SOAPElement):

    elements_properties = OrderedDict([
        ('returnCode', ('return_code', GEPIRReturnCode)),
        ('itemDataLanguage', ('item_data_language', LanguageCode)),
        ('lastChangeDate', ('last_change_date', datetime)),
        ('netContent', ('net_content', (Measurement,))),
        ('tradeItemUnitDescriptor', ('trade_item_unit_descriptor', TradeItemUnitDescriptorCode)),
        ('itemName', ('item_name', str)),
        ('brandName', ('brand_name', str)),
        ('tradeItemClassification', ('trade_item_classification', (TradeItemClassification,))),
        ('gepirRequestedKey', ('gepir_requested_key', GEPIRRequestedKey)),
        ('responderSpecificData', ('responder_specific_data', (ResponderSpecificData,))),
        ('informationProvider', ('information_provider', GEPIRPartyInformation)),
        ('manufacturer', ('manufacturer', GEPIRPartyInformation)),
        ('requestedItem', ('requested_item', (ExternalFileLink,))),
        ('size', ('size', Size)),
        (
            'nextLowerLevelTradeItemInformation',
            (
                'next_lower_level_trade_item_information',
                NextLowerLevelTradeItemInformation
            )
        ),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='itemDataLine',  # type: str
        item_data_language=None,  # type: Optional[str]
        last_change_date=None,  # type: Optional[datetime]
        net_content=None,  # type: Optional[Sequence[Measurement]]
        return_code=None,  # type: Optional[GEPIRReturnCode]
        trade_item_unit_descriptor=None,  # type: Optional[TradeItemUnitDescriptorCode]
        item_name=None,  # type: Optional[str]
        brand_name=None,  # type: Optional[str]
        trade_item_classification=None,  # type: Optional[Sequence[TradeItemClassification]]
        gepir_requested_key=None,  # type: Optional[GEPIRRequestedKey]
        responder_specific_data=None,  # type: Optional[Sequence[ResponderSpecificData]]
        information_provider=None,  # type: Optional[GEPIRPartyInformation]
        manufacturer=None,  # type: Optional[GEPIRPartyInformation]
        requested_item=None,  # type: Optional[Sequence[ExternalFileLink]]
        size=None,  # type: Optional[Size]
        next_lower_level_trade_item_information=None,  # type: Optional[NextLowerLevelTradeItemInformation]
    ):
        self.return_code = return_code  # type: Optional[GEPIRReturnCode]
        self.item_data_language = item_data_language  # type: Optional[str]
        self.last_change_date = last_change_date  # type: Optional[datetime]
        self.net_content = net_content or []  # type: Optional[Measurement]
        self.trade_item_unit_descriptor = trade_item_unit_descriptor  # type: Optional[TradeItemUnitDescriptorCode]
        self.item_name = item_name  # type: Optional[str]
        self.brand_name = brand_name  # type: Optional[str]
        self.trade_item_classification = trade_item_classification or []  # type: Sequence[TradeItemClassification]
        self.gepir_requested_key = gepir_requested_key  # type: Optional[GEPIRRequestedKey]
        self.responder_specific_data = responder_specific_data or []  # type: Sequence[ResponderSpecificData]
        self.information_provider = information_provider  # type: Optional[GEPIRPartyInformation]
        self.manufacturer = manufacturer  # type: Optional[GEPIRPartyInformation]
        self.requested_item = requested_item or []  # type: Sequence[ExternalFileLink]
        self.size = size  # type: Optional[Size]
        self.next_lower_level_trade_item_information = (
            next_lower_level_trade_item_information
        )  # type: Optional[NextLowerLevelTradeItemInformation]
        super().__init__(xml=xml, tag=tag)


class GEPIRItem(SOAPElement):

    elements_properties = OrderedDict([
        ('itemDataLine', ('item_data_line', (ItemDataLine,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirItem',  # type: str
        item_data_line=None  # type: Optional[Sequence[ItemDataLine]]
    ):
        self.item_data_line = ItemDataLines(item_data_line or [])  # type: Sequence[ItemDataLine]
        super().__init__(xml=xml, tag=tag)


class ItemDataLines(list):
    """
    This sub-class of `list` will raise the appropriate error when accessing an item data line
    with a non-zero return code.
    """

    def __getitem__(self, item):
        # type: (int) -> SOAPElement
        item_data_line = list.__getitem__(self, item)  # type: Union[int, ItemDataLine]
        if not isinstance(item_data_line, ItemDataLine):
            item_data_line = ItemDataLine(item_data_line)
        rc = item_data_line.return_code.text.strip()
        if rc in RETURN_CODES_EXCEPTIONS:
            raise RETURN_CODES_EXCEPTIONS[rc](str(item_data_line))
        elif int(item_data_line.return_code.text) != 0:
            raise KeyError('%s not found in %s' % (repr(rc), repr(RETURN_CODES_EXCEPTIONS)))
        return item_data_line

    def __str__(self):
        return ''.join([
            str(list.__getitem__(self, i))
            for i in range(len(self))
        ])

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


class PartyDataLines(list):  # type: List[PartyDataLine]
    """
    This sub-class of `list` will raise the appropriate error when accessing a party data line
    with a non-zero return code.
    """

    def __getitem__(self, item):
        # type: (int) -> PartyDataLine
        party_data_line = list.__getitem__(self, item)  # type: Union[int, ItemDataLine]
        if not isinstance(party_data_line, PartyDataLine):
            party_data_line = PartyDataLine(party_data_line)
        rc = party_data_line.return_code.text.strip()
        if rc in RETURN_CODES_EXCEPTIONS:
            raise RETURN_CODES_EXCEPTIONS[rc]((str(party_data_line)))
        elif int(party_data_line.return_code.text) != 0:
            raise KeyError('%s not found in %s' % (repr(rc), repr(RETURN_CODES_EXCEPTIONS)))
        return party_data_line

    def __str__(self):
        # type: () -> str
        return ''.join([
            str(list.__getitem__(self, i))
            for i in range(len(self))
        ])

    def __iter__(self):
        # type: () -> Iterable[PartyDataLine]
        for i in range(len(self)):
            yield self[i]


class CommunicationChannel(SOAPElement):

    elements_properties = OrderedDict([
        ('communicationChannelCode', ('communication_channel_code', str)),
        ('communicationValue', ('communication_value', str)),
        ('communicationChannelName', ('communication_channel_name', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='communicationChannel',  # type: str
        communication_channel_code=None,  # type: Optional[str]
        communication_value=None,  # type: Optional[str]
        communication_channel_name=None  # type: Optional[str]
    ):
        self.communication_channel_code = communication_channel_code  # type: Optional[str]
        self.communication_value = communication_value  # type: Optional[str]
        self.communication_channel_name = communication_channel_name  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class Contact(SOAPElement):

    elements_properties = OrderedDict([
        ('contactTypeCode', ('contact_type_code', str)),
        ('personName', ('person_name', str)),
        ('departmentName', ('department_name', str)),
        ('jobTitle', ('job_title', str)),
        ('responsibility', ('responsibility', (Description70,))),
        ('communicationChannel', ('communication_channel', (CommunicationChannel,))),
        ('afterHoursCommunicationChannel', ('after_hours_communication_channel', (CommunicationChannel,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='contact',  # type: str
        contact_type_code=None,  # type: Optional[str]
        person_name=None,  # type: Optional[str]
        department_name=None,  # type: Optional[str]
        job_title=None,  # type: Optional[str]
        responsibility=None,  # type: Optional[Sequence[Description70]]
        communication_channel=None,  # type: Optional[Sequence[CommunicationChannel]]
        after_hours_communication_channel=None   # type: Optional[Sequence[CommunicationChannel]]
    ):
        self.contact_type_code = contact_type_code  # type: Optional[str]
        self.person_name = person_name  # type: Optional[str]
        self.department_name = department_name  # type: Optional[str]
        self.job_title = job_title  # type: Optional[str]
        self.responsibility = responsibility or [] # type: Optional[Sequence[Description70]]
        self.communication_channel = communication_channel or [] # type: Sequence[CommunicationChannel]
        self.after_hours_communication_channel = (
            after_hours_communication_channel or []
        )  # type: Sequence[CommunicationChannel]
        super().__init__(xml=xml, tag=tag)


class GeographicalCoordinates(SOAPElement):

    elements_properties = OrderedDict([
        ('latitude', ('latitude', str)),
        ('longitude', ('longitude', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='geographicalCoordinates',  # type: str
        latitude=None,  # type: Optional[str]
        longitude=None,  # type: Optional[str]
    ):
        self.latitude = latitude
        self.longitude = longitude
        super().__init__(xml=xml, tag=tag)


class Address(SOAPElement):

    elements_properties = OrderedDict([
        ('name', ('name', str)),
        ('pOBoxNumber', ('po_box_number', str)),
        ('streetAddressOne', ('street_address_one', str)),
        ('streetAddressTwo', ('street_address_two', str)),
        ('streetAddressThree', ('street_address_three', str)),
        ('city', ('city', str)),
        ('cityCode', ('city_code', str)),
        ('countyCode', ('county_code', str)),
        ('provinceCode', ('province_code', str)),
        ('state', ('state', str)),
        ('postalCode', ('postal_code', str)),
        ('countryCode', ('country_code', CountryCode)),
        ('geographicalCoordinates', ('geographical_coordinates', GeographicalCoordinates)),
        ('currencyOfPartyCode', ('currency_of_party_code', CurrencyCode)),
        ('languageOfThePartyCode', ('language_of_the_party_code', LanguageCode)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='address',  # type: str
        city=None,  # type: Optional[str]
        city_code=None,  # type: Optional[str]
        country_code=None,  # type: Optional[CountryCode]
        county_code=None,  # type: Optional[str]
        cross_street=None,  # type: Optional[str]
        currency_of_party_code=None,  # type: Optional[CurrencyCode]
        language_of_the_party_code=None,  # type: Optional[LanguageCode]
        name=None,  # type: Optional[str]
        po_box_number=None,  # type: Optional[str]
        postal_code=None,  # type: Optional[str]
        province_code=None,  # type: Optional[str]
        state=None,  # type: Optional[str]
        street_address_one=None,  # type: Optional[str]
        street_address_two=None,  # type: Optional[str]
        street_address_three=None,  # type: Optional[str]
        geographical_coordinates=None,  # type: Optional[GeographicalCoordinates]
    ):
        self.city = city  # type: Optional[str]
        self.city_code = city_code  # type: Optional[str]
        self.country_code = country_code  # type: Optional[CountryCode]
        self.county_code = county_code  # type: Optional[str]
        self.cross_street = cross_street  # type: Optional[str]
        self.currency_of_party_code = currency_of_party_code  # type: Optional[CurrencyCode]
        self.language_of_the_party_code = language_of_the_party_code  # type: Optional[LanguageCode]
        self.name = name  # type: Optional[str]
        self.po_box_number = po_box_number  # type: Optional[str]
        self.postal_code = postal_code  # type: Optional[str]
        self.province_code = province_code  # type: Optional[str]
        self.state = state  # type: Optional[str]
        self.street_address_one = street_address_one  # type: Optional[str]
        self.street_address_one = street_address_one  # type: Optional[str]
        self.street_address_two = street_address_two  # type: Optional[str]
        self.street_address_three = street_address_three  # type: Optional[str]
        self.geographical_coordinates = geographical_coordinates  # type: Optional[GeographicalCoordinates]
        super().__init__(xml=xml, tag=tag)


class PartyDataLine(SOAPElement):
    """
    Detailed information about a GEPIR party (company).
    
    Parameters:
        
        - last_change_date (datetime): A date assigned by the system indicating the last time this information was
          altered.
        - gs1_company_prefix (str): The GS1 Company Prefix of the GS1 key being requested.
        - information_provider (GEPIRPartyInformation): Party information about the originator of this response line.
        - party_data_language (str): Indicates the language used to represent data in this response line.
        - return_code (GEPIRReturnCode): Indicates the success or failure of a request. 
        - address (Address): A location at which representatives of this party may be reached.
        - gepir_requested_key (GEPIRRequestedKey): Details about the requested GS1 key. This can be useful when
          multiple keys are queried in the same request.
        - gepir_item_external_file_link (Sequence[ExternalFileLink]): One or more references to related electronic 
          files.
        - responder_specific_data (ResponderSpecificData): A user-defined field for passing additional information about
          this party.
        - gs1_company_prefix_licensee (GEPIRPartyInformation): Information about the party licensing the prefix
          contained in the referenced GS1 key. This will be absent when a solitary key has been licensed (a very
          uncommon scenario), as opposed to a prefix.
        - gs1_key_licensee (GEPIRPartyInformation): Information about the party licensing the referenced GS1 key.
        - information_provider (GEPIRPartyInformation): Information about the party from whom this response line 
          originates.
        - contact (Sequence[Contact]): Information about a individuals or departments acting as a contact for this 
          organization.
    """

    elements_properties = OrderedDict([
        ('gS1CompanyPrefix', ('gs1_company_prefix', str)),
        ('lastChangeDate', ('last_change_date', datetime)),
        ('partyDataLanguage', ('party_data_language', str)),
        ('returnCode', ('return_code', GEPIRReturnCode)),
        ('address', ('address', Address)),
        ('gepirRequestedKey', ('gepir_requested_key', GEPIRRequestedKey)),
        ('responderSpecificData', ('responder_specific_data', ResponderSpecificData)),
        ('gepirItemExternalFileLink', ('gepir_item_external_file_link', (ExternalFileLink,))),
        ('gS1CompanyPrefixLicensee', ('gs1_company_prefix_licensee', GEPIRPartyInformation)),
        ('gS1KeyLicensee', ('gs1_key_licensee', GEPIRPartyInformation)),
        ('informationProvider', ('information_provider', GEPIRPartyInformation)),
        ('contact', ('contact', (Contact,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='partyDataLine',  # type: str
        gs1_company_prefix=None,  # type: Optional[str]
        last_change_date=None,  # type: Optional[datetime]
        party_data_language=None,  # type: Optional[str]
        return_code=None,  # type: Optional[GEPIRReturnCode]
        address=None,  # type: Optional[Address]
        gepir_requested_key=None,  # type: Optional[GEPIRRequestedKey]
        responder_specific_data=None,  # type: Optional[ResponderSpecificData]
        gepir_item_external_file_link=None,  # type: Optional[Sequence[ExternalFileLink]]
        gs1_company_prefix_licensee=None,  # type: Optional[GEPIRPartyInformation]
        gs1_key_licensee=None,  # type: Optional[GEPIRPartyInformation]
        information_provider=None,  # type: Optional[GEPIRPartyInformation]
        contact=None,  # type: Optional[Sequence[Contact]],
    ):
        self.gs1_company_prefix = gs1_company_prefix  # type: Optional[str]
        self.last_change_date = last_change_date  # type: Optional[datetime]
        self.party_data_language = party_data_language  # type: Optional[str]
        self.return_code = return_code  # type: Optional[GEPIRReturnCode]
        self.address = address  # type: Optional[Address]
        self.gepir_requested_key = gepir_requested_key  # type: Optional[GEPIRRequestedKey]
        self.responder_specific_data = responder_specific_data  # type: Optional[ResponderSpecificData]
        self.gepir_item_external_file_link = gepir_item_external_file_link or []  # type: Sequence[ExternalFileLink]
        self.gs1_company_prefix_licensee = gs1_company_prefix_licensee  # type: Optional[GEPIRPartyInformation]
        self.gs1_key_licensee = gs1_key_licensee  # type: Optional[GEPIRPartyInformation]
        self.information_provider = information_provider  # type: Optional[GEPIRPartyInformation]
        self.contact = contact or []  # type: Optional[Sequence[Contact]],
        super().__init__(xml=xml, tag=tag)


class GEPIRParty(SOAPElement):

    elements_properties = OrderedDict([
        ('partyDataLine', ('party_data_line', (PartyDataLine,)))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirParty',  # type: str
        party_data_line=None  # type: Optional[Sequence[PartyDataLine]]
    ):
        self.party_data_line = PartyDataLines(party_data_line or [])  # type: PartyDataLines
        super().__init__(xml=xml, tag=tag)


class GEPIRCountry(SOAPElement):

    elements_properties = OrderedDict([
        ('countryCode', ('country_code', CountryCode)),
        ('countryName', ('country_name', Description70)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirCountry',  # type: str
        country_code=None,  # type: Optional[CountryCode]
        country_name=None,  # type: Optional[Description70]
    ):
        self.country_code = country_code  # type: Optional[CountryCode]
        self.country_name = country_name  # type: Optional[Description70]
        super().__init__(xml=xml, tag=tag)


class PrefixRange(SOAPElement):

    elements_properties = OrderedDict([
        ('prefixRangeLow', ('prefix_range_low', str)),
        ('prefixRangeHigh', ('prefix_range_high', str))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='prefixRange',  # type: str
        prefix_range_low=None,  # type: Optional[str]
        prefix_range_high=None,  # type: Optional[str]
    ):
        self.prefix_range_low = prefix_range_low  # type: Optional[str]
        self.prefix_range_high = prefix_range_high  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GEPIRServer(SOAPElement):

    elements_properties = OrderedDict([
        ('serverCountry', ('server_country', CountryCode)),
        ('serverGLN', ('server_gln', str))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirServer',  # type: str
        server_country=None,  # type: Optional[CountryCode]
        server_gln=None,  # type: Optional[str]
    ):
        self.server_country = server_country  # type: Optional[CountryCode]
        self.server_gln = server_gln  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class EntryPoint(SOAPElement):

    elements_properties = OrderedDict([
        ('gepirVersionCode', ('gepir_version_code', GEPIRVersionCode)),
        ('routerURL', ('router_url', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        gepir_version_code=None,  # type: Optional[GEPIRVersionCode]
        router_url=None,  # type: Optional[str]
    ):
        self.gepir_version_code = gepir_version_code  # type: Optional[GEPIRVersionCode]
        self.router_url = router_url  # type: Optional[str]
        super().__init__(xml=xml)


class GEPIRRouter(SOAPElement):

    elements_properties = OrderedDict([
        ('routerGLN', ('router_gln', str)),
        ('routerIPAddress', ('router_ip_address', str)),
        ('routerSubnetMask', ('router_subnet_mask', str)),
        ('routerURL', ('router_url', str)),
        ('legacyVersion', ('legacy_version', EntryPoint)),
        ('gepirRouterTechnicalContact', ('gepir_router_technical_contact', Contact)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirRouter',  # type: str
        router_gln=None,  # type: Optional[str]
        router_ip_address=None,  # type: Optional[str]
        router_subnet_mask=None,  # type: Optional[str]
        router_url=None,  # type: Optional[str]
        legacy_version=None,  # type: Optional[str]
        gepir_router_technical_contact=None,  # type: Optional[str]
    ):
        self.router_gln = router_gln  # type: Optional[str]
        self.router_ip_address = router_ip_address  # type: Optional[str]
        self.router_subnet_mask = router_subnet_mask  # type: Optional[str]
        self.router_url = router_url  # type: Optional[str]
        self.legacy_version = legacy_version  # type: Optional[str]
        self.gepir_router_technical_contact = gepir_router_technical_contact  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GEPIRInformation(SOAPElement):

    elements_properties = OrderedDict([
        ('gepirClientURI', ('gepir_client_uri', str)),
        ('gepirStatusCode', ('gepir_status_code', GEPIRStatusCode)),
        ('gepirVersionCode', ('gepir_version_code', GEPIRVersionCode)),
        ('supportedLanguage', ('supported_language', LanguageCode)),
        ('gepirServer', ('gepir_server', GEPIRServer)),
        ('gepirRouter', ('gepir_router', GEPIRRouter)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirInformation',  # type: str
        gepir_client_uri=None,  # type: Optional[str]
        gepir_status_code=None,  # type: Optional[GEPIRStatusCode]
        gepir_version_code=None,  # type: Optional[GEPIRVersionCode]
        supported_language=None,  # type: Optional[LanguageCode]
        gepir_server=None,  # type: Optional[GEPIRServer]
        gepir_router=None,  # type: Optional[GEPIRRouter]
    ):
        self.gepir_client_uri = gepir_client_uri  # type: Optional[str]
        self.gepir_status_code = gepir_status_code  # type: Optional[GEPIRStatusCode]
        self.gepir_version_code = gepir_version_code  # type: Optional[GEPIRVersionCode]
        self.supported_language = supported_language  # type: Optional[LanguageCode]
        self.gepir_server = gepir_server  # type: Optional[GEPIRServer]
        self.gepir_router = gepir_router  # type: Optional[GEPIRRouter]
        super().__init__(xml=xml, tag=tag)


class MemberOrganisation(SOAPElement):

    elements_properties = OrderedDict([
        ('countryAdministered', ('country_administered', CountryCode)),
        ('lastChangeDate', ('last_change_date', datetime)),
        ('returnCode', ('return_code', GEPIRReturnCode)),
        ('url', ('url', str)),
        ('gepirCountry', ('gepir_country', GEPIRCountry)),
        ('informationProvider', ('information_provider', GEPIRPartyInformation)),
        ('prefixRange', ('prefix_range', PrefixRange)),
        ('gepirInformation', ('gepir_information', GEPIRInformation)),
        ('contact', ('contact', Contact)),
        ('address', ('address', Address)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='memberOrganisation',  # type: str
        country_administered=None,  # type: Optional[CountryCode]
        last_change_date=None,  # type: Optional[datetime]
        return_code=None,  # type: Optional[GEPIRReturnCode]
        url=None,  # type: Optional[str]
        gepir_country=None,  # type: Optional[GEPIRCountry]
        information_provider=None,  # type: Optional[GEPIRPartyInformation]
        prefix_range=None,  # type: Optional[PrefixRange]
        gepir_information=None,  # type: Optional[GEPIRInformation]
        contact=None,  # type: Optional[Contact]
        address=None,  # type: Optional[Address]
    ):
        self.country_administered = country_administered  # type: Optional[str]
        self.last_change_date = last_change_date  # type: Optional[datetime]
        self.return_code = return_code,  # type: Optional[GEPIRReturnCode]
        self.url = url  # type: Optional[str]
        self.gepir_country = gepir_country  # type: Optional[GEPIRCountry]
        self.information_provider = information_provider  # type: Optional[GEPIRPartyInformation]
        self.prefix_range = prefix_range  # type: Optional[PrefixRange]
        self.gepir_information = gepir_information  # type: Optional[GEPIRInformation]
        self.contact = contact  # type: Optional[Contact]
        self.address = address  # type: Optional[Address]
        super().__init__(xml=xml, tag=tag)


class RootDirectory(SOAPElement):

    elements_properties = OrderedDict([
        ('rootDirectoryDataLanguage', ('root_directory_data_language', LanguageCode)),
        ('rootDirectoryVersion', ('root_directory_version', str)),
        ('memberOrganisation', ('member_organisation', (MemberOrganisation,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='rootDirectory',  # type: str
        root_directory_data_language=None,  # type: Optional[LanguageCode]
        root_directory_version=None,  # type: Optional[str]
        member_organisation=None,  # type: Optional[Sequence[MemberOrganisation]]
    ):
        self.root_directory_data_language = root_directory_data_language  # type: Optional[LanguageCode]
        self.root_directory_version = root_directory_version  # type: Optional[str]
        self.member_organisation = member_organisation or []  # type: Optional[MemberOrganisation]
        super().__init__(xml=xml, tag=tag)


class GetRootDirectory(SOAPElement):
    """
    Properties:
    
        - requester_router (str): Global Location Number (GLN) of the GEPIR router requesting the GEPIR Root Directory.
    """

    elements_properties = OrderedDict([
        ('requesterRouter', ('requester_router', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getRootDirectory',  # type: str
        requester_router=None  # type: Optional[str]
    ):
        self.requester_router = requester_router  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GetRouterDetail(SOAPElement):

    elements_properties = OrderedDict([
        ('requesterRouter', ('requester_router', str)),
        ('requestedRouter', ('requested_router', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getRouterDetail',  # type: str
        requester_router=None,  # type: Optional[str]
        requested_router=None  # type: Optional[str]
    ):
        self.requester_router = requester_router  # type: Optional[str]
        self.requested_router = requested_router  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class RouterDetail(SOAPElement):

    elements_properties = OrderedDict([
        ('routerDetailRefreshDate', ('router_detail_refresh_date', datetime)),
        ('requestedRouterDetail', ('requested_router_detail', MemberOrganisation)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='routerDetail',  # type: str
        router_detail_refresh_date=None,  # type: Optional[datetime]
        requested_router_detail=None  # type: Optional[MemberOrganisation]
    ):
        self.router_detail_refresh_date = router_detail_refresh_date  # type: Optional[str]
        self.requested_router_detail = requested_router_detail  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GetRootDirectoryRequest(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('getRootDirectory', ('get_root_directory', GetRootDirectory)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getRootDirectory',  # type: str
        get_root_directory=None  # type: Optional[str]
    ):
        self.get_root_directory = get_root_directory  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)
        super().__init__(xml=xml, tag=tag)


class GetRouterDetailRequest(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('getRouterDetail', ('get_router_detail', GetRouterDetail)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getRouterDetail',  # type: str
        get_router_detail=None  # type: Optional[str]
    ):
        self.get_router_detail = get_router_detail  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class GetRouterDetailResponse(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('routerDetail', ('router_detail', RouterDetail)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getRouterDetailResponse',  # type: str
        router_detail=None  # type: Optional[str]
    ):
        self.router_detail = router_detail  # type: Optional[RouterDetail]
        super().__init__(xml=xml, tag=tag)


class GetRootDirectoryResponse(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('rootDirectory', ('root_directory', RootDirectory)),
    ])


    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getRootDirectoryResponse',  # type: str
        root_directory=None  # type: Optional[RootDirectory]
    ):
        self.root_directory = root_directory  # type: Optional[RootDirectory]
        super().__init__(xml=xml, tag=tag)


class GEPIRGetPartyRequestParameters(SOAPElement):
    """
    Properties:
    
        - requested_city (str)
        - requested_country (CountryCode)
        - requested_language (LanguageCode)
        - requested_party_name (str)
        - requested_postal_code (str)
        - requested_street_address (str)
    """

    elements_properties = OrderedDict([
        ('requestedCity', ('requested_city', str)),
        ('requestedCountry', ('requested_country', CountryCode)),
        ('requestedLanguage', ('requested_language', LanguageCode)),
        ('requestedPartyName', ('requested_party_name', str)),
        ('requestedPostalCode', ('requested_postal_code', str)),
        ('requestedStreetAddress', ('requested_street_address', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepirGetPartyRequestParameters',  # type: str
        requested_city=None,  # type: Optional[str]
        requested_country=None,  # type: Optional[CountryCode]
        requested_language=None,  # type: Optional[LanguageCode]
        requested_party_name=None,  # type: Optional[str]
        requested_postal_code=None,  # type: Optional[str]
        requested_street_address=None  # type: Optional[str]
    ):
        if requested_country is not None:
            requested_country.tag = 'requestedCountry'
        if requested_language is not None:
            requested_language.tag = 'requestedLanguage'
        self.requested_city = requested_city
        self.requested_country = requested_country
        self.requested_language = requested_language
        self.requested_party_name = requested_party_name
        self.requested_postal_code = requested_postal_code
        self.requested_street_address = requested_street_address
        super().__init__(xml=xml, tag=tag)


class GetItemByGTINRequest(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('getItemByGTIN', ('get_item_by_gtin', GetItemByGTIN)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getItemByGTIN',  # type: str
        get_item_by_gtin=None,  # type: Optional[GetItemByGTIN]
    ):
        self.get_item_by_gtin = get_item_by_gtin
        super().__init__(xml=xml, tag=tag)


class GetItemByGTINResponse(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('gepirItem', ('gepir_item', (GEPIRItem,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getItemByGTINResponse',  # type: str
        gepir_item=None  # type: Optional[Union[Sequence[GEPIRItem], GEPIRItem]]
    ):
        self.gepir_item = gepir_item or []  # type: Optional[Sequence[GEPIRItem]]
        super().__init__(xml=xml, tag=tag)


class GetKeyLicensee(SOAPElement):

    elements_properties = OrderedDict([
        ('getKeyLicensee', ('get_key_licensee', (GEPIRRequestedKey,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getKeyLicensee',  # type: str
        get_key_licensee=None  # type: Optional[Union[Sequence[GEPIRRequestedKey], GEPIRRequestedKey]]
    ):
        if get_key_licensee:
            for gkl in get_key_licensee:
                gkl.tag = 'getKeyLicensee'
        self.get_key_licensee = get_key_licensee or []  # type: Sequence[GEPIRRequestedKey]
        super().__init__(xml=xml, tag=tag)


class GetKeyLicenseeRequest(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('getKeyLicensee', ('get_key_licensee', GetKeyLicensee)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getKeyLicensee',  # type: str
        get_key_licensee=None  # type: Optional[GetKeyLicensee]
    ):
        self.get_key_licensee = get_key_licensee  # type: Optional[GetKeyLicensee]
        super().__init__(xml=xml, tag=tag)


class GetPartyByName(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        (
            'getPartyByName/gepirGetPartyRequestParameters',
            ('gepir_get_party_request_parameters', GEPIRGetPartyRequestParameters)
        ),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getPartyByName',  # type: str
        gepir_get_party_request_parameters=None  # type: Optional[GEPIRGetPartyRequestParameters]
    ):
        self.gepir_get_party_request_parameters = (
            gepir_get_party_request_parameters
        )  # type: Optional[GEPIRGetPartyRequestParameters]
        super().__init__(xml=xml, tag=tag)


class GetPrefixLicensee(SOAPElement):

    elements_properties = OrderedDict([
        ('getPrefixLicensee', ('get_prefix_licensee', (GEPIRRequestedKey,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='getPrefixLicensee',  # type: str
        get_prefix_licensee=None  # type: Optional[Sequence[GEPIRRequestedKey]]
    ):
        if get_prefix_licensee:
            for gpl in get_prefix_licensee:
                gpl.tag = 'getPrefixLicensee'
        self.get_prefix_licensee = get_prefix_licensee or []  # type: Sequence[GEPIRRequestedKey]
        super().__init__(xml=xml, tag=tag)


class GetPrefixLicenseeRequest(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('getPrefixLicensee', ('get_prefix_licensee', GetPrefixLicensee)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getPrefixLicensee',  # type: str
        get_prefix_licensee=None  # type: Optional[GetPrefixLicensee]
    ):
        self.get_prefix_licensee = get_prefix_licensee  # type: Optional[GetPrefixLicensee]
        super().__init__(xml=xml, tag=tag)


class GetKeyLicenseeResponse(SOAPElement):
    """
    Parameters:
        
    - gepir_party (Sequence[GEPIRParty]): A sequence of objects containing information about a GEPIR party.
    """

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('gepirParty', ('gepir_party', (GEPIRParty,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getKeyLicenseeResponse',  # type: str
        gepir_party=None  # type: Optional[Sequence[GEPIRParty]]
    ):
        self.gepir_party = gepir_party or []  # type: Sequence[GEPIRParty]
        super().__init__(xml=xml, tag=tag)


class GetPrefixLicenseeResponse(SOAPElement):
    """
    Parameters:
        
    - gepir_party (Sequence[GEPIRParty]): A sequence of objects containing information about a GEPIR party.
    """

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('gepirParty', ('gepir_party', (GEPIRParty,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getPrefixLicenseeResponse',  # type: str
        gepir_party=None  # type: Optional[Sequence[GEPIRParty]]
    ):
        self.gepir_party = gepir_party or []  # type: Sequence[GEPIRParty]
        super().__init__(xml=xml, tag=tag)


class GetPartyByNameResponse(SOAPElement):
    """
    Parameters:
        
    - gepir_party (Sequence[GEPIRParty]): A sequence of objects containing information about a GEPIR party.
    """

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('gepirParty', ('gepir_party', (GEPIRParty,))),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:getPartyByNameResponse',  # type: str
        gepir_party=None  # type: Optional[Sequence[GEPIRParty]]
    ):
        self.gepir_party = gepir_party or []  # type: Sequence[GEPIRParty]
        super().__init__(xml=xml, tag=tag)


class RequestHeader(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('requesterGLN', ('requester_gln', str)),
        ('onBehalfOfGLN', ('on_behalf_of_gln', str)),
        ('isAuthenticated', ('is_authenticated', bool)),
        ('cascade', ('cascade', int))
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:requestHeader',  # type: str
        requester_gln=None,  # type: Optional[str]
        on_behalf_of_gln=None,  # type: Optional[str]
        is_authenticated=None,  # type: Optional[bool]
        cascade=None  # type: Optional[int]
    ):
        self.requester_gln = requester_gln  # type: Optional[str]
        self.on_behalf_of_gln = on_behalf_of_gln  # type: Optional[str]
        self.is_authenticated = is_authenticated  # type: Optional[bool]
        self.cascade = cascade  # type: Optional[int]
        super().__init__(xml=xml, tag=tag)


class ResponseHeader(SOAPElement):

    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('responderGLN', ('responder_gln', str)),
        ('numberOfHits', ('number_of_hits', int)),
        ('gepirReturnCode', ('gepir_return_code', GEPIRReturnCode)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='gepir:responseHeader',  # type: str
        responder_gln=None,  # type: Optional[str]
        number_of_hits=None,  # type: Optional[int]
        gepir_return_code=None  # type: Optional[GEPIRReturnCode]
    ):
        self.responder_gln = responder_gln  # type: Optional[str]
        self.number_of_hits = number_of_hits  # type: Optional[int]
        self.gepir_return_code = gepir_return_code  # type: Optional[GEPIRReturnCode]
        super().__init__(xml=xml, tag=tag)


class SubCode(SOAPElement):
    """
    Properties:
    
        - value (str)
        - sub_code (SubCode)
    """

    elements_properties = OrderedDict([
        ('Value', ('value', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str, HTTPResponse]]
        tag='Fault',  # type: str
        value=None,  # type: Optional[str]
        sub_code=None,  # type: Optional[SubCode]
    ):
        self.value = value  # type: Optional[str]
        self.sub_code = sub_code  # type: Optional[SubCode]
        super().__init__(xml=xml, tag=tag)


SubCode.elements_properties['Subcode'] = ('sub_code', SubCode)


class FaultCode(SOAPElement):
    """
    Properties:
    
        - value (str): Where "tns" is the target namespace (http://www.w3.org/2003/05/soap-envelope), valid values 
          include:
        
            + "tns:DataEncodingUnknown"
            + "tns:MustUnderstand"
            + "tns:Receiver"
            + "tns:Sender"
            + "tns:VersionMismatch"
            
        - sub_code (SubCode)
    """

    elements_properties = OrderedDict([
        ('Value', ('value', str)),
        ('Subcode', ('sub_code', SubCode)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str, HTTPResponse]]
        tag='Fault',  # type: str
        value=None,  # type: Optional[str]
        sub_code=None,  # type: Optional[SubCode]
    ):
        self.value = value  # type: Optional[str]
        self.sub_code = sub_code  # type: Optional[SubCode]
        super().__init__(xml=xml, tag=tag)


class FaultReason(SOAPElement):
    """
    Properties:
    
        - text (str)
        - lang (str)
    """

    elements_properties = OrderedDict([
        ('Text', ('text', str)),
        ('@lang', ('lang', str)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str, HTTPResponse]]
        tag='Fault',  # type: str
        text=None,  # type: Optional[str]
        lang=None,  # type: Optional[str]
    ):
        self.text = text  # type: Optional[str]
        self.lang = lang  # type: Optional[str]
        super().__init__(xml=xml, tag=tag)


class Fault(SOAPElement):

    elements_properties = OrderedDict([
        ('Code', ('code', FaultCode)),
        ('Reason', ('reason', FaultReason)),
        ('Node', ('node', str)),
        ('Role', ('role', str)),
        ('Detail', ('detail', Element)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str, HTTPResponse]]
        tag='Fault',  # type: str
        code=None,  # type: Optional[FaultCode]
        reason=None,  # type: Optional[FaultReason]
        node=None,  # type: Optional[str]
        role=None,  # type: Optional[str]
        detail=None,  # type: Optional[Element]
    ):
        self.code = code  # type: Optional[FaultCode]
        self.reason = reason  # type: Optional[FaultReason]
        self.node = node  # type: Optional[str]
        self.role = role  # type: Optional[str]
        self.detail = detail  # type: Optional[Element]
        super().__init__(xml=xml, tag=tag)


class Header(SOAPElement):

    elements_properties = OrderedDict([
        ('requestHeader', ('request_header', RequestHeader)),
        ('responseHeader', ('response_header', ResponseHeader)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]]
        tag='soap:Header',  # type: str
        request_header=None,  # type: Optional[RequestHeader]
        response_header=None,  # type: Optional[ResponseHeader]
    ):
        self.request_header = request_header
        self.response_header = response_header
        super().__init__(xml=xml, tag=tag)


class Body(SOAPElement):

    elements_properties = OrderedDict([
        ('getItemByGTIN', ('get_item_by_gtin', GetItemByGTINRequest)),
        ('getKeyLicensee', ('get_key_licensee', GetKeyLicenseeRequest)),
        ('getPartyByName', ('get_party_by_name', GetPartyByName)),
        ('getPrefixLicensee', ('get_prefix_licensee', GetPrefixLicenseeRequest)),
        ('getItemByGTINResponse', ('get_item_by_gtin_response', GetItemByGTINResponse)),
        ('getKeyLicenseeResponse', ('get_key_licensee_response', GetKeyLicenseeResponse)),
        ('getPartyByNameResponse', ('get_party_by_name_response', GetPartyByNameResponse)),
        ('getPrefixLicenseeResponse', ('get_prefix_licensee_response', GetPrefixLicenseeResponse)),
        ('getRootDirectory', ('get_root_directory', GetRootDirectoryRequest)),
        ('getRootDirectoryResponse', ('get_root_directory_response', GetRootDirectoryResponse)),
        ('getRouterDetail', ('get_router_detail', GetRouterDetailRequest)),
        ('getRouterDetailResponse', ('get_router_detail_response', GetRouterDetailResponse)),
        ('Fault', ('fault', Fault)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]],
        tag='soap:Body',  # type: str
        get_item_by_gtin=None,  # type: Optional[GetItemByGTINRequest]
        get_key_licensee=None,  # type: Optional[GetKeyLicenseeRequest]
        get_party_by_name=None,  # type: Optional[GetPartyByName]
        get_prefix_licensee=None,  # type: Optional[GetPrefixLicenseeRequest]
        get_item_by_gtin_response=None,  # type: Optional[GetItemByGTINResponse]
        get_key_licensee_response=None,  # type: Optional[GetKeyLicenseeResponse]
        get_party_by_name_response=None,  # type: Optional[GetPartyByNameResponse]
        get_prefix_licensee_response=None,  # type: Optional[GetPrefixLicenseeResponse]
        get_root_directory=None,  # type: Optional[GetRootDirectory]
        get_root_directory_response=None,  # type: Optional[GetRootDirectoryResponse]
        get_router_detail=None,  # type: Optional[GetRouterDetail]
        get_router_detail_response=None,  # type: Optional[GetRouterDetailResponse]
        fault=None,  # type: Optional[Fault]
    ):
        self.get_item_by_gtin = get_item_by_gtin  # type: Optional[GetItemByGTINRequest]
        self.get_key_licensee = get_key_licensee  # type: Optional[GetKeyLicenseeRequest]
        self.get_party_by_name = get_party_by_name  # type: Optional[GetPartyByName]
        self.get_prefix_licensee = get_prefix_licensee  # type: Optional[GetPrefixLicenseeRequest]
        self.get_item_by_gtin_response = get_item_by_gtin_response  # type: Optional[GetItemByGTINResponse]
        self.get_key_licensee_response = get_key_licensee_response  # type: Optional[GetKeyLicenseeResponse]
        self.get_party_by_name_response = get_party_by_name_response  # type: Optional[GetPartyByNameResponse]
        self.get_prefix_licensee_response = get_prefix_licensee_response  # type: Optional[GetPrefixLicenseeResponse]
        self.get_root_directory = get_root_directory  # type: Optional[GetRootDirectory]
        self.get_root_directory_response = get_root_directory_response  # type: Optional[GetRootDirectoryResponse]
        self.get_router_detail = get_router_detail  # type: Optional[GetRouterDetail]
        self.get_router_detail_response = get_router_detail_response  # type: Optional[GetRouterDetailResponse]
        self.fault = fault  # type: Optional[Fault]
        super().__init__(xml=xml, tag=tag)


class Envelope(SOAPElement):

    xmlns_soap = NAME_SPACES['soap']
    xmlns_gepir = NAME_SPACES['gepir']

    elements_properties = OrderedDict([
        ('@xmlns:soap', ('xmlns_soap', str)),
        ('@xmlns:gepir', ('xmlns_gepir', str)),
        ('Header', ('header', Header)),
        ('Body', ('body', Body)),
    ])

    def __init__(
        self,
        xml=None,  # type: Optional[Union[Element, str]],
        tag='soap:Envelope',  # type: str
        header=None,  # type: Optional[Header]
        body=None,  # type: Optional[Body]
    ):
        self.header = header  # type: Optional[Header]
        self.body = body  # type: Optional[Body]
        super().__init__(xml=xml, tag=tag)


if __name__ == "__main__":
    import doctest
    doctest.testmod()