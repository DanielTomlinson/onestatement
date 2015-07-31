#! /usr/bin/python3

import re
import requests
import time

def getBalance(security_info, account_number):
    # create a session to store all our cookies etc. in
    session = requests.Session()

    # request login form to get cookies
    r = session.get('https://online.tsb.co.uk/personal/logon/login.jsp')

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text)

    # send first part of login request (username and password) to TSB
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
    r = session.post('https://online.tsb.co.uk/personal/primarylogin', headers={'Referer': 'https://online.tsb.co.uk/personal/logon/login.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out which three characters from the memorable information are required
    memorableInfoMatch = re.search('Please enter characters (\d*), (\d*) and&#160;(\d*) from your memorable information', r.text)
    if memorableInfoMatch:
        firstMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(1))-1] # strings start at 0
        secondMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(2))-1] # strings start at 0
        thirdMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(3))-1] # strings start at 0
    else:
        raise LookupError ('Error: couldn\'t find the three characters of memorable information which were being requested. Potentially useful debug information: ' + r.text)

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text)

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
    r = session.post('https://secure.tsb.co.uk/personal/a/logon/entermemorableinformation.jsp', headers={'Referer': 'https://secure.tsb.co.uk/personal/a/logon/entermemorableinformation.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # use a regex to extract the balance
    balanceMatch = re.search('<span class="postit">Account Number </span>' + account_number + '</p></div><div class="balanceActionsWrapper"><div class="accountBalance"><p class="balance"><span class="postit">Balance </span><span class="balanceShowMeAnchor {bubble : \'balance\', pointer : \'top\', topPositionOffset : 10, leftPositionOffset : -20}">£(.*)</span></p>', r.text)
    if balanceMatch:
        return float(balanceMatch.group(1).replace(',', ''))
    else:
        raise LookupError ('No balance matched. Potentially useful debug information: ' + r.text)

def getTransactions(security_info, account_number, start_date, end_date=time.strftime("Y-%m-%d")):
    # create a session to store all our cookies etc. in
    session = requests.Session()

    # request login form to get cookies
    r = session.get('https://online.tsb.co.uk/personal/logon/login.jsp')

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text)

    # send first part of login request (username and password) to TSB
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
    r = session.post('https://online.tsb.co.uk/personal/primarylogin', headers={'Referer': 'https://online.tsb.co.uk/personal/logon/login.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out which three characters from the memorable information are required
    memorableInfoMatch = re.search('Please enter characters (\d*), (\d*) and&#160;(\d*) from your memorable information', r.text)
    if memorableInfoMatch:
        firstMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(1))-1] # strings start at 0
        secondMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(2))-1] # strings start at 0
        thirdMemorableInfoCharacter = security_info['memorable information'][int(memorableInfoMatch.group(3))-1] # strings start at 0
    else:
        raise LookupError ('Error: couldn\'t find the three characters of memorable information which were being requested. Potentially useful debug information: ' + r.text)

    # grab the submit token
    submitTokenMatch = re.search('<input.*?type="hidden".*?name="submitToken".*?value="(\d*)" />', r.text, re.DOTALL)
    if submitTokenMatch:
        submitToken = submitTokenMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the submit token from the first login page. Potentially useful debug information: ' + r.text)

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
    r = session.post('https://secure.tsb.co.uk/personal/a/logon/entermemorableinformation.jsp', headers={'Referer': 'https://secure.tsb.co.uk/personal/a/logon/entermemorableinformation.jsp', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # get the url for more details on the account we're interested in
    accountUrlMatch = re.search('<a.*?href="(/personal/a/viewaccount/accountoverviewpersonalbase.jsp?.*?)".*?>.*?<span.*?>Account Number </span>' + account_number + '</p>', r.text)
    if accountUrlMatch:
        accountURl = 'https://secure.tsb.co.uk/' + accountUrlMatch.group(1)
    else:
        raise LookupError ('Couldn\'t find the account number requested (' + account_number + '). Potentially useful debug information: ' + r.text)

    r = session.get('https://secure.tsb.co.uk/personal/a/logon/entermemorableinformation.jsp')

    print (r.text)
    raise Exception
