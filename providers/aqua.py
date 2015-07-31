#! /usr/bin/python3

import re
import requests

def getBalance(security_info, account_number):
    # create a session to store all our cookies etc. in
    session = requests.Session()

    # send first part of login request (internet ID and last name) to aqua
    payload = {
        '__VIEWSTATE': '/wEPDwUKLTU4NTgxOTI5OA9kFgRmD2QWAmYPFgIeBGhyZWYFKS9+L21lZGlhL0FxdWEvZ3JhcGhpY3MvaWNvbnMvZmF2aWNvbi5hc2h4ZAIBEBYCHgpvbmtleXByZXNzBWFqYXZhc2NyaXB0OnJldHVybiBXZWJGb3JtX0ZpcmVEZWZhdWx0QnV0dG9uKGV2ZW50LCAnVGFyZ2V0XzVkMTk2YjMzLWUzMGYtNDQyZi1hMDc0LTFmZTk3Yzc0NzQ3NCcpZBYCAgMPFgQeA3NyYwU0L34vbWVkaWEvQXF1YS9ncmFwaGljcy9sb2dvcy9HZW5lcmljUHJpbnRIZWFkZXIuYXNoeB4DYWx0ZGRk',
        'datasource_3a4651d1-b379-4f77-a6b1-5a1a4855a9fd': security_info['internet id'],
        'datasource_2e7ba395-e972-4a25-8d19-9364a6f06132': security_info['last name'],
        'Target_5d196b33-e30f-442f-a074-1fe97c747474': 'Next'
    }
    r = session.post("https://service.aquacard.co.uk/aqua/web_channel/cards/security/logon/logon.aspx", headers={'Referer': 'https://service.aquacard.co.uk/aqua/web_channel/cards/security/logon/logon.aspx'}, data=payload)

    # work out which digits from the passcode we need to send
    firstDigitMatch = re.search('selectedvalue_dc28fef3-036f-4e48-98a0-586c9a4fbb3c.index_(\d)', r.text)
    if firstDigitMatch:
        firstPasscodeDigit = security_info['passcode'][int(firstDigitMatch.group(1))-1] # strings start at 0
    else:
        raise LookupError ('Error: couldn\'t find the first digit of the passcode which was being requested. Potentially useful debug information: ' + r.text)

    secondDigitMatch = re.search('selectedvalue_f758fdb6-4b2c-4272-b785-cb3989b67901.index_(\d)', r.text)
    if secondDigitMatch:
        secondPasscodeDigit = security_info['passcode'][int(secondDigitMatch.group(1))-1] # strings start at 0
    else:
        raise LookupError ('Error: couldn\'t find the second digit of the passcode which was being requested. Potentially useful debug information: ' + r.text)

    # send second part of login request (memorable word and two digits from passcode) to aqua
    payload = {
        '__VIEWSTATE': '/wEPDwUKLTU4NTgxOTI5OA9kFgRmD2QWAmYPFgIeBGhyZWYFKS9+L21lZGlhL0FxdWEvZ3JhcGhpY3MvaWNvbnMvZmF2aWNvbi5hc2h4ZAIBEBYCHgpvbmtleXByZXNzBWFqYXZhc2NyaXB0OnJldHVybiBXZWJGb3JtX0ZpcmVEZWZhdWx0QnV0dG9uKGV2ZW50LCAnVGFyZ2V0XzUzYWI3OGQzLTc4ZWQtNDZmMS1hNzc3LTFmZDc5NTdlMTE2NScpZBYCAgMPFgQeA3NyYwU0L34vbWVkaWEvQXF1YS9ncmFwaGljcy9sb2dvcy9HZW5lcmljUHJpbnRIZWFkZXIuYXNoeB4DYWx0ZGRk',
        'Target_53ab78d3-78ed-46f1-a777-1fd7957e1165': '',
        'datasource_20056b2c-9455-4e42-aeba-9351afe0dbe1': security_info['memorable word'],
        'selectedvalue_dc28fef3-036f-4e48-98a0-586c9a4fbb3c': firstPasscodeDigit,
        'selectedvalue_f758fdb6-4b2c-4272-b785-cb3989b67901': secondPasscodeDigit
    }
    r = session.post("https://service.aquacard.co.uk/aqua/web_channel/cards/security/logon/credentials.aspx", headers={'Referer': 'https://service.aquacard.co.uk/aqua/web_channel/cards/security/logon/credentials.aspx'}, data=payload)

    # use a regex to extract the balance
    balanceMatch = re.search('<strong>Current balance</strong></th><td class="amount"><strong>£(.*?)</strong></td>', r.text)
    if balanceMatch:
        typeMatch = re.search('<td class="creditdebit"><acronym title="(.*?)">', r.text)
        if typeMatch:
            balanceType = typeMatch.group(1)
            if balanceType == 'debit':
                return float('-' + balanceMatch.group(1))
            elif balanceType == 'credit':
                return float(balanceMatch.group(1))
            else:
                raise ValueError ('An unknown balance type (' + balanceType + ') was reported.')
        else:
            raise LookupError ('No balance type matched. Potentially useful debug information: ' + r.text)
    else:
        raise LookupError ('No balance matched. Potentially useful debug information: ' + r.text)
