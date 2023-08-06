gepir
=====

A python package for working with the `Global Electronic Party Information Registry (GEPIR)`_ SOAP API.

|
Requirements & Installation
---------------------------

- Python 3.4+ or...
- Python 2.7 *and* `pip`_

To install (in a terminal or command-prompt), execute:

.. code-block:: shell

    pip install gepir
|
Getting Started
---------------

To follow and execute subsequent code examples, you will need to import the following:

::

    from gepir import GEPIR
    from gepir.elements import GetKeyLicenseeResponse, GetPrefixLicenseeResponse, GetPartyByNameResponse, GEPIRParty,
    PartyDataLine, GEPIRItem, ItemDataLine

To "connect" to GEPIR's API, create an instance of the ``GEPIR`` class. Optional parameters include:

- **requester_gln** (*str*): The 13-digit Global Location Number (GLN) of the requesting organization. This defaults to
  "0000000000000" (which will work fine for making unauthenticated* requests).
- **router** (*str*): The URI of the router end-point to which requests should be passed. This defaults to the
  `GS1 Global Router`_.

\*Note: GS1 limits unauthenticated requests to 30 each day for any given IP address. See
`Mitigating Request Limits`_ for tips concerning how to make best use of these requests for common usage scenarios, and
how/where to obtain unrestricted (paid) access.

::

    gepir = GEPIR(
        requester_gln='0000000000000'
    )

An instance of ``GEPIR`` has 4 methods which will be useful to a typical user. The first three allow you to retrieve
"party" information (information about a GS1 registered entity, typically a company). The last method allows a user to
lookup item-specific information, however *item* information is not widely available in GEPIR at this time.

- `get_key_licensee`_
- `get_prefix_licensee`_
- `get_party_by_name`_
- `get_item_by_gtin`_

Additionally, two methods are only intended for use by a GEPIR Member Organization (MO), typically in cascading requests
to other nodes in the GEPIR network.

- `get_root_directory`_
- `get_router_detail`_
|
Requesting Company Information
------------------------------

.. _`get_key_licensee`:

The most common use for GEPIR is to lookup company ("party") information for a `Global Trade Item Number (GTIN)`_
licensee. This can be accomplished with ``GEPIR.get_key_licensee()``, which accepts the following parameters:

- **requested_key_code** (*str*): This key code indicates the type of data contained in the *requested_key_value*.

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

- **requested_key_value** (*str*): A value corresponding to the indicated *requested_key_code*.
- **requested_language** (*str*): A 2-3 digit language code (ISO 639), optionally followed by
  a hyphen and region code (ISO 15924).
- **get_key_licensee** (Sequence[`GEPIRRequestedKey`_]): If more than one set of the preceding parameters need to be
  incorporated into the same request, a series of `GEPIRRequestedKey`_ instances can be passed instead of,
  or in addition to, the previous 3 parameters.

The following parameters for ``GEPIR.get_key_licensee()`` are only intended for use by a GEPIR MO:

- **on_behalf_of_gln** (*str*): The GLN of the originator of the request. This remains unchanged if the request
  is cascaded to another server. This should only be populated by the initiating MO. This must be
  a valid, active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
  address, this field should be set to ``None``. Furthermore, even if the requester passes authentication,
  only known GEPIR nodes should be allowed to set this field.
