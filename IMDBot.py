from re import split
import film as f
import person as p
import company as c
import user as u
import ner
import spellinghandler as sp
import synonyms as sy
import postagging as pt
import twitter as tw
import googleNews as gn
from chatterbot import ChatBot

bot = ChatBot('MovieBot')

# Introduces itself and sets up username
print('IMDBot: Hello There! My name is IMDBot. ', end='')
userName = u.askForName() #set username for the first time
print(f'IMDBOT: I just want to make sure I have your name right.')
userName = u.checkName(userName) #check username if correct. method can also be used if user wants to change their username
print(f'I am a bot who knows all about movies. ') #concatenates to "IMDBot: That's a cool name, userName! "

# bot asks user for permission and assistance with authenticating APIs. User can decline.
twAPI = tw.enableTwitter(userName) # if enabled, twAPI is an object, otherwise twAPI = '' 

# enable Google news
googleNews = gn.enableGoogleNews()
print(f'I can also look up the latest news about people, movies, and production companies using Google News. This does not require any permissions!')

# Once APIs are done, can use the bot as intended
print(f'IMDBot: Now, how can I help you today? ')
while True:
    try:
        raw_user_input = input(f'{userName}: ') # collect user input for this iteration
        # Process user input
        entities = ner.listEntities(raw_user_input) # named entity recognition
        movie_name = ner.getMovieName(raw_user_input) # save movie name from ner, if any
        person_name = ner.getPersonName(raw_user_input) # save person name from ner, if any
        company_name = ner.getOrgName(raw_user_input) # save company name from ner, if any
        user_input = sp.fixSentence(raw_user_input, entities) # correct any spelling mistakes outside of entities
        tagged = pt.getPosSentenceEntity(user_input,entities) # get the Part of speech of the spell checked sentence in the form of arrays containing tuples
        user_input = sy.getArray(user_input, entities) # User input is now an array. To look for keywords: if 'keyword' in user_input

        # Make input (not including entities) lowercase
        for i in range (len(user_input)):
            user_input[i] = user_input[i].lower()
        
        if len(user_input) == 1 and 'help' in user_input:
            print('IMDBot: You said \'help\'. I\'m IMDBot. A chatbot that knows all about movies! :) ')
            print('IMDBot: Here\'s a list of some of the things you can ask me to do:')
            print(f'\t - change your name')
            print(f'\t - enable or disable Twitter')
            print(f'\t - find a movie')
            print(f'\t - tell you how long a movie is (the runtime)')
            print(f'\t - give you the plot or summary of a movie')
            print(f'\t - find the director of a movie')
            print(f'\t - list characters in a movie you previously searched for')
            print(f'\t - find which actor played a certain character in a movie')
            print(f'\t - find the latest movie an actor worked on')
            print(f'\t - list other movies an actor has worked on')
            print(f'\t - tell you what an actor\'s birthday, birth place, and biography are')
            print(f'\t - check if an actor was in a movie')
            print(f'\t - find out if a person worked on or had a role in a movie')
            print(f'\t - find the production company of a movie')
            print(f'\t - find what other movies that company produced')
            print(f'\t - display the latest tweet by an actor or director')
            print(f'\t - find five recent news articles about an actor, director, movie, and/or production company')
            print('IMDBot: If you want to end the conversation, you can simply say \'Goodbye\'')

        # User can change theirname
        elif (sy.findSyns(user_input, 'change') == 0 and ('name' in user_input or 'username' in user_input)):
            userName = u.checkName(userName)
            print('How can I help you?') #concatenates to "IMDBot: That's a cool name, userName! "

        # Enable Twitter. If Twitter was not authorized on startup, but the user changed their mind and wants to authorize Twitter
        elif(('enable' in user_input) and ('twitter' in user_input) and (twAPI == '')):
            twAPI = tw.enableTwitter(userName)
            print(f'IMDBot: Now, how can I help?')

        # Disable Twitter. Twitter is already enabled, but the user wants to disable Twitter
        if(('disable' in user_input) and ('twitter' in user_input) and (twAPI != '')):
            twAPI = '' # need the API object to do anything. Without it, no Twitter API actions can be performed
            print('IMDBot: Twitter is now disabled. If you would like to re-enable it, please ask me to \'Enable Twitter\'')
        
        # Find a movie or find another movie
        elif ((sy.findSyns(user_input, 'find') == 0 or sy.findSyns(user_input, 'search') == 0) and ('another' in user_input or sy.findSyns(user_input, 'movie') == 0)): # pick the movie to talk about
            movie = f.findMovie(userName)

        # Find the director a movie
        elif (sy.findSyns(user_input, 'director') == 0 or sy.findSyns(user_input, 'directed') == 0): #find the director of the movie we're talking about and store as object for follow up questions about them
            if 'movie' in locals(): # check if a movie object is already saved (a movie is being spoken about)
                person = f.findDirector(movie)
                tw.printLatestTweet(twAPI, person['name'])
            else:
                print('IMDBot: Sorry, I don\'t know which movie you\'re asking about to find the director. Try to ask me to find a movie :)') # if a movie is not being currently discussed, tell user it doesn't understand 
        
        # List the characters of a movie
        elif (sy.findSyns(user_input, 'character') == 0):
            if 'movie' in locals():
                movie = f.showCharacters(movie)
            else:
                print('IMDBot: Sorry, I don\'t know which movie you\'re asking about to list the characters. Try to ask me to find a movie first!')
        
        # Find the actor who played a character
        elif (('who' in user_input) and (('played' in user_input) or ('voiced' in user_input)) and (person_name != '')):
            if 'movie' in locals(): # If there's already a movie object (previously searched for a movie)
                person = f.whoPlayed(twAPI, userName, movie, person_name, movie_name)
            elif movie_name != '': # If the user is asking who played {character} in {movie_name} then we have a movie name to use
                person = f.whoPlayed(twAPI, userName, '', person_name, movie_name)
            else: # Don't know which movie they're asking to search for the character in
                print(f'IMDBot: I\'m sorry. To look for {person_name} I need to know which movie you\'re asking about.')

        # User asks about the person's latest tweet
        elif(('latest' in user_input) and ('tweet' in user_input)):
            if(twAPI == ''):
                print(f'IMDBot: Twitter is not enabled. Please ask me to \'enable Twitter\'.')
            else:
                if 'person' in locals() and person_name == '': # if there is already a person object in locals (a person was already searched for) and that is the only name mentioned
                    tw.printLatestTweet(twAPI, person['name'], userName) # prints the latest tweet and asks user if they want to like it if they haven't already
                elif(person_name != ''): # if the user asked "What is {person_name}'s latest tweet?" then this name is the one to use to search
                    tw.printLatestTweet(twAPI, person_name, userName) # prints the latest tweet and asks user if they want to like it if they haven't already
                else: # no person or name, so can't look up the latest tweet without knowing the person
                    print(f'IMDBot: I\'m sorry. I don\'t know who you\'re asking about.')
        
        # What is the production company of a movie
        elif (('production' and 'company') in user_input or sy.findSyns(user_input, 'companies') == 0):
            if movie_name != '':
                movie = c.findMovieForCompany(userName, movie_name)
                company = c.findCompany(movie)
                print('IMDBot: What else would you like to know? :)')
            elif 'movie' in locals():
                company = c.findCompany(movie) # list the production companies of the movie asked
                print('IMDBot: What else would you like to know? :)')
            else:
                print('IMDBot: Sorry. I need to know which movie you\'re asking about first. Please ask me again and specify the movie :)')
            
        # List other movies that the production company produced
        elif ('other' in user_input and sy.findSyns(user_input, 'produce')):
            otherMovie = c.findMovieForCompany(userName, '')
            c.isProduction(company_name, otherMovie)
            print("IMDBot: What else would you like to know?")
        
        # Recent news about movie or person
        elif (sy.findSyns(user_input, 'news') == 0) or (('what' in user_input or 'what\'s' in user_input) and sy.findSyns(user_input, 'new') == 0):
            query = []
            if person_name != '': query.append(person_name)     # if user specified a person (person_name is a found entity), add it to the query
            if movie_name != '': query.append(movie_name)       # if user specified a movie (movie_name is a found entity), add it to the query
            if company_name != '': query.append(company_name)   # if user specified a company (company_name is a found entity), add it to the query
            if len(query) >= 1: # if at least one of the above was added to the query
                query = " and ".join(query) # join them with the word ' and '
            elif ('him' in user_input or 'her' in user_input or 'them' in user_input) and ('person' in locals()): # no entities, but a person was previously specified and the user asked about 'him, her or them'
                query = person['name'] # make the person's name the query
            elif 'movie' in locals() and 'company' not in locals(): # no entities, no person, but a movie was previously specified
                query = movie['title'] # make the movie title the query
            elif 'movie' not in locals() and 'company' in locals(): # no entities, no person, no movie, but a company was previously specified
                query = company # make the company name the query
            elif 'movie' in locals() and 'company' in locals(): # if both a movie AND a company were previously specified, clarify what the user wants to search for
                print(f"IMDBot: Before I search for news, I just want to clarify... Were you asking about the movie '{movie['title']}' or the production company '{company}'?")
                answer = input(f'{userName}: ')
                if(answer.find('movie') != -1): # this can be problematic if the user uses the actual name of the movie instead of the word 'movie'
                    query = movie['title'] # make the movie title the query
                elif(answer.find('company') != -1): # this can be problematic if the user uses the actual name of the company instead of the word 'company'
                    query = company # make the company name the query
                elif(answer.find('both') != -1): # this can be problematic if the user uses the actual names of both the movie and company instead of the word 'both'
                    query = movie['title'] + ' and ' + company # make both the movie and company names the query
                else:
                    query = '' # if the user doesn't say 'movie' or 'company' then leave the query blank
            else:
                query = ''
            if query != '': # if the query isn't blank
                gn.getGoogleNews(userName, googleNews, query) # search with the query
            else: # if the query is blank
                print('IMDBot: Sorry, I don\'t know which person, movie, or production company you want me to look for news about. Please try asking me again in another way.')

        # List other movies the person has worked on
        elif('what' in user_input and ('other' in user_input or 'another' in user_input)) :
            #takes in user input and calls otherRoles() from person.py
            if 'person' in locals():
                print("IMDBot: Hmm... let me think...")
                p.otherRoles(person) # Takes person object
            else:
                print("IMDBot: Sorry I am not sure how to help with that.")
        
        # What is the person's birthday
        elif(sy.findSyns(user_input, 'birthday') == 0 or ('when' in user_input and sy.findSyns(user_input, 'born') == 0)):
            #Call giveBio() from person.py
            #Search for birthday/birthdate
            print("IMDBot: Hmm... let me think...")
            if 'person' in locals():
                p.giveBio(person['name'], 1)
            elif person_name != '':
                p.giveBio(person_name, 1)
            else:
                print("IMDBot: I\'m not sure who you\'re asking about.")
            print("IMDBot: What else would you like to know?")
        
        # What is the person's birth place
        elif(('where' in user_input or 'place' in user_input) and ('born' in user_input or 'birth' in user_input)):
            #Search for birth place of an actor
            print("IMDBot: Hmm... let me think...")
            if 'person' in locals():
                p.giveBio(person['name'], 2)
            elif person_name != '':
                p.giveBio(person_name, 2)
            else:
                print("IMDBot: I\'m not sure who you\'re asking about.")
            print("IMDBot: What else would you like to know?")
        
        # What is the last movie the person worked on
        elif(sy.findSyns(user_input, 'latest') == 0 or sy.findSyns(user_input, 'last') == 0 and sy.findSyns(user_input, 'movie') == 0):
            #Search for a latest movie by an actor
            print("IMDBot: Hmm... let me think...")
            if 'person' in locals():
                p.giveBio(person['name'], 3)
            elif person_name != '':
                p.giveBio(person_name, 3)
            else:
                print("IMDBot: I\'m not sure who you\'re asking about.")
            print("IMDBot: What else would you like to know?")
        
        # Provide a biography of the person
        elif('bio' in user_input or sy.findSyns(user_input, "biography") == 0):
            # Gets bio of an actor
            # bio {any actor name}
            if 'person' in locals():
                p.giveBio(person['name'], 4)
            elif person_name != '':
                p.giveBio(person_name, 4)
            else:
                print("IMDBot: I\'m not sure who you\'re asking about.")
            print("IMDBot: What else would you like to know?")
        
        # Check if a person was in a movie
        elif(('check' in user_input and 'if' in user_input and 'in' in user_input) and (person_name != '') and (movie_name != '')):
            #Check if a {actor} is in {movie}
            if 'movie' in locals():
                p.checker(userName, person_name, movie, movie_name)
            else:
                p.checker(userName, person_name, '', movie_name)
            print('IMDBot: What else can I help you with?')
            
        # What is the runtime of a movie
        elif ((('how' and 'long') in user_input) or ('runtime' in user_input or sy.findSyns(user_input, 'length') == 0)): # Moved to the bottom because it can get called by accident if near top
            if 'movie' in locals():
                movie = f.runtime(movie)
            else:
                print('IMDBot: Sorry, I need to know which movie you want me to check the runtime for. Please ask me to find a movie first.')
        
        # Confirm if the person worked on a movie
        elif(('worked' in user_input and 'on' in user_input) or ('role' in user_input and 'in' in user_input) or ('acted' in user_input and 'in' in user_input)): # Moved to bottom because it can get called by accident if at the top
            #takes in user input and calls isMember() from person.py
            if 'movie' in locals():
                print("IMDBot: Hmm... let me check...")
                p.isMember(movie, person) # Takes movie and person objects so they must already be defined
            else:
                print("IMDBot: Sorry, I could not find anything about that.")
        
        # What is the summary or plot of a movie
        elif (('summary' in user_input) or ('plot' in user_input)):
            if 'movie' in locals():
                movie = f.giveSummary(movie)
            else:
                print('IMDBot: Sorry, I don\'t know which movie you\'re asking about. Try to ask me to find a movie :)')

        # User can change the subject
        elif ('nevermind' in user_input):
            print(f'IMDBot: Ok. How can I help?')

        # User can end the conversation by saying 'bye'
        elif ('bye' in user_input or sy.findSyns(user_input, 'goodbye') == 0): #end conversation if user says bye
            print('\nIMDBot: Goodbye! It was nice talking to you ' + userName)
            quit()

        else:
            #bot.get_response(raw_user_input)
            print("IMDBot: I'm sorry. Something went wrong. Can you try to ask that again in another way?")

    except(KeyboardInterrupt, EOFError, SystemExit) as e: #end conversation in case of fatal error or user inputs ctrl+c
        break
