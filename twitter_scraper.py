from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from twitter_bot import TwitterBot
from telegram_bot import TelegramBot
import os
# import requests

#from google import genai
import google.generativeai as genai


def generate_ai_reply(client,tweet_text):
    prompt = (
        "Analyze the following tweet and write a short, polite reply (no longer then 1-2 sentences) "
        "that supports Israel's perspective and counters any misinformation. "
        "Keep it factual and neutral, avoid aggressive language.\n\n"
        f"Tweet: {tweet_text}"
        )


    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
    )
    return response.text


def ai_reply(key, tweets):
    genai.configure(api_key=key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash") 
    
    chat =gemini_model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "Analyze the following tweet and write a short, polite reply (no longer then 1-2 sentences) "
        "that supports Israel's perspective and counters any misinformation. "
        "Keep it factual and neutral, avoid aggressive language.\n"
        ]
    }
])
   
    
    respones = []
    for tweet in tweets:
        respones.append(chat.send_message(tweet.get("text")).text)
        
    return respones
        

    
       
      
if __name__ == "__main__":
    load_dotenv()
    #keys
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
  
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    
    
    GEMINI_KEY = os.getenv("GEMINI_KEY")
    
    #Telegram bot - for searching tweets
    #GPT client - for generate a pro-israeli comment
    #Telegram bot - for sendinf tweet and suggestion comment 
    Telegram_bot = TelegramBot(TELEGRAM_TOKEN,CHAT_ID)
    X_bot = TwitterBot(BEARER_TOKEN,True) #true = test. false = real
    # gemini_client = genai.Client(api_key=GEMINI_KEY)
    
   
   
   #Time - for not double searching
    end_time = datetime.now(timezone.utc)- timedelta(seconds=20)
    start_time =  end_time - timedelta(days=1)
    print(f"Searching tweets from {start_time} to {end_time}")
    
    tweets = X_bot.search_tweets("free palestine", 10,start_time,end_time)
    respones = ai_reply(GEMINI_KEY,tweets)
    
    if tweets:
        print("\nTweet URLs found:")
        for tweet,response in zip(tweets,respones):
            # ai_comment = generate_ai_reply(gemini_client,tweet.get("text"))
            Telegram_bot.send_message_to_telegram(tweet.get("url"),response)



                
                
                
                
    
    
        
    
    
        
