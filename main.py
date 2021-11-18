from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests
import argparse

load_dotenv()

def shorten_link(token, url):
    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    
    bitlink = response.json()['link']
    
    return bitlink

def count_clicks(token, link):
    link_parts = urlparse(link)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link_parts.netloc}{link_parts.path}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    return response.json()['total_clicks']

def is_bitlink(token, url):
    link_parts = urlparse(url)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link_parts.netloc}{link_parts.path}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(api_url, headers=headers)
    
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='link or BitLink')
    args = parser.parse_args()
    user_link = args.link

    auth_token = os.getenv('BITLY_TOKEN')
    try:
        if is_bitlink(auth_token, user_link):
            print(f'По вашей ссылке прошли: {count_clicks(auth_token, user_link)} раз(а)')
        else:
            bitlink = shorten_link(auth_token, user_link)
            print('Битлинк: ', bitlink)
    except requests.exceptions.HTTPError:
        print('Вы указали неверную ссылку')
