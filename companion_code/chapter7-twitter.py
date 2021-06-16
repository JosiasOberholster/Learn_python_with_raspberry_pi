import twitter

def print_tweets(tweets):
    for tweet in tweets:
        print('text: ', tweet['text'])
        print('from: ', tweet['user']['screen_name'])

twitter_user = twitter.Twitter(
    auth=twitter.OAuth("ACCESS-TOKEN","ACCESS-TOKEN-SECRET", "CONSUMER-KEY","CONSUMER-SECRET"))

status = twitter_user.statuses

home = status.home_timeline()
print("home")
print_tweets(home)

mentions = status.mentions_timeline()
print("mentions")
print_tweets(mentions)

search_string = input("Enter text to search for, or press enter to skip: ")
if search_string != "":
    search = twitter_user.search.tweets(q=search_string)
    print("search")
    print_tweets(search['statuses'])

tweet = input("Enter tweet, or press enter to exit: ")

if tweet != "":
    twitter_user.statuses.update(status=tweet)