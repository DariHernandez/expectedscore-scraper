import os
from config import Config
from logs import logger
from scraping_manager.automate import Web_scraping

def main (): 

    # Get credentials
    credentials = Config()
    user = credentials.get('user')
    password = credentials.get('password')

    # Start chrome instance
    web_page = "https://expectedscore.com/"
    scraper = Web_scraping (web_page)

    # Login 
    selector_login_button = "button.login_btn"
    scraper.click (selector_login_button)
    scraper.refresh_selenium ()

    selector_user = 'input[name="USER_LOGIN"]'
    selector_password = 'input[name="USER_PASSWORD"]'
    selector_submit = 'input[type="submit"]'
    scraper.send_data (selector_user, user)
    scraper.send_data (selector_password, password)
    scraper.click (selector_submit)
    scraper.refresh_selenium ()

    input ("end?")
  


if __name__ == "__main__":
    main()