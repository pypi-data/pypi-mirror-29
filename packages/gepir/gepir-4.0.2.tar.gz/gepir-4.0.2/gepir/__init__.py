from __future__ import absolute_import, division, print_function, unicode_literals

from future import standard_library

standard_library.install_aliases()

from builtins import *

from copy import copy
from xml.etree.ElementTree import ParseError

from urllib.error import HTTPError
from urllib.request import Request, urlopen

from gepir.elements import Envelope, Header, Body, GetItemByGTIN, RequestHeader, GetKeyLicensee, \
    GetPrefixLicensee, GEPIRItem, LanguageCode, GetPartyByName, CountryCode, GEPIRGetPartyRequestParameters, \
    GEPIRRequestedKey, ItemDataLine, GetItemByGTINRequest, GetKeyLicenseeRequest, GetPrefixLicenseeRequest, \
    GetRootDirectory, GetRootDirectoryRequest, GetRouterDetail, GetRouterDetailRequest, GetRouterDetailResponse, \
    GetKeyLicenseeResponse
from gepir.elements import RequestedKeyCode
from gepir.errors import RETURN_CODES_EXCEPTIONS, FAULT_CODES_ERRORS, Fault

try:
    from typing import Sequence, Union, Optional
except ImportError:
    pass

MONITORING = 'http://staging.gepir.ch/faq/serverstatus/Monitoring/'


