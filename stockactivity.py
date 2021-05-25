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

timesmention = 0

stock = input('Enter a stock name: ')
print()

stock = stock.upper()

if '$' not in stock:
    stock = f'${stock}'


# Looping through each id in group IDs. So that we fetch messages from all the groups we are interested in
print(f'Messages in which {stock} is mentioned:')
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
        if stock in text:
            print(text)
            timesmention += 1




print()
print(f'Stock {stock} is mentioned in {timesmention} texts')

