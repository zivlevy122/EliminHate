import requests

class TelegramBot:
    def __init__(self,telegram_token,chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
           
    def send_message_to_telegram(self,tweet_url,tweet_comment):
        url = f"https://api.telegram.org/bot{ self.telegram_token}/sendMessage"
        
        message = f"{tweet_url}\nSuggested reply:\n{tweet_comment}"
        payload = {"chat_id": self.chat_id, "text": message,  "disable_web_page_preview": False  }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
        else:
            print("Message sent!")
    