The Python FinTech package
==========================

This package contains all the functionality that is required to work with
EBICS, SEPA and other financial technologies. The usage has been realised
as simple as possible but also as flexible as necessary.

Features
--------

- Obtain bank account statements (incl. CAMT and MT940 parser)
- Create and submit SEPA credit transfers (pain.001)
- Create and submit SEPA direct debits CORE/B2B (pain.008)
- Mostly full SEPA support
- Automatic calculation of the lead time based on holidays and cut-off times
- Integrated mandate manager (beta)
- Plausibility check of IBAN and BIC
- Validation of payment orders against the SEPA Clearing Directory of the
  German Central Bank
- Bankcode/Account to IBAN converter according to the rules of the German
  Central Bank
- Currency converter
- DATEV converter (KNE)

The FinTech package provides you the possibility to manage all of your everyday
commercial banking activities such as credit transfers, direct debits or the
retrieval of bank account statements in a flexible and secure manner.

All modules can be used free of charge. Only the unlicensed version of the
EBICS module has few restrictions. The upload of SEPA documents is limited
to a maximum of five transactions and bank account statements can not be
retrieved for the last three days.

Examples
--------

Simple SEPA Credit Transfer (pain.001)
++++++++++++++++++++++++++++++++++++++

.. sourcecode:: python

    import fintech
    fintech.register()
    from fintech.sepa import Account, SEPACreditTransfer
    
    # Create the debtor account from an IBAN
    debtor = Account('DE89370400440532013000', 'Max Mustermann')
    # Create the creditor account from a tuple (IBAN, BIC)
    creditor = Account(('AT611904300234573201', 'BKAUATWW'), 'Maria Musterfrau')
    # Create a SEPACreditTransfer instance
    sct = SEPACreditTransfer(debtor)
    # Add the transaction
    tx = sct.add_transaction(creditor, 10.00, 'Purpose')
    # Render the SEPA document
    print(sct.render())
    
Simple SEPA Direct Debit (pain.008)
+++++++++++++++++++++++++++++++++++

.. sourcecode:: python

    import fintech
    fintech.register()
    from fintech.sepa import Account, SEPADirectDebit
    
    # Create the creditor account from a tuple (ACCOUNT, BANKCODE)
    creditor = Account(('532013000', '37040044'), 'Max Mustermann')
    # Assign the creditor id
    creditor.set_creditor_id('DE98ZZZ09999999999')
    # Create the debtor account from a tuple (IBAN, BIC)
    debtor = Account(('AT611904300234573201', 'BKAUATWW'), 'Maria Musterfrau')
    # For a SEPA direct debit a valid mandate is required
    debtor.set_mandate(mref='M00123456', signed='2014-02-01', recurrent=True)
    # Create a SEPADirectDebit instance of type CORE
    sdd = SEPADirectDebit(creditor, 'CORE')
    # Add the transaction
    tx = sdd.add_transaction(debtor, 10.00, 'Purpose')
    # Render the SEPA document
    print(sdd.render())

EBICS
+++++

.. sourcecode:: python
    
    import fintech
    fintech.register()
    from fintech.ebics import EbicsKeyRing, EbicsBank, EbicsUser, EbicsClient
    
    keyring = EbicsKeyRing(keys='~/mykeys', passphrase='mysecret')
    bank = EbicsBank(keyring=keyring, hostid='MYBANK', url='https://www.mybank.de/ebics')
    user = EbicsUser(keyring=keyring, partnerid='CUSTOMER123', userid='USER1')
    # Create new keys for this user
    user.create_keys(keyversion='A006', bitlength=2048)
    
    client = EbicsClient(bank, user)
    # Send the public electronic signature key to the bank.
    client.INI()
    # Send the public authentication and encryption keys to the bank.
    client.HIA()
    
    # Create an INI-letter which must be printed and sent to the bank.
    user.create_ini_letter(bankname='MyBank AG', path='~/ini_letter.pdf')

    # After the account has been activated the public bank keys
    # must be downloaded and checked for consistency.
    print(client.HPB())
    
    # Finally the bank keys must be activated.
    bank.activate_keys()
    
    # Download MT940 bank account statements
    data = client.STA(
        start='2014-02-01',
        end='2014-02-07',
        )
    client.confirm_download()


