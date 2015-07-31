#! /usr/bin/python3

import finance_api
import hashlib
import json

with open('config.json') as config_file:    
    accounts = json.load(config_file)

account_map = {}
totalBalance = float(0)

# generate account map
for account in accounts:
    account['id'] = hashlib.sha1((account['provider'] + account['number']).encode()).hexdigest()
    account_map[account['id']] = {'name': account['name'], 'provider': account['provider']}

# dump map (account id to nice name and provider name)
with open("map.json", "w") as outfile:
    json.dump(account_map, outfile, indent=4)

# get account balances
for account in accounts:
    account['balance'] = finance_api.getBalance(account['provider'], account['security'], account['number'])
    totalBalance += account['balance']

# generate HTML
html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>OneStatement</title>
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <style type="text/css">
            #myTab {margin-bottom:10px;}
            #myTabContent {padding:5px;}
        </style>
    </head>
    <body>
        <div class="container" style="margin-top:20px;">
            <ul id="myTab" class="nav nav-tabs">
                <li class="active"><a href="#overview" data-toggle="tab">Overview</a></li>"""
for account in accounts:
    html += '                <li><a href="#' + account['id'] + '" data-toggle="tab">' + account['name'] + '</a></li>'
html += """            </ul>
            <div id="myTabContent" class="tab-content">
                <div class="tab-pane fade in active" id="overview">"""
html += "                    <p><strong>Total balance: £" + '%.2f' % totalBalance + "</strong></p>"
html += "                </div>"
for account in accounts:
    html += '                <div class="tab-pane fade" id="' + account['id'] + '">'
    html += "                   <p><strong>Account balance: £" + '%.2f' % account['balance'] + "</strong></p>"
    html += '                </div>'
html += """            </div>
            <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
            <script src="js/jquery.min.js"></script>
            <!-- Include all compiled plugins (below), or include individual files as needed -->
            <script src="js/bootstrap.min.js"></script>
        </div>
    </body>
</html>"""
f = open('index.html', 'w')
f.write(html)
f.close()
