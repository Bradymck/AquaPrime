import tweepy

consumer_key = 'TWITTER_KEY'
consumer_secret = 'TWITTER_SECRET'
access_token = 'TWITTER_ACCESS_TOKEN'
access_token_secret = 'TWITTER_ACCESS_SECRET'

# Authentication with OAuth 1.0a User Context
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

# Create a subclass of tweepy.StreamingClient
class MyStream(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(tweet.text)
        # Ensure the tweet is not from the bot itself to avoid a self-reply loop
        if tweet.author_id != self.client.authenticated_user_id:
            # Respond to the tweet
            api.update_status('@' + tweet.author.screen_name + ' Your response here!',
                              in_reply_to_status_id=tweet.id)

# Initialize MyStream with your bearer token
myStream = MyStream(bearer_token=access_token)

# Add rules to your stream for the keywords
myStream.add_rules(tweepy.StreamRule("keyword1"))
myStream.add_rules(tweepy.StreamRule("keyword2"))

# Start streaming
# You should specify the fields you need in the stream
myStream.filter(tweet_fields=["author_id", "conversation_id"])
