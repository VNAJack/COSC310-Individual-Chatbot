# Twitter API - Pull the latest tweets from a famous person, parse that tweet, and integrate relevant information into your conversation

import synonyms as sy
import tweepy
import webbrowser

# Authentication Info
consumer_key = 'wdyVpaa5w3aIcSonL0hOR0sHj'
consumer_secret = 'ciA39f1wV2w3rSfab2gfiiuRujbBuTCWTHCjkW9iZnnLHz3Fa3'

# Runs upon startup AND when user asks to "Enable Twitter" the bot will ask user for permission to use Twitter
def enableTwitter(userName): 
    print('IMDBot: I can use Twitter to enhance your search experience by reading the latest tweets by actors, directors, etc., but first I need to ask for your permission. ')
    while True: # loop to ask if user wants to enable Twitter
        print('IMDBot: Please confirm (yes/no) if you would like to grant me read and write permission. If you say yes, the web page that opens will explain the permission in detail before confirming the authorization.')
        check = input(f'{userName}: ')
        checkFirst = check[:1].lower() # Save first letter (might only need y or n)
        checkArr = sy.getArray(check, []) # Turn user input into array for synonym checking
        if (checkFirst == 'y' or sy.findSyns(checkArr, 'yes') == 0): # If user said yes
            print('IMDBot: Great! ', end='')
            return authenticateTwitter() # call method to authenticate
        elif (checkFirst == 'n' or sy.findSyns(checkArr, 'no') == 0): # If user said no
            print('IMDBot: Ok, I will not use Twitter. If you change your mind, please ask me to \"Enable Twitter\" ') # acknowledge user choice
            return ''
        else:
            print(f'IMDBot: I\'m sorry, I don\'t understand. ')

# If user permits use of Twitter, then the program needs to go through the authentication process, which requires user assistance and an Internet connection
def authenticateTwitter():
    count = 0
    while True:
        count += 1 # counter so that the user is not stuck in a loop forever
        # authorization of consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        redirect_url = auth.get_authorization_url()
        webbrowser.open(redirect_url)
        print('In the new browser window, please read the permission details and then click \'Authorize App\'. ') # concatenates to last message. "Great!" or "Let's try again"
        user_pin_input = input("IMDBot: What is the PIN value? ")
        try:
            auth.get_access_token(user_pin_input)
            api = tweepy.API(auth) # Not worried about rate limiter because there are 500,000 tweets that can be looked up per month
            print('IMDBot: Thank you for helping me set up Twitter! ') # Acknowledge that it is successful
            print('IMDBot: If you change your mind, you can ask me to \'Disable Twitter\' ')
            return api
        except:
            if(count == 3): # Only a few attempts to authenticate Twitter so that user is not stuck in loop if Twitter auth doesn't work.
                print('IMDBot: It looks like Twitter won\'t work today. That\'s ok! Let\'s move on :) ')
                return ''
            else:
                print('IMDBot: Something went wrong. Let\'s try again. ', end='')
                continue

# Uses the actor's name to find the twitter account and tell the user which account the bot found.
def findUser(api, query_person_name):
    for i, user_obj in enumerate(tweepy.Cursor(api.search_users, q=query_person_name).items(1)): # Only returns the 1st search result. Can be problematic if the first result is not the actual actor.
        print(f"IMDBot: The Twitter account I found associated with the name \'{query_person_name}\' is {user_obj.screen_name}") # Acknowledge the user account found (it might be incorrect)
        return user_obj # to get the screen name: user.screen_name

# Uses the user object to find and return the latest tweet ("status") object
def getLatestTweet(api, user_obj):
    user_timeline = user_obj.timeline() # get the user's timeline
    status_obj = user_timeline[0] # get the user's latest tweet as an object
    return status_obj

# Checks if the tweet is already liked ("favorited"). If is isn't, asks the user if they want to like it.
def askToLikeTweet(api, tweet_obj_id, userName):
    try:
        if api.get_status(tweet_obj_id).favorited: # Check if the tweet was already liked. If the user has already liked the tweet, then acknowledge and continue to next iteration of user input for converation
            print('IMDBot: Oh! It looks like you already liked this tweet!')
            print('IMDBot: What else would you like to know?')
            return
        else:
            while True: # Loop for yes or no question in case the user inputs something other than yes or no
                print(f'IMDBot: Do you want to \'like\' this tweet?') # Prompt to like tweet
                check = input(f'{userName}: ') # Receive input
                checkFirst = check[:1].lower() # Save first letter (only need y or n)
                checkArr = sy.getArray(check, []) # Turn user input into array for synonym checking
                if (checkFirst == 'y' or sy.findSyns(checkArr, 'yes') == 0): # if user said yes
                    api.create_favorite(tweet_obj_id) # Tweepy's method to like a Tweet
                    if api.get_status(tweet_obj_id).favorited: # Check using the tweet ID if it is now liked
                        print('Cool! You liked the tweet!') # Acknowledge if it is
                    else:
                        print('IMDBot: Woops! Something went wrong, so I could not like the tweet.')
                    break
                elif (checkFirst == 'n' or sy.findSyns(checkArr, 'no') == 0): # if user said no
                    print(f'IMDBot: Ok, you did not like the tweet.')
                    break
                else: # if user said something other than yes or no
                    print(f'IMDBot: I\'m sorry, I don\'t understand. ')
                    continue
            print('IMDBot: What else can I do for you today?')
            return
    except:
        print('IMDBot: Uh oh. Something went wrong and I cannot continue this action. What else can I help you with today?')
        return

# called in IMDBot.py to find and print the latest tweet
def printLatestTweet(api, query_person_name, userName):
    if(api == ''): # Determines if user permitted use of Twitter API
        return
    else:
        try:
            user = findUser(api, query_person_name) # To find a tweet, first the bot needs to find the person's user account on Twitter
            tweet_obj = getLatestTweet(api, user) # After finding the user account, find the latest Tweet by that person
            printTweet(query_person_name, user, tweet_obj) # print the tweet
            askToLikeTweet(api, tweet_obj.id, userName) # See if the user already liked the tweet. If they haven't, ask if they want to
            return
        except:
            print('IMDBot: Uh oh. Something went wrong and I can\'t read this tweet. What else can I help you with today?')
            return

# actual printing of the tweet
def printTweet(person_name, user_obj, tweet_obj):
    userUrl = f"https://twitter.com/{user_obj.screen_name}"
    tweetUrl = userUrl + f"/status/{tweet_obj.id}"
    print(f"IMDBot: Here\'s {person_name}\'s latest tweet, which you can also read at {tweetUrl}") # Offer the tweet URL
    print(f"{user_obj.screen_name}: {tweet_obj.text}") # Display the latest Tweet
