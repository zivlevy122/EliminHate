import tweepy
from datetime import datetime, timedelta, timezone

class TwitterBot:
    def __init__(self,bearer_token,test_mode=False):
        # Initialize the Client with the Bearer Token
        self.client = tweepy.Client(bearer_token=bearer_token)  if not test_mode else None
        self.history_tweets = "sent_urls.txt"
        self.test_mode = test_mode
    
    def append_urls_to_history(self,start_time, end_time ,tweets):
        #save sent URLs
        with open(self.history_tweets, 'a', encoding='utf-8') as f:
            f.write(f"\nTweets from {start_time} to {end_time}:\n")
            for tweet in tweets:
                f.write(f"{tweet.get("url")}\n")                
    
    
    def search_tweets(self, hashtag,max_results,start_time,end_time):
        # search (number max_result) new tweets by the hasttag. return the tweet link
        # Uses time filtering to reduce API usage
        # date = YYYY-MM-DD
        new_tweets = []
        if self.test_mode:
            print("Running in TEST MODE (no API call)")
            
            fake_tweets = [{"username": "piii_98", "tweetid":"1948980151066165620", "text": "The world lives with these demons, it doesn't matter who the person in front of them is, a child or a woman, just kill quietly"}
                             ,{"username": "YosephHaddad", "tweetid":"1949207207142137903","text":"An Israeli DJ was not allowed to perform on the Tomorrowland stage due to 'security reasons' - but who did come on stage to play tonight? A DJ wearing a shirt with the Palestinian flag and a drawing of the Land of Israel from the river to the sea.What a disgrace this festival is! A festival of hypocrisy!!"}
                        #    {"username": "GlobeEyeNews", "tweetid":"1949212183080079607","text": "BREAKING: ChatGPT CEO Sam Altman says people share personal info with ChatGPT but don’t know chats can be used as court evidence in legal cases."}
                        ]
            
            for tweet in fake_tweets:
                link = f"https://twitter.com/{tweet.get('username')}/status/{tweet.get('tweetid')}"
                new_tweets.append({"url":link, "text": tweet.get("text")})
                
        else:            
            try:
                query = f"#{hashtag} -is:retweet"
                
                # if date:
                #     query += f" since:{date}"
                #     print(f"Searching tweets since: {date}")
                
                response = self.client.search_recent_tweets(
                    query=query,
                    max_results=max_results,
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat(),
                    #tweet_fields=['created_at', 'public_metrics', 'author_id'],
                    expansions=['author_id'],
                    user_fields=['username']
                )
                
                if not response.data:
                    print("No tweets found")
                    return []
                
                # Get user info for building URLs
                # map user id to user name
                users = {user.id: user.username for user in response.includes.get('users', [])}
                                
                for tweet in response.data:
                    username = users.get(tweet.author_id, 'unknown')
                    link = f"https://twitter.com/{username}/status/{tweet.id}"
                    new_tweets.append({"url":link, "text":tweet.text})
                    
            except tweepy.TooManyRequests:
                print("Rate limit exceeded. Wait!")
                return []
            except Exception as e:
                print(f"Error: {e}")
                return []
                    
        if new_tweets: 
            self.append_urls_to_history(start_time,end_time,new_tweets)
        return new_tweets
            