Changelog
---------

v4.4.1 [2018-03-09]
    - Added some logging

v4.4.0 [2018-03-08]
    - Added EbicsClient context manager (auto-confirm)
    - Added EbicsClient property suppress_no_data_error
    - Added some IBAN countries
    - Fixed unverified SSL connections (Py>=2.7.9)
    - Accept multiple NtryDtls nodes in CAMTDocument

v4.3.5 [2017-10-25]
    - Fixed a SEPA date issue.
    - MT940 parser: Accept all characters in purpose text even if defined as delimiter.
    - Fixed a distributed signature bug.

v4.3.4 [2017-08-10]
    - Added the fields *sum_credits* and *sum_debits* to the MT942 parser.
    - Fixed the handling of invalid times (24:00:00) in CAMT documents.
    - Added the possibility to specify custom order parameters for FDL/FUL.
    - Added further support for SEPA structured references.

v4.3.3 [2017-06-06]
    - Fixed a bug parsing CAMT52 documents.
    - Made the user for EbicsClient optional.
    - Fixed a bug in EbicsUser.create_ini_letter to correctly return bytes.
    - Added silent parameter to method EbicsBank.activate_keys.
    - Added the attributes reference_id and sequence_id to the CAMTDocument parser.
    - Now parses the transaction classification also for DK in addition to ZKA.

v4.3.2 [2017-03-30]
    - Minor bug fix parsing MT942 documents.
    - Minor bug fix creating self-signed certificates.
    - Fixed a problem with Python builts compiled without "--with-fpectl".

v4.3.1 [2017-02-06]
    - Fixed a bug of Account.set_mandate with named arguments.

v4.3.0 [2017-01-19]
    - PyOpenSSL is not longer required to support certificates.
    - Removed direct debit type COR1 and adjusted mandate sequence types.
      API changes:
      
      - OLD: Account.set_mandate(mref, signed, first, last)
      - NEW: Account.set_mandate(mref, signed, recurrent)
      - OLD: SEPADirectDebit(account, 'COR1', ...)
      - NEW: SEPADirectDebit(account, 'CORE', ...)

v4.2.4 [2017-01-17]
    - Added a check for DigestMethod algorithm.
    - Fixed a bug rejecting mandates signed more than three years ago.
    - Fixed minor bug in mt940 parser.
    
v4.2.3 [2016-10-27]
    - Fixed bug of wrong content type in EBICS module.
    - Added support for EBICS uploads that are approved manually via accompanying document.

v4.2.2 [2016-05-05]
    - Added timeout to EBICS requests.
    - Made BIC optional for SEPA transactions.
    - Added creditor id to InitgPty/OrgId for Spanish banks.
    - Added postal address to SEPA documents.
    - Added support for creditor reference numbers.

v4.2.1 [2015-08-20]
    - Added a check of the unicode variant (UCS2, UCS4) to setup.py.

v4.2.0 [2015-08-17]
    - Added the SEPA fields BREF, RREF, SQTP and RTCD to the MT940 parser.
    - Added a dictionary of possible return codes to the SEPA module.
    - Added the possibility to dynamically license additional EBICS users.
    - Fixed an encoding bug of non-ascii error messages under Python 2.
    - Fixed a bug swapping local and remote account for returned transactions
      by the CAMT parser.

v4.1.1 [2015-04-24]
    - Disabled output of license due to some difficulties with pip

v4.1.0 [2015-04-20]
    - Added support for other currencies in addition to EUR.
    - Added new Amount class with an integrated currency converter.
    - Now the SEPATransaction property *amount* is of type Amount.

