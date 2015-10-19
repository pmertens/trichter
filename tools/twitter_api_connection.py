# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
import simplejson
import pdb
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import os

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "1MD9HjL7qB01D4vhKGXZL9WlX"
CONSUMER_SECRET = os.environ.get('TRICHTER_CONSUMER_SECRET')

OAUTH_TOKEN = "177422243-j4RozosnmhsmynM8A0i0lWTIj4bfzbM4bNE6xlh3"
OAUTH_TOKEN_SECRET = os.environ.get('TRICHTER_OAUTH_TOKEN_SECRET')


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = get_oauth()
        payload = {
        'user_id': '5943622',
        'count': 200,
        'exclude_replies': 'true',
        }
        r = requests.get(
        	url="https://api.twitter.com/1.1/statuses/user_timeline.json",
        	params=payload,
        	auth=oauth
        	)
        tweets = r.json()
        for tweet in tweets:
        	print tweet.get('text')
