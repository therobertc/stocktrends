import firebase_admin
from firebase_admin import credentials, firestore
from pprint import pprint
import re, json


# regular expression for extracting stocks starting with $ and having min 2 and max 5 characters
stockregex = re.compile(r'(?<!\S)\$[A-Z]{2,5}\b')

# Document IDs of the groups we are interested in
groupdocsIDs = ['EQfskFUyuLtHOK8cGACE',
                'SlACe04fpalux8Pj3jSn',
                'W7hH6ByApo9zeOuUiHU3',
                'dzdy4T9uhe1ydIs4eabv',
                'DGwBxV7x7ldrkS1agoIK14iqlmE2']

# Fetching credentials to access firestore
cred = credentials.Certificate('service-key.json')
app = firebase_admin.initialize_app(cred)

# Getting the database object
db = firestore.client(app)

stocks_dict = {}

# Looping through each id in group IDs. So that we fetch messages from all the groups we are interested in
print('Messages:')
print()
for docId in groupdocsIDs:

    # Query to get to the messages and fetch the documents for each group at a time
    messages = db.collection('message').document(docId).collection('messages').get()

    # Looping through group chat messages
    for mesg in messages:
        mesgdict = mesg.to_dict()

        # If text field not in document then ignore since some documents for some reason did not have text field
        if 'text' not in mesgdict:
            continue

        # Get the text from the message document
        text = mesgdict['text']
        print(text)

        # Get the stocks mentioned in the text
        stocksinstring = stockregex.findall(text)

        # Loop through each stock and add it to stocks_dict
        for eachstock in stocksinstring:
            # getting rid of the $ sign in the stock name that is going to be saved in stocklist
            eachstock = str(eachstock).replace('$', '')

            if eachstock in stocks_dict:  # if the stock name is already in stocklist increment by 1
                stocks_dict[eachstock] = stocks_dict[eachstock] + 1
            else:  # if the stock name is not in stocklist, well now we have :)
                stocks_dict[eachstock] = 1


# Sort stocks from top to bottom
top2bottom_stocks_dict = dict(sorted(stocks_dict.items(), key=lambda item: item[1], reverse=True))

# Converts to json
jsonData = json.dumps(top2bottom_stocks_dict)

print()
print('Json data')
print(jsonData)

