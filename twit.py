# TODO: README pip install tweepy 

import synonyms as sy

import tweepy
import webbrowser
import time

# Authentication Info
consumer_key = 'wdyVpaa5w3aIcSonL0hOR0sHj'
consumer_secret = 'ciA39f1wV2w3rSfab2gfiiuRujbBuTCWTHCjkW9iZnnLHz3Fa3'
callback_uri = 'oob' # http://cfe.sh/twitter/callback

# Variables

# upon startup and when user asks to "Use Twitter" the bot will ask user for permission to use Twitter
def enableTwitter(userName): 
    print('IMDBot: I can use Twitter to enhance your search experience by reading the latest tweets by actors. ')
    while True: # loop to ask if user wants to enable Twitter
        print('IMDBot: Please confirm (yes/no) if you would like me to use Twitter. I will need your help for a few seconds to set it up. ')
        check = input(f'{userName}: ')
        checkFirst = check[:1].lower() # Save first letter (might only need y or n)
        checkArr = sy.getArray(check, []) # Turn user input into array for synonym checking
        if (checkFirst == 'y' or sy.findSyns(checkArr, 'yes') == 0): # If user said yes
            print('IMDBot: Great! ', end='')
            return authenticateTwitter() # call method to authenticate
        elif (checkFirst == 'n' or sy.findSyns(checkArr, 'no') == 0): # If user said no
            print('IMDBot: Ok, I will not use Twitter. If you change your mind, please ask me to \"Use Twitter\" ') # acknowledge user choice
            return
        else:
            print(f'IMDBot: I\'m sorry, I don\'t understand. ')


# If user permits use of Twitter, then the program needs to go through the authentication process, which requires user assistance and an Internet connection
def authenticateTwitter():
    count = 0
    while True:
        count += 1 # counter so that the user is not stuck in a loop forever
        # Twitter API authentication
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
        redirect_url = auth.get_authorization_url()
        webbrowser.open(redirect_url)
        print('In the new browser window, please click \'Authorize App\'. ') # concatenates to last message. "Great!" or "Let's try again"
        user_pin_input = input("IMDBot: What is the PIN value? ")
        try:
            auth.get_access_token(user_pin_input)
            api = tweepy.API(auth) # Not worried about rate limiter because there are 500,000 tweets that can be looked up per month
            # TESTING --------------------------
            # me = api.me()
            # print('My screen name: ', end='')
            # print(me.screen_name)
            # ----------------------------------
            print('IMDBot: Thank you for helping me set up Twitter! ') # Acknowledge that it is successful
            return api
        except:
            if(count == 3): # Only a few attempts to authenticate Twitter so that user is not stuck in loop if Twitter auth doesn't work.
                print('IMDBot: It looks like Twitter won\'t work today. That\'s ok! Let\'s move on :) ')
                return
            else:
                print('IMDBot: Something went wrong. Let\'s try again. ', end='')
                continue

# Uses the actor's name to find the twitter account. 
def findUser(api, query_username):
    print('1') # TESTING ONLY
    for i, user in enumerate(tweepy.Cursor(api.search_users, q=query_username).items(1)): # Only returns the 1st search result. Can be problematic if the first result is not the actual actor.
        print(user.screen_name) # TESTING ONLY
        return user # to get the screen name: user.screen_name

def getLatestTweet(api, user_obj):
    print('3')
    user_timeline = user_obj.timeline() # get the user's timeline
    status_obj = user_timeline[0] # get the user's latest tweet as an object
    print('latest tweet:')
    print(status_obj.text)

def printLatestTweet(twitterAPI, query_actor_name):
    if(twitterAPI == ''): # Determines if user permitted use of Twitter API
        return
    else:
        #try:
        user = findUser(twitterAPI, query_actor_name)
        print(user.screen_name)
        getLatestTweet(twitterAPI, user)
        #except:
        #    print('Try-except error') # TESTING ONLY

# TESTING ONLY -------------------------------------------------------------------------
api = enableTwitter('V')

print('API: ', end='')
print(api)

query_name = input(f'Search for Twitter user: ')
printLatestTweet(api, query_name)
    




