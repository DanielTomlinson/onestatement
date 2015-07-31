#! /usr/bin/python3

import time

def getBalance(provider, security_info, account_number):
    provider = provider.lower().replace(" ", "")
    providerModule = __import__('providers.' + provider, globals(), locals(), ['getBalance'], 0)
    providerGetBalance = providerModule.getBalance
    balance = providerGetBalance(security_info, account_number)
    return balance