v4.0.0 [2015-04-14]
    - Made the library Python 2/3 compatible.
    - Added support for the cryptography package in addition to PyCrypto.
    - Made the BIC optional for national transactions.
    - Added the originator id to SEPA documents in GB and IE.
    - Added a check to recognize transaction duplicates.
    - Added a CAMT parser.
    - Changed some attributes of SEPATransaction instances to be conform
      with the new CAMT parser:
    
      + Removed the property *id*.
      + Removed the property *account*, instead use the method *get_account()*.
      + Renamed the property *due_date* to *date*.
      + Renamed the property *ext_purpose* to *purpose_code*.
      + Changed the property *purpose*, now it is a tuple of strings.
      + Changed the property *amout*, now debits are signed negative.
    
    - Fixed the handling of invalid dates (eg. 2015-02-30) in MT940 and
      CAMT parsers.
    - Fixed a problem with the exception handling in IPython.
    - Some code improvements and minor bug fixes.

v3.0.3 [2015-02-05]
    - Fixed a bug in the XML to dictionary converter.
    - Fixed a bug in the path handler of the EbicsKeyRing class.

v3.0.2 [2015-01-29]
    - Fixed a bug handling bank keys with a small bit-length.
    - Added some tolerance to the MT940 parser and collect unknown structured
      fields.

v3.0.1 [2015-01-26]
    - Renamed the package from *ebics* to *fintech* and the module *client* to
      *ebics*.
    - Splitted the functionality of the class *EbicsClient* into the classes
      *EbicsClient*, *EbicsBank*, *EbicsUser* and *EbicsKeyRing*. Added the
      new class factory *EbicsClientCompat* for backwards compatibility.
    - Added basic support for EBICS protocol version 2.4 (H003).
    - Added support for certificates.
    - Added the order types FUL and FDL.
    - Added a French and English version of the INI-letter.
    - Added the order types PUB, HCA, HCS and H3K.
    - Added a check of remote SSL certificates against trusted CAs.
    - Fixed the broken functionality of distributed signatures.
    - Added a much faster PBKDF2 implementation.
    - Created a more tolerant MT940 parser.
    - Changed the API of *SEPACreditTransfer* and *SEPADirectDebit* to be more
      consistent and added support for different PAIN scheme versions.
    - Several bug fixes.

v2.1.2 [2014-10-26]
    - Fixed some bugs regarding the distributed signature

v2.1.1 [2014-10-26]
    - Fixed a bug throwing an exception in an unregistered version of PyEBICS.
    - Fixed bug of wrong *OrderParams* tag used by orders of the distributed
      signature.

v2.1.0 [2014-09-29]
    - Added some functionality based on the SCL Directory, published by the
      German Central Bank.

v2.0.3 [2014-09-11]
    - Fixed a bug refusing valid creditor ids.
    - Added a test to check DATEV parameters for invalid arguments.

v2.0.2 [2014-09-05]
    - Fixed a bug in some EBICS requests (missing parameter tag).
    - Fixed a bug in the MT940 parser.

v2.0.1 [2014-08-18]
    - Fixed a bug handling XML namespaces.
    - Changed the behaviour of the flag *parsed* of some methods. Now a
      structure of dictionaries is returned instead of an objectified XML
      object.
    - Changed the expected type of the *params* parameter. Now it must be
      a dictionary instead of a list of tuples.
    - Added support for distributed signatures (HVU, HVD, HVZ, HVT, HVE, HVS).

v1.3.0 [2014-07-29]
    - Fixed a few minor bugs.
    - Made the package available for Windows.

v1.2.0 [2014-05-23]
    - Added new DATEV module.
    - Fixed wrong XML position of UltmtCdtr node in SEPA documents.
    - Changed the order of the (BANKCODE, ACCOUNT) tuple to (ACCOUNT, BANKCODE)
      used by the Account initializer.

v1.1.25 [2014-02-22]
    - Minor bug fix of the module loader.

v1.1.24 [2014-02-21]
    - First public release.
