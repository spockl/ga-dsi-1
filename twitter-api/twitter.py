from TwitterAPI import TwitterAPI

access_token_key = "3546434294-fAPQoZ3aTYyZAouLESOSf8OTsXIpOD0a5YE4BDE"
access_token_secret = "K7RNSX4NDGJEfh26mqYqpowQ54WZa6fyCfnyH4dSb9R7m"

api_key = "isbH41qVfiP4hGAolaa8FrodB"
api_secret = "izIIMJpcLrNudIhANwC5NiAwMCtK0wtxLotjDkbTEJFX2ooeiB"

_debug = 0


api = TwitterAPI(api_key, api_secret, access_token_key, access_token_secret)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''

def retrieve_tweets(topic,
                    url="https://stream.twitter.com/1/statuses/filter.json",
                    method="GET", ):
    """

    Params:
    topic - must be in this format "#topic" or '@handle"
    Returns
    """
    response = api.request('statuses/filter', {'track': topic})
    if response.status_code != 200:
        raise ValueError("Unable to retrieve tweets, please check your API credentials")
    for x in response:
        try:
            yield x
        except UnicodeError as unicode_error:
            continue
