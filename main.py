# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 18:05:00 2016

@author: @ceeflyer
"""
from requests_oauthlib import OAuth1Session
import sys

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
#LISTS_LIST_URL = 'https://api.twitter.com/1.1/lists/list.json?screen_name=ceeflyer'
LISTS_STATUSES_URL = 'https://api.twitter.com/1.1/lists/statuses.json?list_id=738212830285946880&count=20'

CONSUMER_KEY='2obWL9WLQLobUOqtwzBrPoGHD'
CONSUMER_SECRET='wevyRd9x2m3Mcu7ECMj045g6xJbXBfKRfC1rCIqEEat4UlG5pR'

# Set up oauth
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, 
                      callback_uri='oob')
# Fetch request token
oauth.fetch_request_token(REQUEST_TOKEN_URL)
# Get authorisation URL
auth_url = oauth.authorization_url(AUTHORIZE_URL)

print('Please access to', auth_url, 'and get verifier code.')

# Parse authorisation response
resp = oauth.parse_authorization_response(auth_url)

verifier = input('Input verifier: ')
# Fetch access token
oauth.fetch_access_token(ACCESS_TOKEN_URL, verifier)
# Make actual access to Twitter
req = oauth.get(LISTS_STATUSES_URL)

# Do some test
output = req.json()
media_urls = []
try:
    print(len(output), 'tweets have picked.')
    for tweet in output:
        entity = tweet.get('entities')
        media = entity.get('media')
        if media is None:
            print('No media have found on', tweet.get('id_str'))
        else:
            for media_item in media:
                url = media_item.get('media_url_https')
                print('Found:', url)
                media_urls.append(url)
except:
    print('Tweets cannot be picked.', sys.exc_info()[0])

print('Finally,', len(media_urls), ' images have found.')
#print(json.dumps(output))

