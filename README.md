# **Movie Chat Bot**

## COSC 310 Final Project (Individual Assignment)

Per the Final Project description, Assignment 3 was imported to this repository for the purpose of individual work.

**NOTE FOR THE TA:**

>To identify sections that were added for this project, I added the note "(Final Project)" to the updated and added areas of this README file so that the TA can Ctrl+F to easily find all the areas that were updated or added for this individual assignment. These notes are also included in the Table of Contents to assist with navigation.

Other parts of the project were changed for this project for the purpose of integration, smoother conversation, and error handling and are documented within the code's comments.

## Table of Contents
* [General Information](#general-information) (updated for Final Project)
* [Language and Modules](#language-and-modules) (updated Final Project)
* [Setup](#setup) (updated for Final Project)
* [Classes](#classes)
  - [Main Class](#main-class) (updated for Final Project)
  - [Commands and IMDbPy integration](#commands-and-imdbpy-integration) (updated for Final Project)
  - [Natural Language Processing](#natural-language-processing) (updated for Final Project)
  - [Testing](#testing)
  - [GUI](#gui)
  - [Twitter API](#twitter-api) (__added__ for Final Project)
  - [Google News](#google-news) (__added__ for Final Project)
* [Future Considerations](#future-considerations) (updated for Final Project)


## General Information

This project has resulted in the creation of a responsive and interactive chatbot named IMDBot using Python. IMDBot takes on the role of a friend who is very knowledgeable about movies and utilizes the following libraries: IMDbPY, spaCy, nltk, pyspellchecker, chatterbot, Tweepy, and GoogleNews. With these libraries IMDBot can answer questions about movies, actors, directors, and production companies, check the latest tweet by famous people, and provide the relevant and recent news about people, movies, and companies.

## Language and Modules

- Python 3.6.5
- IMDbPY Library
- nltk 3.4.4
- spaCy 3.0.5 **with** Pipelines en_core_web_sm 3.0.0
- pyspellchecker 0.6.1 
- chatterbot 1.0.2
- tweepy 3.10.0 *(Final Project)*
- GoogleNews 1.5.7 *(Final Project)*
- pyshorteners 1.0.1 *(Final Project)*

## Setup

1. In order to use this code to its full extent, please ensure you have Python 3.6.5 installed. Not all libraries are compatible with other versions of Python. It is recommended to create a separate environment to avoid Python version issues.

2. Ensure you have all of the required libraries installed. You can do this through pip and Python by running the following:

> $ pip install IMDBPy 

> $ pip install spacy

> $ pip install spacy-lookups-data

> $ python -m spacy download en_core_web_sm

> $ pip install pyspellchecker

> $ pip install nltk

> $ pip install chatterbot

> $ pip install chatterbot-corpus (Optional; See chatterTrainer.py under [Trainers/Utility](#trainers/utility))

> $ pip install tweepy

> $ pip install GoogleNews

> $ pip install pyshorteners

3. Download the necessary corpora, and then exit the interpreter using the following steps:

> $ Python

> *>>>* import nltk

> *>>>* nltk.download('wordnet')

> *>>>* nltk.download('punkt')

> *>>>* nltk.download('averaged_perceptron_tagger')

> *>>>* exit()

4. Make sure the code will be running on the file directory. If using Visual Studio Code, you can ensure you have it running on the directory with these steps:
    - Go to settings or use the shortcut: ctrl + ,
    - Type "execute in file dir"
    - Check the box for "When executing a file in terminal, whether to use execute the file's directory, instead of the current open folder"

5. Run the bot using the following command from within the project's main directory.

> $ python IMDBot.py

## Classes

This project has four core parts that make it work:

1. The IMDb integration and the functions that allow the bot to output the requested information 
2. The classes that handle natural language processing and allow the bot to better understand the user's inputs
3. The Twitter API integration, which - upon authorization by the user - can look up the latest tweets by famous people with the user's own Twitter account and allow them to 'like' tweets.
4. The Google News integration that will look up relevant and recent news about people, movies, and companies.

To see the class structure of the IMDb integration and natural language processing, take a look at the [Assignment 3 UML Diagram](https://lucid.app/publicSegments/view/aebe824d-31ce-4685-9720-e142ce18f0fb/image.pdf). Please note this was __not__ updated for the Final Project.

### Main Class

#### [IMDBot.py](IMDBot.py)

 - Main file that the user runs; it contains the conversation loop of  if-elif-statements that look for key words from the user input
 - Inherits the other classes
 - Handles major exceptions gracefully, and quick ctrl+c shutdown has also been implemented.
 - Updates and additions were made for the integration of Twitter and Google News *(Final Project)*

### Commands and IMDbPy integration

#### [user.py](user.py)

- Requests the name of the current user so that IMDBot can refer to the user by the specified name and for interface use.
- Lets the user change their name upon request

#### [film.py](film.py)

- Uses the IMDbPY library to
  - find a movie based on the movie title provided by the user
  - find the main director of a movie
  - provide a summary of a movie
  - list the characters of a movie
  - provide the runtime of a movie
  - find which actor played a specific character in a movie -- [twitter.py](#twitter.py) is incorporated to enhance the search experience. *(Final Project)*

#### [person.py](person.py)

- This class handles commands related to people in the movie industry, this includes, actors, directors and other crewmembers.
- Finds the movies a person has worked
- Provides general biographical information about actors and directors
- Checks if an individual has worked in a specific movie.
- Error handling was improved for the integration of [Google News](#google-news) *(Final Project)*

#### [company.py](company.py)

- Finds the main production company of a movie based on the given movie title
- Determines whether a production company worked on specific movies or if a movie is in the company's repertoire.
- Smoothed some interactions and added more error handling to ensure it works smoothly with [Google News](#google-news) *(Final Project)*

### Natural Language Processing

#### [ner.py](ner.py)

- This class handles named entity recognition. It breaks down user input in a way that allows the chatbot to discern whether a user is asking about a certain movie, person, or company within a sentence.

#### [synonyms.py](synonyms.py)

- This class handles synonym recognition, which allows the bot to understand what a user input means even if certain words haven't been hardcoded.
- It is based off of the wordnet training corpus for accuracy.

#### [spellinghandler.py](spellinghandler.py)

- Ensures that any misspelt words are properly corrected in the user input before any other class processes it.
- It fixes any spelling mistakes to prevent runtime errors in later processing.

#### [postagging.py](postagging.py)

- Facilitates the breaking down of a sentence into its basic parts, it can tag nouns, verbs, etc.
- This makes the bot more able to understand the subject and reason for a user input, making commands easier to communicate.

#### Trainers and Utility

- the classes [nerTrainer.py](nerTrainer.py) and [nerTrainerHelp.py](nerTrainerHelp.py) work in tandem
  - nerTrainer has a vast collection of custom training cases as a corpus for the named entity recognition object to use.
    - Additional training cases were added for the integration of Twitter and Google News *(Final Project)*
  - nerTrainerHelp provides a template for developers to create training cases related to people, movies, and companies.

- chatterTrainer.py trains the chatterbot object used for generating procedural responses, it only needs to be run once to train, but can be run again if training   cases are added. The neural network training is stored in db.sqlite3 so that training doesn't have to occur at runtime. (To retrain and run chatterTrainer.py, you   must install chatterbot-corpus).
   

### Testing

#### [test_IMDBot.py](test_IMDBot.py)
- Runs all the unittest functions to ensure proper code functionality.
- Gives the bot example inputs to test if it can understand commands as natural language.

### GUI

#### [gui.py](gui.py)

- Builds and runs a GUI container for chatbot interaction
- This GUI is more of a proof of concept, as time constraints prevented implementation to the main runtime.
- It can be run to see what it would look like, but chatbot interaction is nonfunctional

### Twitter API
#### [twitter.py](twitter.py)
*(Final Project)*
- Before the Twitter API can be used, `enableTwitter()` is called on startup to ask for the user's permission to connect to their Twitter account.
  - If the user denies this request, then the Twitter API functionality is disabled
  - If the user approves this request, then `authenticateTwitter()` is used to provide instructions and open a web page where the user can (a) read more details about the permission, and (b) authorize or cancel the process
  - The user can enable or disable the Twitter API at any time using the key words "enable Twitter" or "disable Twitter" in their conversation with IMDBot, so the user has full control over the bot's connection to their Twitter account.
- Functions:
  - `findUser()` Finds the Twitter account of a famous person based on the name provided by the user or from the name of an actor or director that was found with IMDbPY. It then prints the Twitter Handle of the account that was found to be associated with the name.
  - `getLatestTweet()` Finds the latest tweet or 'status' of the found Twitter account.
  - `printTweet()` Prints the latest tweet to the console and presents the tweet's URL.
  - `askToLikeTweet()` Asks the user if they want to 'like' the tweet if it is not already 'liked'
  - `printLatestTweet()` is the function used in [IMDBot.py](#IMDBot.py) and [film.py](#film.py). It calls the aforementioned functions in order, and it also uses appropriate error handling.
- The latest tweet by an actor or director is found and printed when:
  - specifically requested by the user in their conversation with IMDBot (i.e. "What is [actor-name]'s latest tweet?")
  - the user searches for an actor or director (i.e. "Who played [character-name] in [movie-title]?")


### Google News

#### [googleNews.py](googleNews.py)
*(Final Project)*
- Upon program startup, Google News is initialized with English as the language setting via `enableGoogleNews()`
- Functions:
  - `searchNews()` searches for relevant and recent news about the person, movie, and/or company that was specified by the user and stores it in the Google News object.
  - `get5Results()` gets the top 5 news articles and adds them to a list.
  - `displayResults()` prints the title, date posted, and source of the 5 news articles.
  - `askToRead()` prompts the user if they want to read any of the 5 articles. Uses natural language processing so that the user can write their answer as a sentence - not just a number. If the user indicates they want to read an article, then these functions are called:
    - `printArticle()` prints a short description of the article and provides a tiny url (imported library pyshorteners) to the full article.
    - `askToReadAnother()` prompts the user if they want to read another article. Recursion is used with `askToRead()` to continue the interaction until the user indicates they do not want to read another article.
  - `clearSearch()` is used after the user is done with the articles to delete the search results from the Google News object.
  - `getGoogleNews()` is the only function used in [IMDBot.py](#IMDBot.py). It calls the aformentioned functions and handles errors gracefully.

## Future Considerations

- GUI implementation
- Larger corpora for the trainers
- Additional API integrations
- POS Tagging improvements regarding interfunctionality
- Refactoring of the program so that all user interactions occur in the main class to allow for natural language processing of each time a user provides input.