- **is_authenticated** (*bool*): State of the incoming requester as to whether the user is a member in good
  standing or not. This should only be populated by the initiating MO (it is no longer assumed when a
  request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication
  fails on ``requester_gln`` + IP address, this field should be set to ``None``. Furthermore, even if the
  requester passes authentication, only known GEPIR nodes should be allowed to set this field.
- **cascade** (*int*): An integer between 0 and 9 indicating the number of times a request may be cascaded to
  another server. This element is decremented each time the request is passed on. A request with a cascade
  count of ``0`` must not be cascaded further.

``GEPIR.get_key_licensee()`` will return an instance of `GetKeyLicenseeResponse`_, a container element for a sequence of
`GEPIRParty`_ instances.

::

    gklr = gepir.get_key_licensee(
        requested_key_code='GTIN',
        requested_key_value='00037447250897'
    ) # type: GetKeyLicenseeResponse
    for gepir_party in gklr.gepir_party:  # type: GEPIRParty
        print(gepir_party)

This method can also be used to retrieve party information for additional GS1 keys, such as a
`Global Location Number (GLN)`_ licensee.

::

    gklr = gepir.get_key_licensee(
        requested_key_code='GLN',
        requested_key_value='0037447121067'
    )  # type: GetKeyLicenseeResponse
    for gepir_party in gklr.gepir_party:  # type: GEPIRParty
        print(gepir_party)

.. _`get_prefix_licensee`:

``GEPIR.get_prefix_licensee()`` is similar to ``GEPIR.get_key_licensee()`` (and accepts the same arguments), but it
only returns a GEPIR party if that party licenses the `Global Company Prefix (GCP)`_ corresponding to the key requested
(as opposed to licensing only the solitary key).

::

    gplr = gepir.get_prefix_licensee(
        requested_key_code='GTIN',
        requested_key_value='00037447250897'
    )  # type: GetPrefixLicenseeResponse
    for gepir_party in gplr.gepir_party:  # type: GEPIRParty
        print(gepir_party)

You will likely find the above method to be redundant, because it is possible to determine whether a `GEPIRParty`_
licenses the prefix, or only an individual GS1 key, by the presence or absence of a `gs1_company_prefix_licensee`_.

::

    for gtin in ('00037447250897',):
        gklr = gepir.get_key_licensee(
            requested_key_code='GTIN',
            requested_key_value=gtin
        )  # type: GetKeyLicenseeResponse
        for gepir_party in gklr.gepir_party:  # type: GEPIRParty
            for party_data_line in gepir_party.party_data_line:  # type: PartyDataLine
                if party_data_line.gs1_company_prefix_licensee is None:
                    print("This party is not the licensee of this key's GCP.")
                else:
                    print(
                        "This party *is* the licensee of this key's GCP: \n" +
                        str(party_data_line.gs1_company_prefix_licensee)
                    )

.. _`get_party_by_name`:

Lastly, information about a party can be retrieved based on a country and all or part of the company's name and
(optionally) additional locale information about the company, using ``GEPIR.get_party_by_name()``, which accepts the
following parameters:

- **requested_country** (*str*): A 2-digit country code (ISO 3166-1 alpha-2) indicating which country to search. By
  default, the code "ZZ" is used, which initiaes a *worldwide* search. A worldwide search takes significantly longer,
  however—so it is recommended that a country code be provided, when known.
- **requested_party_name** (*str*): All or part of the name of a party.
- **requested_street_address** (*str*): Find parties with this text in the address.
- **requested_city** (*str*): Find parties within this city.
- **requested_postal_code** (*str*): Find parties within this postal code.
- **requested_language** (*str*): (*A 2-digit or 3-digit language code*) Specifies the language of the request
  text-fields if the language is not the default language of the information provider.

The following parameters for ``GEPIR.get_party_by_name()`` are only intended for use by a GEPIR MO:

- **on_behalf_of_gln** (*str*): The GLN of the originator of the request. This remains unchanged if the request
  is cascaded to another server. This should only be populated by the initiating MO. This must be a valid,
  active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
  address, this field should be set to ``None``. Furthermore, even if the requester passes authentication,
  only known GEPIR nodes should be allowed to set this field.
- **is_authenticated** (*bool*): State of the incoming requester as to whether the user is a member in good
  standing or not. This should only be populated by the initiating MO (it is no longer assumed when a
  request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication
  fails on ``requester_gln`` + IP address, this field should be set to ``None``. Furthermore, even if the
  requester passes authentication, only known GEPIR nodes should be allowed to set this field.
- **cascade** (*int*): An integer between 0 and 9 indicating the number of times a request may be cascaded to
  another server. This element is decremented each time the request is passed on. A request with a cascade
  count of ``0`` must not be cascaded further.

::

    for country, company, city in (
        ('US', 'Leatherman', 'Portland'),
    ):
        gpbnr = gepir.get_party_by_name(
            country,
            company,
            requested_city=city
        )  # type: GetPartyByNameResponse
        for gepir_party in gpbnr.gepir_party:  # type: GEPIRParty
            print(gepir_party)
|
Requesting Item Information
---------------------------

.. _`get_item_by_gtin`:

Item information is not *widely* available in GEPIR at this time, however it can be queried using
``GEPIR.get_item_by_gtin()``, which accepts the following parameters:

- **requested_gtin** (*str*): A 14 digit global trade item number.
- **requested_language** (*str*): (*A 2-digit or 3-digit language code*) Specifies the language of the request
  text-fields if the language is not the default language of the information provider.

The following parameters for ``GEPIR.get_item_by_gtin()`` are only intended for use by a GEPIR MO:

- **on_behalf_of_gln** (*str*): The GLN of the originator of the request. This remains unchanged if the request
  is cascaded to another server. This should only be populated by the initiating MO. This must be a valid,
  active GLN. To prevent spoofing, if the GEPIR Premium authentication fails on ``requester_gln`` + IP
  address, this field should be set to ``None``. Furthermore, even if the requester passes authentication,
  only known GEPIR nodes should be allowed to set this field.
- **is_authenticated** (*bool*): State of the incoming requestor as to whether the user is a member in good
  standing or not. This should only be populated by the initiating MO (it is no longer assumed when a
  request comes from an initiating trusted router). To prevent spoofing, if the GEPIR Premium authentication
  fails on ``requester_gln`` + IP address, this field should be set to ``None``. Furthermore, even if the
  requester passes authentication, only known GEPIR nodes should be allowed to set this field.
- **cascade** (*int*): An integer between 0 and 9 indicating the number of times a request may be cascaded to
  another server. This element is decremented each time the request is passed on. A request with a cascade
  count of ``0`` must not be cascaded further.

::

    gibgr = gepir.get_item_by_gtin(
        requested_gtin='04760000100013'
    )  # type: GetItemByGTINResponse
    for gepir_item in gibgr.gepir_item:  # type: GEPIRItem
        for item_data_line in gepir_item.item_data_line:  # type: ItemDataLine
            print(item_data_line)

|
Interpreting a GEPIR Response
-----------------------------

The following classes, representing elements from which a GEPIR response is composed, can be found in the module
``gepir.elements``.

=============================== ========================================================================================
Class                           **Properties** (*types*)
=============================== ========================================================================================
_`GetKeyLicenseeResponse`       - **gepir_party** (Sequence[`GEPIRParty`_]): A sequence of objects containing
                                  information about a GEPIR party. Each `GEPIRParty`_ represents *one* party (company).
------------------------------- ----------------------------------------------------------------------------------------
_`GetPrefixLicenseeResponse`    - **gepir_party** (Sequence[`GEPIRParty`_]): A sequence of objects containing
                                  information about a GEPIR party. Each `GEPIRParty`_ represents *one* trade item.
------------------------------- ----------------------------------------------------------------------------------------
_`GetPartyByNameResponse`       - **gepir_party** (Sequence[`GEPIRParty`_]): A sequence of objects containing
                                  information about a GEPIR party. Each `GEPIRParty`_ represents *one* party (company).
------------------------------- ----------------------------------------------------------------------------------------
_`GetItemByGTINResponse`        - **gepir_party** (Sequence[`GEPIRItem`_]): A sequence of objects containing
                                  information about a trade item. Each `GEPIRItem`_ represents *one* trade item.
------------------------------- ----------------------------------------------------------------------------------------
_`GEPIRParty`                   - **party_data_line** (Sequence[`PartyDataLine`_]): A sequence of objects containing
                                  information about a party (company). Each data line represents the party information
                                  available for this request from one node in the GEPIR network (one MO).
------------------------------- ----------------------------------------------------------------------------------------
_`PartyDataLine`                - **last_change_date** (*datetime*): A date assigned by the system indicating the last
                                  time this information was altered.
                                - **gs1_company_prefix** (*str*): The GS1 Company Prefix of the GS1 key being requested.
                                - **information_provider** (`GEPIRPartyInformation`_): Party information about the
                                  originator of this response line.
                                - **party_data_language** (*str*): Indicates the language used to represent data in this
                                  response line.
                                - **return_code** (`GEPIRReturnCode`_): Indicates the success or failure of a request.
                                - **address** (`Address`_): A location at which representatives of this party may be
                                  reached.
                                - **gepir_requested_key** (`GEPIRRequestedKey`_): Details about the requested GS1 key.
                                  This can be useful when multiple keys are queried in the same request.
                                - **gepir_item_external_file_link** (Sequence[`ExternalFileLink`_]): One or more
                                  references to related electronic files.
                                - **responder_specific_data** (`ResponderSpecificData`_): A user-defined field for
                                  passing additional information about this party.
                                - **gs1_company_prefix_licensee** (`GEPIRPartyInformation`_): Information about the
                                  party licensing the prefix contained in the referenced GS1 key. This will be absent
                                  when a solitary key has been licensed (a very uncommon scenario), as opposed to a
                                  prefix.
                                - **gs1_key_licensee** (`GEPIRPartyInformation`_): Information about the party licensing
                                  the referenced GS1 key.
                                - **information_provider** (`GEPIRPartyInformation`_): Information about the party from
                                  whom this response line originates.
                                - **contact** (Sequence[`Contact`_]): Information about a individuals or departments
                                  acting as a contact for this organization.
------------------------------- ----------------------------------------------------------------------------------------
_`GEPIRReturnCode`              - **text** (*str*): "0" indicates success, all other values indicate an error has
                                  occurred.

                                  + "0" (Query Successful): The request has been successfully completed and the response
                                    is in the body of the message.
                                  + "1" (Missing or invalid parameters): One or more parameters are missing or
                                    incorrect. This might be and  incorrect length, invalid check digit, a non-numeric
                                    characters in a number, etc. No data is returned.
                                  + "2" (PhoneBookRecord not found): No record exists for this key or these search parameters. No
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

                                - **code_list_version** (*str*): Which snapshot of the code-list was this code taken
                                  from?
=============================== ========================================================================================

|
Mitigating Request Limits
-------------------------

References
----------

- `GEPIR 4.0 Specifications`_
- `GEPIR 4.0 WSDL`_

.. _`pip`: https://pip.pypa.io/en/stable/installing/
.. _`Global Electronic Party Information Registry (GEPIR)`: http://gepir.gs1.org/
.. _`GS1 Global Router`: http://gepir4ws.gs1.org:8080/gepir/services/Gepir4xServicePort?WSDL
.. _`GEPIR 4.0 Specifications`: https://www.gepir.de/docs/GS1_GEPIR_SPECIFICATIONS_VERSION4.0.0_d0_0_13_151015.pdf
.. _`GEPIR 4.0 WSDL`: http://gepir4ws.gs1.org:8080/gepir/services/Gepir4xServicePort?WSDL
.. _`Global Trade Item Number (GTIN)`: http://www.gtin.info
.. _`Global Company Prefix (GCP)`: http://www.gs1.org/company-prefix
.. _`Global Location Number (GLN)`: http://www.gs1.org/gln