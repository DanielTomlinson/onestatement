# OneStatement

**Your attention is drawn to the LICENSE file, in particular the note that this software is provided "as is" and without any warrenties. You are encouraged to inspect the source code and report any issues you discover.**

OneStatement is a project written for my [Young Rewired State Festival of Code](http://festival.yrs.io/) 2015 project. The idea is to aggrigate transaction data from multiple financial institutions into one statement. The key advantage this program has over other solutions such as [Money Dashboard](https://www.moneydashboard.com/) is that your security details never leave your machine (other than to be sent directly to the financial institution for checking), therefore you are not handing your bank details to a third party. This solution means you don't have to accept the risk of a third party losing your sensitive financial data (and liability for any resulting losses).

**Current status: checks balances only.**

The API is written facilitate extracting data from financial institutions and currently doesn't support checking transactions - it will be added at some point in the near future. Once this is done it shouldn't take too much effort to add transaction data to OneStatement.

## Requirements

This program uses Python 3 and the [Requests](http://docs.python-requests.org/en/latest/) module. I've only tested it on Debian 8 "Jessie", but in principle there's no reason it shouldn't work on other platforms.

Integrations currently only exist for [American Express](https://www.americanexpress.com/uk/), [Bank of Scotland](http://www.aquacard.co.uk/), [HSBC](http://www.hsbc.co.uk/1/2/), [Lloyds Bank](http://www.lloydsbank.com/), and [TSB](http://www.tsb.co.uk/). Please feel free to submit pull requests with other integrations - although validation of correctness will be challenging, the code will be checked for any security issues.

## Usage

Firstly, write a configuration file in JSON called config.json. It should look a bit like this:

```
[ 
    { 
        "name":"Current Account",
        "provider":"HSBC",
        "number":"13579246",
        "type":"current",
        "security":{"username":"foo", "password":"bar", "memorable answer":"baz"}
    },
    {
        "name":"Savings Account",
        "provider":"TSB",
        "number":"24681098",
        "type":"savings",
        "security":{"username":"steve", "password":"apple", "memorable information":"thebigonenewyork"}
    },
    {
        "name":"Credit Card",
        "provider":"Aqua",
        "number":"2505",
        "type":"credit",
        "security":{"internet id":"HomeBrewCCRW", "last name":"Wayne", "memorable word":"foobar2000", "passcode":"15243"}
    }
]
```

Note that the security information is institution-specific - you'll need to check which details you need to log into internet banking.

You then simply need to run `./onestatement.py`, and view the index.html file it generates (in the same directory).

## API Usage

It's possible to use the API provided by finance_api.py directly. At some point in time it'll be packaged nicely so it can be installed using pip.

### getBalance

Example: `getBalance(provider, security_info, account_number)`

`security_info` is a dictionary of security credentials (see the example config file above).

Returns the balance as a float (i.e. without a £ sign).

### getTransactions

**Doesn't yet exist**, but the syntax will be:

Example: `getTransactions(provider, security_info, account_number, start_date[, end_date])`

The start date should be earlier than the end date (which is optional, and defaults to today). Dates should be formatted in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601).

Returns JSON of the transactions containing the following:

Account ID - the ID of the acount where the transaction took place.  
Date - the date of the transaction.  
Type - a three character code corresponding to the transaction type (for example, cash widthdrawal, faster payment, or bank giro credit).  
Description - the description of the transaction (from the institution).   
Amount - the amount of the transaction.  
Merchant - the merchant in the transaction, if the data is available / extractable from the description.  
Location - the location of the merchant in the transaction, if available.  
Tags - tags to assist in money management, for example 'food' or 'discretionary spending'.  
URL - the URL relating to a transaction, for example, an Amazon order URL.  
Other - a field for future use.
