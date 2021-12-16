import os
import time
from config import Config
from logs import logger
from tqdm import tqdm
from scraping_manager.automate import Web_scraping

def main (): 

    # Get credentials
    credentials = Config()
    user = credentials.get('user')
    password = credentials.get('password')

    # Start chrome instance
    logger.info ("Starting chrome...")
    web_page = "https://expectedscore.com/"
    scraper = Web_scraping (web_page)

    # Login 
    logger.info ("Login with credentials...")
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

    # Pagination loop
    current_page = 0
    while True:

        current_page += 1
        logging.info (f"\nCurrent page: {current_page}")

        # Get matches links
        links_matches = []
        selector_matches = '.next-matches-section.allchamp.active > .next-matches-section-page[data-nm-page="1"] > a.next-matches-item'
        elems_matches = scraper.get_elems (selector_matches)
        for match_index in range (1, len (elems_matches) + 1):

            selector_link = f"{selector_matches}:nth-child({match_index})"
            link_match = scraper.get_attrib (selector_link, "href")
            links_matches.append (link_match)

        # Open new empty tab
        logger.info ("Extracting data: ")
        scraper.open_tab ()
        scraper.switch_to_tab (1)
        for link in tqdm(links_matches): 

            # Open match in second tab
            scraper.set_page (link)
            time.sleep (5)

            # TODO:Get match data

        # Close tab
        scraper.end_browser ()
        scraper.switch_to_tab (0) 

        input ("Continue?")
        selector_next = ".next-matches-btn.next"
        classes_next = scraper.get_attrib (selector_next, "class")
        if "disable" in classes_next:
            logger.info ("No more matches. Program end.")



if __name__ == "__main__":
    main()