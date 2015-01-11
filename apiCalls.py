import requests
import json
import pickle
import atexit
import os.path

loc = "comp3201payme.appspot.com"

TOM = 't.r.williamst@googlemail.com'
LUBO = 'lubodjwow@gmail.com'
ALEX = 'alex.kumaila@gmail.com'
POLLY = 'pollawatp@gmail.com'

headers = {
    'User-Agent': 'FakePI'
}

session_name = 'session'

session_db = 'sessions.db'

if os.path.isfile(session_db): 
    users = pickle.load(open(session_db, 'r'))
else:
    users = {}

# Shutdown hook to serialize sessions to file
def exit_handler():
    pickle.dump(users, open(session_db, 'w'))

atexit.register(exit_handler)

def main():
    # Do a simple request to login required people
    user = getAPI(TOM, 'user')['results'][0]
    print "Logged in as: " + user['email']
    
    # Do a simple request to login required people
    user = getAPI(LUBO, 'user')['results'][0]
    print "Logged in as: " + user['email']
    
    waitForStep("Add train debt")
    addGroupDebt(TOM, 2000, (ALEX, POLLY, LUBO), 'Train to Bournemouth')
    
    waitForStep("Add beer debt")
    addGroupDebt(TOM, 1600, (ALEX, LUBO), 'Beer in Bournemouth')
    
    waitForStep("Fix last payment of lubo")
    fixLastPayment(LUBO)
    
    waitForStep("Cleanup DB")
    cleanUp()

def cleanUp():
    # Remove lubo from tom
    r = postAPI(TOM, 'friends', {'key': getUser(LUBO)['key']}, 'remove')
    
    # Remove tom from lubo
    r = postAPI(LUBO, 'friends', {'key': getUser(TOM)['key']}, 'remove')
    
    # Delete any payments from lubo
    payments = getAPI(LUBO, 'payments')['results']
    for payment in payments:
        r = postAPI(LUBO, 'payments', {'key': payment['key']}, 'remove')
    
    # Delete any debts from TOM with Bournemouth
    debts = getAPI(TOM, 'debts')['results']
    for debt in debts:
        if 'Bournemouth' in debt['description']:
            del debt['readOnly']
            r = postAPI(TOM, 'debts', debt, 'remove')
    
    # Remove lubo from the group
    group = getAPI(TOM, 'groups')['results'][0]
    luboKey = getUser(LUBO)['key']
    
    if luboKey in group['users']:
        del group['users'][group['users'].index(luboKey)]
        del group['readOnly']
    
        r = postAPI(TOM, 'groups', group, 'update')
    
def fixLastPayment(userEmail):
    payments = getAPI(userEmail, 'payments')['results']
    
    # Get last debt
    lastPay = payments[0]
    for payment in payments:
        if payment['created'] > lastPay['created']:
            lastPay = payement
    
    # Delete it
    r = postAPI(userEmail, 'payments', {'key': lastPay['key']}, 'remove')
    
    # Submit required fields
    newPay = {'debt': lastPay['debt'], 'amount': lastPay['amount'], 'description': lastPay['description'], 'payer': getUser(userEmail)['key']}
        
    # Submit it again
    r = postAPI(userEmail, 'payments', newPay, 'add')
    
def addGroupDebt(userEmail, amount, users, description):
    userAmount = amount / (len(users) + 1)
    
    for user in users:
        debt = {'amount': userAmount, 'description': description, 'debtor': getFriend(userEmail, user)['key'], 'creditor': getUser(userEmail)['key']}
        r = postAPI(userEmail, 'debts', debt, 'add')
        
def waitForStep(stepName):
    raw_input(stepName + '. Press enter to continue.')
    
def getAPI(userEmail, pageName, param = ""):
    return doAPI(userEmail, requests.get, pageName, param).json()
    
def postAPI(userEmail, pageName, data, param = ""):
    return doAPI(userEmail, requests.post, pageName, param, json.dumps(data))
    
def doAPI(userEmail, method, pageName, param = "", data = None):
    checkEmail = False

    # We don't have a session yet for that user
    if userEmail not in users:
        users[userEmail] = {session_name : raw_input("Session ID for " + userEmail + ": ")}
        checkEmail = True
    
    r = method(getURL(pageName, param), cookies = users[userEmail], headers = headers, data = data)
    users[userEmail].update(r.cookies)
    
    # Session has expired, invalidate cookie and retry
    if 'user/login' in r.url:
        del users[userEmail]
        return doAPI(userEmail, method, pageName, param, data)
    
    if checkEmail:
        sessionEmail = getUser(userEmail)['email']
    
        if sessionEmail != userEmail:
            print "User mismatch. Expected: " + userEmail + ". Session: " + sessionEmail
            del users[userEmail]
            return doAPI(userEmail, method, pageName, param, data)
    
    return r
    
def getURL(pageName, param = ""):
    return 'http://' + loc + '/api/' + pageName + '/' + param
    
def getUser(userEmail):
    return getAPI(userEmail, 'user')['results'][0]
    
def getFriend(userEmail, friendEmail):
    friends = getAPI(userEmail, 'friends')['results']
    
    for friend in friends:
        if friend['email'] == friendEmail:
            return friend
    return None
    
main()
