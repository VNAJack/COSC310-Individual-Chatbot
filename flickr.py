import flickrapi
import webbrowser

api_key = u'c928c5eb2b5d2bf99fb65017ad1a16b1'
api_secret = u'3f371a1546ec7fb1'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')

# print('Step 1: authenticate')
# 
# # Only do this if we don't have a valid token already
# if not flickr.token_valid(perms='read'):

#     # Get a request token
#     flickr.get_request_token(oauth_callback='oob')

#     # Open a browser at the authentication URL. Do this however
#     # you want, as long as the user visits that URL.
#     authorize_url = flickr.auth_url(perms='read')
#     webbrowser.open_new_tab(authorize_url)

#     # Get the verifier code from the user. Do this however you
#     # want, as long as the user gives the application the code.
#     verifier = str(input('Verifier code: '))

#     # Trade the request token for an access token
#     flickr.get_access_token(verifier)

# print('Step 2: use Flickr')
# resp = flickr.photos.getInfo(photo_id='7658567128')

# 898-931-188


# f = FlickrAPI(api_key='c928c5eb2b5d2bf99fb65017ad1a16b1',
#           api_secret='3f371a1546ec7fb1',
#           #callback_url='http://www.example.com/callback/'
#           )

# auth_props = f.get_authentication_tokens()
# auth_url = auth_props['auth_url']

# #Store this token in a session or something for later use in the next step.
# oauth_token = auth_props['oauth_token']
# oauth_token_secret = auth_props['oauth_token_secret']

# print 'Connect with Flickr via: %s' % auth_url




# Public feed
# search = '?format=php_serial&tags=RyanReynolds'

# url = 'https://www.flickr.com/services/feeds/photos_public.gne'
# search_url = url + search

# data = file_get_contents(search_url)

# photos = data['items']

# for photo in photos:
#     print('src=' + photo['photo_url'])