class GEPIR(object):
    """
    Methods:
        
        For unauthenticated users:
        
            - get_item_by_gtin 
            - get_party_by_name
            - get_key_licensee
            - get_prefix_licensee
            
        For authenticated GEPIR MO's:
        
            - get_root_directory
            - get_router_detail
    """

    def __init__(
        self,
        requester_gln='0000000000000',  # type: Optional[str]
        router='http://gepir4ws.gs1.org:8080/gepir/services/Gepir4xServicePort'  # type: str
    ):
        """
        Parameters:
            
            - requester_gln (str): The 13-digit Global Location Number (GLN) of the requesting organization.
            - router: The URI of the router end-point to which requests should be passed. 
        """
        self.requester_gln = requester_gln  # type: str
        self.router = router  # type: str

    @property
    def host(self):
        return self.router.split('://')[1].split('/')[0]

    @property
    def wsdl(self):
        return self.router + '?WSDL'

    def request(
        self,
        body,  # type: Union[Body, str]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> Envelope
        """
        This method accepts a SOAP ``Body`` element and returns a SOAP ``Envelope``. This method is intended for use by
        message-specific methods ``GEPIR.get_item_by_gtin()``, ``GEPIR.get_key_licensee()``, 
        ``GEPIR.get_prefix_licensee()``, ``GEPIR.get_root_directory()``, and ``GEPIR.get_router_detail()``.
        
        Parameters:
            
            - body (Body): The SOAP ``Body`` of the request.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        request_header = RequestHeader(
            requester_gln=self.requester_gln,
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        )
        envelope = Envelope(
            header=Header(
                request_header=request_header
            ),
            body=body
        )
        if isinstance(envelope, str):
            envelope = Envelope(envelope)
        data = bytes(
            str(envelope),
            encoding='utf-8'
        )
        request = Request(
            self.router,
            headers={
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/soap+xml;charset=UTF-8',
                'Host': self.host
            },
            data=data
        )

        def request_text():
            s = str(request.data, encoding='utf-8')
            return (
                ('\n%s: %s\n' % (request.get_method(), self.router)) +
                '\n'.join(
                    '%s: %s' % (k, v)
                    for k, v in request.header_items()
                ) + (
                    ('\n' + s)
                    if request.data is not None
                    else ''
                )
            )

        try:
            response = urlopen(request)
        except HTTPError as e:
            data = e.file.read()
            try:
                s = str(data, encoding='utf-8')
                envelope = Envelope(s)
                fault = envelope.body.fault
                if fault is None:
                    e.msg = (
                        'Request:\n\n\t' +
                        request_text() +
                        '\n\nResponse:\n\n\t' +
                        s +
                        '\n\n' +
                        e.msg
                    )
                    raise e
                else:
                    fault_code = fault.code.value.split(':')[-1].split('.')[0]
                    if fault_code in FAULT_CODES_ERRORS:
                        raise FAULT_CODES_ERRORS[fault_code](
                            envelope=envelope,
                            request=request
                        )
                    else:
                        raise Fault(envelope=envelope, request=request)
            except ParseError:
                raise e
        s = str(
            response.read(),
            encoding='utf-8'
        )
        envelope = Envelope(s)
        if envelope.header.response_header is not None:
            return_code = envelope.header.response_header.gepir_return_code.text.strip()
            if return_code in RETURN_CODES_EXCEPTIONS:
                raise RETURN_CODES_EXCEPTIONS[return_code](
                    envelope=str(envelope)
                )
        return envelope

    def get_item_by_gtin(
        self,
        requested_gtin,  # type: Union[Sequence[str], str]
        requested_language=None,  # type: Optional[Union[str, LanguageCode]]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetItemByGTINResponse
        """
        This method retrieves item information for a GTIN. Note: Most items do not have item information available in 
        GEPIR at this time.
        
        Parameters:
            
            - requested_gtin (str): A 14 digit global trade item number.
            - requested_language (str): A 2 or 3-digit language code.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        if isinstance(requested_gtin, str):
            requested_gtin = (requested_gtin,)
        if requested_language is not None:
            if isinstance(requested_language, str):
                requested_language = LanguageCode(
                    text=requested_language,
                    tag='requestedLanguage'
                )
            elif isinstance(requested_language, LanguageCode):
                requested_language = copy(requested_language)
                requested_language.tag = 'requestedLanguage'
        return self.request(
            Body(
                get_item_by_gtin=GetItemByGTINRequest(
                    get_item_by_gtin=GetItemByGTIN(
                        requested_gtin=requested_gtin,
                        requested_language=requested_language
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_item_by_gtin_response

    def get_party_by_name(
        self,
        requested_party_name,  # type: str
        requested_country='ZZ',  # type: Optional[str]
        requested_street_address=None,  # type: Optional[str]
        requested_city=None,  # type: Optional[str]
        requested_postal_code=None,  # type: Optional[str]
        requested_language=None,  # type: Optional[str]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetPartyByNameResponse
        """
        Retrieve information about a party given a full or partial company name, a 2-digit country code, and
        (optionally) more specific locale information.
         
        Parameters:
            
            - requested_country (str): (*str*): A 2-digit country code (ISO 3166-1 alpha-2) indicating which country to
              search. By default, the code "ZZ" is used, which initiaes a *worldwide* search. A worldwide search takes
              significantly longer, however—so it is recommended that a country code be provided, when known.
            - requested_party_name (str): Find parties where the party name contains this text.
            - requested_street_address (str): Find parties with this text in the address.
            - requested_city (str): Find parties within this city.
            - requested_postal_code (str): Find parties within this postal code.
            - requested_language: (A 2-digit or 3-digit language code) Return responses in this language.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        if isinstance(requested_country, str):
            requested_country = CountryCode(
                text=requested_country
            )
        if isinstance(requested_language, str):
            requested_language = LanguageCode(
                text=requested_language
            )
        return self.request(
            Body(
                get_party_by_name=GetPartyByName(
                    gepir_get_party_request_parameters=GEPIRGetPartyRequestParameters(
                        requested_city=requested_city,
                        requested_country=requested_country,
                        requested_language=requested_language,
                        requested_party_name=requested_party_name,
                        requested_postal_code=requested_postal_code,
                        requested_street_address=requested_street_address
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_party_by_name_response

    def get_key_licensee(
        self,
        requested_key_code=None,  # type: Optional[str]
        requested_key_value=None,  # type: Optional[str]
        requested_language=None,  # type: Optional[str]
        get_key_licensee=None,  # type: Union[GEPIRRequestedKey, Sequence[GEPIRRequestedKey]]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetKeyLicenseeResponse
        """
        This method retrieves party information for the licensee of a GS1 key (such as a *GTIN* or *GLN*).
        
        Parameters:
        
            - requested_key_code (str): This key code indicates the type of data contained in the 
              ``requested_key_value``.
    
              + "GTIN": A 14-digit Global Trade Item Number (GTIN), composed of numneric digits only.
              + "GLN": A 13-digit Global Location Number (GLN), composed of numeric digits only.
              + "SSCC": An 18-digit Serial Shipping Container Code (SSCC), composed of numeric digits only.
              + "GRAI": A 13-digit Global Returnable Asset Identifier (GRAI), composed of numeric digits only.
              + "GIAI": A 30-digit Global Individual Asset Identifier (GIAI), composed of numeric digits only.
              + "GSRN": An 18-digit Global Service Relation Number (GSRN), composed of numeric digits only.
              + "GDTI": A 13-digit Global Document Type Identifier (GDTI), composed of numeric digits only.
              + "GSIN": A 17-digit Global Shipment Identification Number (GSIN), composed of numeric digits only.
              + "GINC": A 30-digit Global Identification Number for Consignment (GINC), composed of numeric digits 
                only.
              + "GCN": A 13-digit Global Coupon Number (GCN), composed of numeric digits only.
                
            - requested_key_value (str): A value corresponding to the indicated ``requested_key_code``.
            - requested_language (str): A 2-3 digit language code (ISO 639), optionally followed by
              a hyphen and region code (ISO 15924).
            - get_key_licensee (Sequence[GEPIRRequestedKey]): If more than one set of the preceding parameters need to 
              be incoorporated into the same request, a series of ``GEPIRRequestedKey`` instances can be passed instaed
              of, or in addition to, the previous 3 parameters. 
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        if isinstance(get_key_licensee, GEPIRRequestedKey):
            get_key_licensee = (get_key_licensee,)
        if isinstance(requested_language, str):
            requested_language = LanguageCode(
                text=requested_language
            )
        if get_key_licensee is None:
            get_key_licensee = []
        if (
            requested_key_code is not None or
            requested_key_value is not None or
            requested_language is not None
        ):
            if isinstance(requested_key_code, str):
                requested_key_code = RequestedKeyCode(
                    text=requested_key_code
                )
            get_key_licensee.append(
                GEPIRRequestedKey(
                    requested_key_code=requested_key_code,
                    requested_key_value=requested_key_value,
                    requested_language=requested_language
                )
            )
        return self.request(
            Body(
                get_key_licensee=GetKeyLicenseeRequest(
                    get_key_licensee=GetKeyLicensee(
                        get_key_licensee=get_key_licensee
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_key_licensee_response

    def get_prefix_licensee(
        self,
        requested_key_code=None,  # type: Optional[str]
        requested_key_value=None,  # type: Optional[str]
        requested_language=None,  # type: Optional[str]
        requested_keys=None,  # type: Union[GEPIRRequestedKey, Sequence[GEPIRRequestedKey]]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetPrefixLicensee
        """
        This method retrieves party information for the company/organization associated with *all items* sharing the
        same prefix (GCP) of a given GS1 identifier (such as a *GTIN* or *GLN*).
        
        Parameters:
        
            - requested_key_code (str): This key code indicates the type of data contained in the 
              ``requested_key_value``.
    
                + "GTIN": A 14-digit Global Trade Item Number (GTIN), composed of numneric digits only.
                + "GLN": A 13-digit Global Location Number (GLN), composed of numeric digits only.
                + "SSCC": An 18-digit Serial Shipping Container Code (SSCC), composed of numeric digits only.
                + "GRAI": A 13-digit Global Returnable Asset Identifier (GRAI), composed of numeric digits only.
                + "GIAI": A 30-digit Global Individual Asset Identifier (GIAI), composed of numeric digits only.
                + "GSRN": An 18-digit Global Service Relation Number (GSRN), composed of numeric digits only.
                + "GDTI": A 13-digit Global Document Type Identifier (GDTI), composed of numeric digits only.
                + "GSIN": A 17-digit Global Shipment Identification Number (GSIN), composed of numeric digits only.
                + "GINC": A 30-digit Global Identification Number for Consignment (GINC), composed of numeric digits 
                  only.
                + "GCN": A 13-digit Global Coupon Number (GCN), composed of numeric digits only.
                
            - requested_key_value (str): A value corresponding to the indicated ``requested_key_code``.
            - requested_language (str): A 2-3 digit language code (ISO 639), optionally followed by
              a hyphen and region code (ISO 15924).
            - get_key_licensee (Sequence[GEPIRRequestedKey]): If more than one set of parameters need to be
              incoorporated into the same request, a series of ``GEPIRRequestedKey`` instances can be passed instaed of,
              or in addition to, the previous 3 parameters.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further. 
        """
        if isinstance(requested_keys, GEPIRRequestedKey):
            requested_keys = (requested_keys,)
        if requested_language is not None:
            if isinstance(requested_language, str):
                requested_language = LanguageCode(
                    text=requested_language,
                    tag='requestedLanguage'
                )
            elif isinstance(requested_language, LanguageCode):
                requested_language = copy(requested_language)
                requested_language.tag = 'requestedLanguage'
        if requested_keys is None:
            requested_keys = []
        if (
            requested_key_code is not None or
            requested_key_value is not None or
            requested_language is not None
        ):
            if isinstance(requested_key_code, str):
                requested_key_code = RequestedKeyCode(
                    text=requested_key_code
                )
            requested_keys.append(
                GEPIRRequestedKey(
                    requested_key_code=requested_key_code,
                    requested_key_value=requested_key_value,
                    requested_language=requested_language
                )
            )
        return self.request(
            Body(
                get_prefix_licensee=GetPrefixLicenseeRequest(
                    get_prefix_licensee=GetPrefixLicensee(
                        get_prefix_licensee=requested_keys
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_prefix_licensee_response

    def get_root_directory(
        self,
        requester_router=None,  # type: Optional[str]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetRootDirectoryResponse
        """
        Requests information concerning the GEPIR root directory. This request may only be performed by authenticated  
        GEPIR routers.
        
        Parameters:
            
            - requester_router (str): Global Location Number (GLN) of the router initiating this request.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        return self.request(
            Body(
                get_root_directory=GetRootDirectoryRequest(
                    get_root_directory=GetRootDirectory(
                        requester_router=requester_router
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_root_directory_response

    def get_router_detail(
        self,
        requester_router=None,  # type: Optional[str]
        requested_router=None,  # type: Optional[str]
        on_behalf_of_gln=None,  # type: Optional[str]
        cascade=9,  # type: int
        is_authenticated=False,  # type: Optional[bool]
    ):
        # type: (...) -> GetRouterDetailResponse
        """
        This request may only be performed by authenticated GEPIR routers.
        
        Parameters:
            
            - requester_router (str): The Global Location Number (GLN) of the GEPIR router initiating this request.
            - requested_router (str): The Global Location Number (GLN) of the GEPIR router concerning which details are 
              requested.
            - on_behalf_of_gln (str): The GLN of the originator of the request. This remains unchanged if the request 
              is cascaded to another server. This should only be populated by the initiating MO. This must be a valid, 
              active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
              address, this field should be set to null. Furthermore, even if the requester passes authentication, 
              only known GEPIR nodes should be allowed to set this field.
            - is_authenticated (bool): State of the incoming requestor as to whether the user is a member in good 
              standing or not. This should only be populated by the initiating MO (it is no longer assumed when a 
              request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication  
              fails on ``requester_gln`` + IP address, this field should be set to null. Furthermore, even if the   
              requester passes authentication, only known GEPIR nodes should be allowed to set this field.
            - cascade (int): An integer between 0 and 9 indicating the number of times a request may be cascaded to 
              another server. This element is decremented each time the request is passed on. A request with a cascade
              count of zero must not be cascaded further.
        """
        return self.request(
            Body(
                get_router_detail=GetRouterDetailRequest(
                    get_router_detail=GetRouterDetail(
                        requester_router=requester_router,
                        requested_router=requested_router
                    )
                )
            ),
            on_behalf_of_gln=on_behalf_of_gln,
            is_authenticated=is_authenticated,
            cascade=cascade
        ).body.get_router_detail_response


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    gepir = GEPIR()
    print(gepir.get_key_licensee('GTIN', '00037447250897'))
