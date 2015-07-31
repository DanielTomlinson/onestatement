#! /usr/bin/python3

import re
import requests

def getBalance(security_info, account_number):
    # create a session to store all our cookies etc. in
    session = requests.Session()

    # request login form to get cookies
    r = session.get('https://online.lloydsbank.co.uk/personal/logon/login.jsp')

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        return 'Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text

    # send first part of login request (username and password)
    payload = {
        'frmLogin:strCustomerLogin_userID': security_info['username'].upper(),
        'frmLogin:strCustomerLogin_pwd': security_info['password'],
        'frmLogin:btnLogin1.x': '25',
        'frmLogin:btnLogin1.y': '1',
        'frmLogin': 'frmLogin',
        'submitToken': submitToken,
        'target': '',
        'hdn_mobile': ''
    }
    r = session.post('https://online.lloydsbank.co.uk/personal/primarylogin', headers={'Referer': 'https://online.bankofscotland.co.uk/personal/logon/login.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out which three characters from the memorable information are required
    memorableInfoMatch = re.search('Please enter characters (\d*), (\d*) and&#160;(\d*) from your memorable information', r.text)
    if memorableInfoMatch:
        firstMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(1))-1] # strings start at 0
        secondMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(2))-1] # strings start at 0
        thirdMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(3))-1] # strings start at 0
    else:
        return 'Error: couldn\'t find the three characters of memorable information which were being requested. Potentially useful debug information: ' + r.text

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        return 'Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text

    # submit the required three characters
    payload = {
        'frmentermemorableinformation1:strEnterMemorableInformation_memInfo1': '&nbsp;' + firstMemorableInfoCharacter,
        'frmentermemorableinformation1:strEnterMemorableInformation_memInfo2': '&nbsp;' + secondMemorableInfoCharacter,
        'frmentermemorableinformation1:strEnterMemorableInformation_memInfo3': '&nbsp;' + thirdMemorableInfoCharacter,
        'frmentermemorableinformation1:btnContinue.x': '40',
        'frmentermemorableinformation1:btnContinue.y': '22',
        'frmentermemorableinformation1': 'frmentermemorableinformation1',
        'submitToken': submitToken
    }
    r = session.post('https://secure.lloydsbank.co.uk/personal/a/logon/entermemorableinformation.jsp', headers={'Referer': 'https://secure.bankofscotland.co.uk/personal/a/logon/entermemorableinformation.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # check if we're on a promo page - if we are skip it
    promoMatch = re.search('<title>Lloyds Bank - Interstitial page</title>', r.text)
    if promoMatch:
        print ('Promo page spotted - skipping!')
        r = session.get('https://secure.lloydsbank.co.uk/personal/a/logon/interstitialpage.jsp?lnkcmd=continueLnk1&al=', headers={'Referer': 'https://secure.bankofscotland.co.uk/personal/a/logon/interstitialpage.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'})

    # use a regex to extract the balance
    balanceMatch = re.search('<span class="postit">Account Number </span>' + account_number + '</p></div><div class="balanceActionsWrapper"><div class="accountBalance"><p class="balance"><span class="postit">Balance </span><span class="balanceShowMeAnchor {bubble : \'balance\', pointer : \'top\', topPositionOffset : 10, leftPositionOffset : -20}">£(.*)</span></p>', r.text)
    if balanceMatch:
        return float(balanceMatch.group(1).replace(',', ''))
    else:
        raise LookupError ('No balance matched. Potentially useful debug information: ' + r.text)
