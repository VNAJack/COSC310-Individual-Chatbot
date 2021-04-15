# Google Feed API - take any public feeds and displays them in a useful way in your program
# pip install GoogleNews
# pip install pyshorteners

import synonyms as sy
from GoogleNews import GoogleNews
import pyshorteners # used to shorten URLs

# INITIALIZE with settings --> return googleNews object
def enableGoogleNews():
    googleNews = GoogleNews()
    googleNews.set_lang('en') # choose language: English
    # No date range or period set because many movies and actors have news that is not actually that recent
    return googleNews

def clearSearch(googleNews):
    googleNews.clear()

# SEARCH --> input query, returns list of dictionaires. Each article is a dict.
def searchNews(googleNews, query):
    googleNews.get_news(query) # search for relevant and recent news about the query
    return googleNews # return the googleNews object which holds the search

# TITLE OF ARTICLE --> input article dict, returns title as string
def getTitle(article):
    rawTitle = article['title'] # includes title and other info separated by "–"
    strippedTitle = rawTitle.strip() # removes any trailing and leading whitespaces, including tabs
    length = len(strippedTitle)
    if strippedTitle.find("-") == length : # if title has trailing "-" remove it
        return strippedTitle[:length-1].strip()
    else:
        return strippedTitle

# SOURCE OF ARTICLE --> input article dict, returns source as string
def getSource(article):
    return article['site']

# DATE POSTED OF ARTICLE --> input article dict, returns date as string (format example: Mar. 30)
def getDatePosted(article):
    rawDateTime = str(article['datetime']) # Raw will either be None or something like 2021-04-11 15:14:21.383450
    if rawDateTime == 'None': # Not all articles have 'dateTime', but will have 'date'
        return article['date'] # 'date' is already in format "Mar. 30"
    else:
        date = rawDateTime.split(" ")[0] # 2021-04-11
        date = date.split("-") # ['2021', '04', '11']
        month = getMonthName(date[1]) # get month name from 04
        day = trimDay(date[2]) # trim day if it has leading 0's
        return f'{month}. {day}' # return in format "Mar. 30"

# HELPER FOR getDatePosted() to convert month "number" to short name
def getMonthName(month):
    if month == '01': return "Jan"
    elif month == '02': return "Feb"
    elif month == '03': return "Mar"
    elif month == '04': return "Apr"
    elif month == '05': return "May"
    elif month == '06': return "Jun"
    elif month == '07': return "Jul"
    elif month == '08': return "Aug"
    elif month == '09': return "Sep"
    elif month == '10': return "Oct"
    elif month == '11': return "Nov"
    elif month == '12': return "Dec"
    else: return 'ERR'

# HELPER FOR getDatePosted() to remove leading 0's on day
def trimDay(day):
    if day[:1] == '0': return day[1:2]
    else: return day

# 5 RELEVANT NEWS ARTICLES --> returns list of articles, and articles are dicts
def get5Results(googleNews):
    newsList = googleNews.result() # get the list of results
    # print('IMDBot: Here are the 5 most relevant and recent search results:')
    articleList = [] # make a list of the 5 results for future use
    for i in range(0, 5):
        article = newsList[i]
        articleList.append(article)
    return articleList

# Display the relevant results and ask user which article they want to read
def displayResults(articleList, query):
    # Print list of 5 most relevant and recent search results
    print(f'IMDBot: Here are the 5 most relevant and recent news stories I could find about {query}:')
    i = 1
    for article in articleList:
        print(f'{i}) {getTitle(article)} posted {getDatePosted(article)} by {getSource(article)}')
        i += 1

def askToRead(userName, articleList, query):
    # Ask user which article they want to read (0 to cancel, 1-5 for articles, otherwise ask again)
    while True:
        print('IMDBot: Which article you would like to read?')
        user_input = input(f'{userName}: ')
        user_input = user_input.split(" ")
        user_input = [word.lower() for word in user_input]
        if('nevermind' in user_input or sy.findSyns(user_input, 'cancel') == 0 or sy.findSyns(user_input, 'stop') == 0 or sy.findSyns(user_input, 'none') == 0):
            return 
        elif(2 in user_input or sy.findSyns(user_input, 'second') == 0 or sy.findSyns(user_input, 'two') == 0):
            printArticle(articleList[1])
            break
        elif(3 in user_input or sy.findSyns(user_input, 'third') == 0 or sy.findSyns(user_input, 'three') == 0):
            printArticle(articleList[2])
            break
        elif(4 in user_input or sy.findSyns(user_input, 'fourth') == 0 or sy.findSyns(user_input, 'four') == 0):
            printArticle(articleList[3])
            break
        elif(5 in user_input or sy.findSyns(user_input, 'fifth') == 0 or sy.findSyns(user_input, 'five') == 0):
            printArticle(articleList[4])
            break
        elif(1 in user_input or sy.findSyns(user_input, 'first') == 0 or sy.findSyns(user_input, 'one') == 0): # moved to bottom in case someone writes "second one"
            printArticle(articleList[0])
            break
        else:
            print('IMDBot: I\'m sorry, I don\'t understand.')
            continue
    askToReadAnother(userName, articleList, query)

# print article info. Helper for displayResults()
def printArticle(article):
    # print(f'IMDBot: Ok, for the article \'{getTitle(article)}\' which was posted {getDatePosted(article)} by {getSource(article)}, ', end='') # Confirm article selected
    print(f"IMDBot: Here\'s a short description: {article['desc']}")
    print(f'IMDBot: And this is the link to read the full article: {getLink(article)}')
    return

def askToReadAnother(userName, articleList, query):
    while True:
        print('IMDBot: Would you like to read one of the other articles?')
        check = input(f'{userName}: ')
        checkFirst = check[:1].lower() # Save first letter (might only need y or n)
        checkArr = sy.getArray(check, []) # Turn user input into array for synonym checking
        if (checkFirst == 'y' or sy.findSyns(checkArr, 'yes') == 0): # If user said yes
            print('IMDBot: Great! I\'ll list them again.') # acknowledge the yes
            displayResults(articleList, query) # display results again
            askToRead(userName, articleList, query) # ask which they want to read
            return
        elif (checkFirst == 'n' or sy.findSyns(checkArr, 'no') == 0): # If user said no
            return
        else:
            print(f'IMDBot: I\'m sorry, I don\'t understand. ')
            continue

def getLink(article):
    long_url = article['link']
    url_shortener = pyshorteners.Shortener()
    short_url = url_shortener.tinyurl.short(long_url)
    return short_url

def getGoogleNews(userName, googleNews, query):
    try:
        googleNews = searchNews(googleNews, query) # search for news related to the query
        articleList = get5Results(googleNews) # get the top 5 relevant news articles from the results
        displayResults(articleList, query) # display the 5 articles
        askToRead(userName, articleList, query) # ask if the user wants to read any of them. If no, returns False. If yes, the article is displayed and returns True.
        clearSearch(googleNews)
        print('IMDBot: Ok. What else would you like to know?')
        return googleNews
    except:
        clearSearch(googleNews)
        print('IMDBot: Uh oh. Something went wrong and I can\'t continue to look for news.')
        print('IMDBot: What else can I help you with?')
        return googleNews