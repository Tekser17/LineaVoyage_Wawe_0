import json
import os
import time
from croco_selenium import ChromeDriver

from appconnect.twitter import Twitter
from logs.logger import Logger
from globals import EXTENSIONS_PATH, PROJECT_PATH
from appconnect.discord import Discord
from appconnect.email import Email

logger = Logger("main_py")
metamask_extension_paths = [os.path.join(PROJECT_PATH, 'extensions/nkbihfbeogaeaoehlefnkodbefgpgknn.crx')]

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())


def parse_discord_accounts():
    discord_accounts = []
    with open('accounts/discord_accounts.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(':')
            email = parts[0]
            password = parts[1]
            token = parts[2]
            discord_accounts.append([email, password, token])
    return discord_accounts


def parse_twitter_accounts():
    twitter_accounts = []
    with open('accounts/twitter_accounts.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(':')
            username = parts[0]
            password = parts[1]
            email = parts[2]
            auth_token = parts[-1].split(';')[-1]
            twitter_accounts.append([username, password, email, auth_token])
    return twitter_accounts


def main():
    driver = ChromeDriver(extension_paths=metamask_extension_paths)
    time.sleep(5)
    driver.close_tabs()
    time.sleep(1)
    twitter_accounts = parse_twitter_accounts()
    discord_accounts = parse_discord_accounts()
    for twitter_account in twitter_accounts:
        email_ = Email(twitter_account[2], twitter_account[1])
        print(email_)
        twitter = Twitter(driver, twitter_account[1], email_)
        twitter.sign_in()



    for discord_account in discord_accounts:
        email_ = Email(discord_account[0], discord_account[1])
        discord = Discord(driver, discord_account[1], email_, discord_account[2])
        discord.sign_in()

    time.sleep(10)
    driver.close_tabs()
    time.sleep(1)
    driver.get('https://www.intract.io/linea/quest/654a0e8e95c012164b1f1683')

    time.sleep(15)



if __name__ == '__main__':
    main()