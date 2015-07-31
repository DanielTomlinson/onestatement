#! /usr/bin/python3

import re
import requests

def getBalance(security_info, account_number):
    # talk to American Express
    payload = {
        'Face': 'en_GB',
        'Logon': 'Logon',
        'acctSelected': 'Cards - Your Account',
        'acctSelectedURL': '/myca/logon/emea/action/LogLogonHandler?request_type=LogLogonHandler&location=us_logon1',
        'TARGET': 'https://global.americanexpress.com/myca/intl/acctsumm/emea/accountSummary.do?request_type=&Face=en_GB&omnlogin=uk_enterpriselogin_myca',
        'DestPage': 'https://global.americanexpress.com/myca/intl/acctsumm/emea/accountSummary.do?request_type=&Face=en_GB&omnlogin=uk_enterpriselogin_myca',
        'act': 'soa',
        'errMsgValueInPage': 'false',
        'isDestFound': 'destNotFound',
        'cardsmanage': 'soa',
        'UserID': security_info['username'],
        'Password': security_info['password']
    }
    r = requests.post("https://global.americanexpress.com/myca/logon/emea/action/LogLogonHandler?request_type=LogLogonHandler&location=us_logon1", data=payload)

    # use a regex to extract the balance
    balanceMatch = re.search(account_number + '.*?<span class="balance-data">£(.*?)</span>', r.text, re.DOTALL)
    if balanceMatch:
        return float('-' + balanceMatch.group(1).replace(',', ''))
    else:
        raise LookupError ('Error: no balance matched. Potentially useful debug information: ' + r.text)
