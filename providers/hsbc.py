#! /usr/bin/python3

import re
import requests
import time

def getBalance(security_info, account_number):
    # create a session to store all our cookies etc. in
    session = requests.Session()

    # get a url to use to login to internet banking (they appear to expire)
    r = session.get("https://www.hsbc.co.uk/1/2/")
    urlMatch = re.search('<li><a.*? href="(.*?)" title="Log on to Personal Internet Banking">', r.text)
    if urlMatch:
        internetBankingUrl = 'https://www.hsbc.co.uk' + urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find an internet banking url. Potentially useful debug information: ' + r.text)

    # get the url to post the username to
    r = session.get(internetBankingUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'})
    urlMatch = re.search('<form method="post".*?id="logonForm".*?action="(.*?)".*?>', r.text, re.DOTALL)
    if urlMatch:
        postUrl = 'https://www.hsbc.co.uk' + urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post an internet banking username to. Potentially useful debug information: ' + r.text)

    # send username
    payload = {
        'jdata': '',
        'browserTimeZone': int(time.time())*1000,
        'userid': security_info['username'],
        'cookieuserid': 'false',
        'nextPage': 'WELCOME_PAGE'
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out where to submit the "tempForm"
    urlMatch = re.search('<form name=tempForm action="(.*?)" method="POST">', r.text)
    if urlMatch:
        postUrl = urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post the "tempForm" to. Potentially useful debug information: ' + r.text)

    # submit the "tempForm"
    payload = {
        'userid': security_info['username'].upper(),
        'initialAccess': 'true'
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out where to submit the form with all the SAAS tokens
    urlMatch = re.search("<form name=tempForm action='(.*?)' method='POST'>", r.text)
    if urlMatch:
        postUrl = urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post the SAAS tokens to. Potentially useful debug information: ' + r.text)

    # extract the SAAS_TOKEN_ASSERTION_ID and SAAS_TOKEN_ID
    saasAssertionIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ASSERTION_ID" value="(.*?)"', r.text)
    if saasAssertionIdMatch:
        saasAssertionId = saasAssertionIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ASSERTION_ID on the second temporary login form. Potentially useful debug information: ' + r.text)
    saasIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ID" value="(.*?)"', r.text)
    if saasIdMatch:
        saasId = saasIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ID on the second temporary login form. Potentially useful debug information: ' + r.text)

    # submit the form with all the SAAS tokens
    payload = {
        'SAAS_TOKEN_ASSERTION_ID': saasAssertionId,
        'SAAS_TOKEN_ID': saasId
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # we have to do all the above again
    urlMatch = re.search("<form name=tempForm action='(.*?)' method='POST'>", r.text)
    if urlMatch:
        postUrl = urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post the SAAS tokens to (for the second time). Potentially useful debug information: ' + r.text)
    saasAssertionIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ASSERTION_ID" value="(.*?)"', r.text)
    if saasAssertionIdMatch:
        saasAssertionId = saasAssertionIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ASSERTION_ID on the second temporary login form. Potentially useful debug information: ' + r.text)
    saasIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ID" value="(.*?)"', r.text)
    if saasIdMatch:
        saasId = saasIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ID on the second temporary login form. Potentially useful debug information: ' + r.text)
    payload = {
        'SAAS_TOKEN_ASSERTION_ID': saasAssertionId,
        'SAAS_TOKEN_ID': saasId
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

### WE WANT TO TRY AND LOG IN WITHOUT SECURE KEY
### THIS SHOULD BE POSSIBLE, BUT JAVASRIPT MAKES IT SOMEWHAT UNOBVIOUS HOW IT ALL WORKS
### I THINK I'VE GOT IT THOUGH!

    # get the url to use when logging in without secure key
    withoutSecureKeyMatch = re.search('<a href="(.*?)">.*?Without Secure Key', r.text)
    if withoutSecureKeyMatch:
        withoutSecureKeyUrl = 'https://www1.security.hsbc.co.uk' + withoutSecureKeyMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to use when attempting to log in without secure key. Potentially useful debug information: ' + r.text)

    # get the page to log in without secure key
    r = session.get(withoutSecureKeyUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'})

    # scrape the page to post the security information to
    urlMatch = re.search('<form data-dojo-type="hsbcwidget/formValidCheck" method="post".*?action="(.*?)">', r.text, re.DOTALL)
    if urlMatch:
        postUrl = 'https://www1.security.hsbc.co.uk' + urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post the secure key and memorable answer to. Potentially useful debug information: ' + r.text)

    # work out which digits of the password we're being asked for
    passwordCharsMatch = re.search('data-dojo-props="chalNums: \[(\d, \d, \d)\]', r.text)
    if passwordCharsMatch:
        passwordCharsRequested = passwordCharsMatch.group(1).split()
    else:
        raise LookupError ('Error: couldn\'t find the password characters being requested. Potentially useful debug information: ' + r.text) 
    passwordChars = []
    # characters 7 and 8 are actually second to last and last (respectively)
    for char in passwordCharsRequested:
        char = char[0] # remove trailing comma
        if char == '7':
            tmpChar = -2
        elif char == '8':
            tmpChar = -1
        else:
            tmpChar = int(char) - 1 # computer counting starts at 0
        passwordChars.append(security_info['password'][tmpChar])

    # scrape the ESDS token
    esdsMatch = re.search("<input type='hidden' name='(.*?)' value='0' />", r.text)
    if esdsMatch:
        esdsToken = esdsMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find an ESDS token. Potentially useful debug information: ' + r.text)

    # post the memorable answer and requested digits from the password
    payload = {
        esdsToken: 0,
        'jdata': '',
        'browserTimeZone': int(time.time())*1000,
        'memorableAnswer': security_info['memorable answer'],
        'pass' + passwordCharsRequested[0]: passwordChars[0],
        'pass' + passwordCharsRequested[1]: passwordChars[1],
        'pass' + passwordCharsRequested[2]: passwordChars[2],
        'password': passwordChars[0] + passwordChars[1] + passwordChars[2]
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # work out where this form is going
    urlMatch = re.search('<form name=tempForm action="(.*?)" method="POST">', r.text, re.DOTALL)
    if urlMatch:
        postUrl = urlMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the url to post the SAAS tokens to (after sending the secure key code). Potentially useful debug information: ' + r.text)

    # scrape the ESDS token
    esdsMatch = re.search("<input type='hidden' name='(.*?)' value='0' />", r.text)
    if esdsMatch:
        esdsToken = esdsMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find an ESDS token (2nd time). Potentially useful debug information: ' + r.text)

    # extract the SAAS_TOKEN_ASSERTION_ID and SAAS_TOKEN_ID
    saasAssertionIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ASSERTION_ID" value="(.*?)"', r.text, re.DOTALL)
    if saasAssertionIdMatch:
        saasAssertionId = saasAssertionIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ASSERTION_ID on the temporary login form after sending the secure key code. Potentially useful debug information: ' + r.text)
    saasIdMatch = re.search('<input type="hidden" name="SAAS_TOKEN_ID" value="(.*?)"', r.text)
    if saasIdMatch:
        saasId = saasIdMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the SAAS_TOKEN_ID on the temporary login form after sending the secure key code. Potentially useful debug information: ' + r.text)

    # post the SAAS tokens
    payload = {
        esdsToken: 0,
        'SAAS_TOKEN_ID': saasId,
        'SAAS_TOKEN_ASSERTION_ID': saasAssertionId
    }
    r = session.post(postUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}, data=payload)

    # find the redirect link
    redirectMatch = re.search('<a title="You are being redirected, if this does not complete shortly please use this link" href="(.*?)">You are being redirected, if this does not complete shortly please use this link</a>', r.text)
    if redirectMatch:
        redirectUrl = 'https://www.saas.hsbc.co.uk' + redirectMatch.group(1)
    else:
        raise LookupError ('Error: couldn\'t find the URL to redirect to. Potentially useful debug information: ' + r.text)

    # click it
    r = session.get(redirectUrl, headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'})

    r = session.get('https://www.saas.hsbc.co.uk/1/3/personal/online-banking?BlitzToken=blitz', headers={'Referer': r.url, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'})

    # use a regex to extract the balance
    balanceMatch = re.search(account_number + '.*?<div class="col3 rowNo1 rightAlign"><strong>(\d*?\.\d\d)', r.text, re.DOTALL)
    if balanceMatch:
        typeMatch = re.search('.*?<div class="col3 rowNo1 rightAlign"><strong>\d*?\.\d\d  (.)', r.text)
        if typeMatch:
            balanceType = typeMatch.group(1)
            if balanceType == 'C':
                return float(balanceMatch.group(1))
            elif balanceType == 'D':
                return float('-' + balanceMatch.group(1))
            else:
                raise ValueError ('An unknown balance type (' + balanceType + ') was reported.')
        else:
            raise LookupError ('No balance type matched. Potentially useful debug information: ' + r.text)
    else:
        raise LookupError ('No balance matched. Potentially useful debug information: ' + r.text)
