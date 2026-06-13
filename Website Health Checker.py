"""

This is my first project using Python!
--------------------------------------
Project: 
Website health status checker

Description: 
This is a simple Python-based project to regularly check a list of website's status. 
If the website is not working (status != "200"), I am notified through Telegram!

Purpose:
This is an automated way to check for deployed websites' status so urgent support can be given.

"""

import requests
import time
import os
from dotenv import load_dotenv

#Load variables from .env files

#Telegram Bot configuration details
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

#Bypass bot detection on certain websites
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" 
}

#List of URLs to check
url = {
        'Codeinplace' : 'https://codeinplace.stanford.edu/cip6/studenthome',
        'Google' : 'https://www.google.com/',
        'Wikipedia' : 'https://www.wikipedia.org/',
        'Github' : 'https://github.com/'
    }

#Function to use Telegram Bot in sending notification once API is down
def send_telegram_notification(message):
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    parse_info = {
        'chat_id' : chat_id,
        'text' : message
    }

    try:
        response = requests.post(telegram_url, json=parse_info)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

#Function to check url status - whether the site is up or currentlty down
def check_url_status(url, timeout = 5):
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        if response.status_code == 200:
            #print('Website is up and running!')
            return True
        else:
            #print('Website is currently down! Please contact the website administrator.')
            return False
    except requests.exceptions.ConnectionError:
        print('Checking failed - connection failed/DNS error')
        return False
    except requests.exceptions.Timeout:
        print(f"Timed out after {timeout} seconds")   
        return False     
    except Exception as e:
        print(f"Failure - Unknown error occurred: {e}.")   
        return False
    
def main():
    #List of websites to test

    while True:
        for key, value in url.items():
            check_status_response = check_url_status(url[key])
            if check_status_response:
                website_status_label = f'{key} is UP AND RUNNING'
                print(website_status_label)
            else:
                website_status_label = f'{key} is currently down! Please contact the website administrator.'
                #print(website_status_label)
                send_telegram_notification(website_status_label)
        
        time.sleep(3,600)

if __name__ == '__main__':
    main()




