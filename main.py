import json
import time
from croco_selenium import ChromeDriver
from seldegen.socials import Twitter
from globals import METAMASK_PATH
from seldegen.socials import Discord
from seldegen import Email, Metamask

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


def parse_private_keys():
    private_keys = []
    with open('accounts/private_keys.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            private_keys.append(line.strip())
    return private_keys


def main():
    driver = ChromeDriver(extension_paths=[METAMASK_PATH])
    timeout = 15

    time.sleep(5)
    driver.close_tabs()
    time.sleep(2)

    twitter_accounts = parse_twitter_accounts()
    discord_accounts = parse_discord_accounts()
    private_keys = parse_private_keys()

    for idx, private_key in enumerate(private_keys):

        twitter_account = twitter_accounts[idx]
        email_ = Email(twitter_account[2], twitter_account[3])
        twitter = Twitter(driver, twitter_account[1], email_, twitter_account[0])
        twitter.sign_in()
        time.sleep(5)
        if driver.current_url == 'https://twitter.com/i/flow/login':
            # ....
            driver.quit()
            continue

        discord_account = discord_accounts[idx]
        email_ = Email(discord_account[0], discord_account[1])
        discord = Discord(driver, discord_account[1], email_, discord_account[2])
        discord.sign_in()
        driver.refresh()

        time.sleep(3)

        metamask = Metamask.sign_up(driver, 'Password123')
        metamask.import_account(private_key)
        time.sleep(3)

        driver.get('https://www.intract.io/linea/quest/654a0e8e95c012164b1f1683')
        time.sleep(5)
        driver.click(timeout, '/html/body/intract/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div')  # Меню выбора кошелька
        driver.click(timeout, '//*[@id="centered-modal"]/div/div/div/div[3]/div/div[2]/div[1]')  # Выбор metamask
        time.sleep(4)
        metamask.connect()
        time.sleep(8)
        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            break
        time.sleep(3)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > section:nth-child(3) > span:nth-child(2) > section").click()""")
        time.sleep(3)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.container.p-0 > div > div > div.col-12.col-lg-7.col-xxl-8.h-100.mx-0.px-0.d-lg-block > div > div > div.swiper.swiper-initialized.swiper-horizontal.swiper-pointer-events.swiper-watch-progress.overflow-hidden > div > div.swiper-slide.swiper-slide-visible.swiper-slide-active > div > div.d-flex.flex-column.form-input-width > div").click()""")
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        #time.sleep(8)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.w-100.quest-navigation.entered.pe-lg-5.pe-0 > div > div > div > div > div:nth-child(2) > button").click()""")
        time.sleep(2)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.container.p-0 > div > div > div.col-12.col-lg-7.col-xxl-8.h-100.mx-0.px-0.d-lg-block > div > div > div.swiper.swiper-initialized.swiper-horizontal.swiper-pointer-events.swiper-watch-progress.overflow-hidden > div > div.swiper-slide.swiper-slide-visible.swiper-slide-active > div > div.d-flex.flex-column.form-input-width > div").click()""")
        time.sleep(3)
        driver.execute_script("""document.querySelector("#centered-modal > div > div > div > div.modal-body.h-100.p-1.p-sm-4.position-relative.overflow-hidden > div.mt-0.p-3.position-relative > div.mt-5 > div").click()""")
        time.sleep(5)
        twitter.connect()
        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            break
        time.sleep(5)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.container.p-0 > div > div > div.col-12.col-lg-7.col-xxl-8.h-100.mx-0.px-0.d-lg-block > div > div > div.swiper.swiper-initialized.swiper-horizontal.swiper-pointer-events.swiper-watch-progress.overflow-hidden > div > div.swiper-slide.swiper-slide-visible.swiper-slide-active > div > div.d-flex.flex-column.form-input-width > div").click()""")
        time.sleep(4)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.w-100.quest-navigation.entered.pe-lg-5.pe-0 > div > div > div > div > div:nth-child(2) > button").click()""")
        time.sleep(3)
        driver.execute_script("""document.querySelector("#root-container > div > div:nth-child(3) > div > div > div > section:nth-child(4) > div > div.container.p-0 > div > div > div.col-12.col-lg-7.col-xxl-8.h-100.mx-0.px-0.d-lg-block > div > div > div.swiper.swiper-initialized.swiper-horizontal.swiper-pointer-events.swiper-watch-progress.overflow-hidden > div > div.swiper-slide.swiper-slide-visible.swiper-slide-active > div > div.d-flex.flex-column.form-input-width > div").click()""")
        time.sleep(1)
        driver.execute_script(""""document.querySelector("#centered-modal > div > div > div > div.modal-body.h-100.p-1.p-sm-4.position-relative.overflow-hidden > div.mt-0.p-3.position-relative > div.mt-5 > div").click()""")


    time.sleep(2022)
    for twitter_account in twitter_accounts:
        email_ = Email(twitter_account[2], twitter_account[3])
        print(email_)
        twitter = Twitter(driver, twitter_account[1], email_, twitter_account[0])
        twitter.sign_in()
        time.sleep(100)

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
