import os
import time
import datetime
from tqdm import tqdm
from logs import logger
from config import Config
from api_post import try_request
from spreadsheet_manager.xlsx import SS_manager
from scraping_manager.automate import Web_scraping

scraper = Web_scraping ("about:blank")

# Get credentials
credentials = Config()
user = credentials.get('user')
password = credentials.get('password')
send_data = credentials.get('send_data')
api_url = credentials.get('api_url')

def login (current_tab=0):

    # Start chrome instance
    logger.info ("\nStarting chrome...")
    web_page = "https://expectedscore.com/"
    scraper.set_page (web_page)

    # Login 
    logger.info ("Login with credentials...")
    selector_login_button = "button.login_btn"
    scraper.click (selector_login_button)
    scraper.refresh_selenium(back_tab=current_tab)

    selector_user = 'input[name="USER_LOGIN"]'
    selector_password = 'input[name="USER_PASSWORD"]'
    selector_submit = 'input[type="submit"]'
    scraper.send_data (selector_user, user)
    scraper.send_data (selector_password, password)
    scraper.click (selector_submit)
    scraper.refresh_selenium(back_tab=current_tab)

def main (): 

    login ()

    # Pagination loop
    current_page = 0
    current_row = 2
    while True:

        current_page += 1
        logger.info (f"\nCurrent page: {current_page}")

        # Get matches links
        links_matches = []
        selector_matches = '.next-matches-section.allchamp.active > .next-matches-section-page.active > a.next-matches-item'
        elems_matches = scraper.get_elems (selector_matches)
        for match_index in range (1, len (elems_matches) + 1):

            selector_link = f"{selector_matches}:nth-child({match_index})"
            link_match = scraper.get_attrib (selector_link, "href")
            links_matches.append (link_match)

        # Open new empty tab
        logger.info ("Extracting data: ")
        scraper.open_tab ()
        scraper.switch_to_tab (1)
        
        # Matches loop
        page_data = []
        for link in tqdm(links_matches): 

            # Open match in second tab
            scraper.set_page (link)
            time.sleep (3)

            # Validate url
            url = scraper.driver.current_url
            if url == "https://expectedscore.com/404.php":
                continue

            # Catch login time out error
            selector_error = ".access-denied-xg-block > .access-denied-xg-title"
            error_text = str(scraper.get_text (selector_error))
            if "not have sufficient rights" in error_text:
                scraper.open_tab ()
                scraper.switch_to_tab (2)
                login (current_tab=2)
                scraper.end_browser()
                scraper.switch_to_tab (1)
                scraper.driver.refresh ()
                time.sleep (3)
                scraper.refresh_selenium (back_tab=1)

            # Go to Standing page
            selector_standing = ".about-match-page__nav > .menu-btn.spreadsheet"
            scraper.click (selector_standing)
            time.sleep (3)
            scraper.refresh_selenium (back_tab=1)

            selector_base = '.tournament-table__body > div[mode="out-in"] > .row'
            selectors_teams = [
                f"{selector_base}.first-team", 
                f"{selector_base}.second-team"
            ]

            # Teams loop
            match_data = []
            for selector_team in selectors_teams:

                selector_columns = f"{selector_team} > div.cell"

                # Get columns
                while True:
                    columns_elem = scraper.get_elems (selector_columns)
                    if not columns_elem:
                        time.sleep (2)
                        scraper.refresh_selenium(back_tab=1)
                    else:
                        break

                # Columns loop
                team_data = []
                for column_index in range (1, len(columns_elem) + 1):

                    # Get columns data
                    selector_column = f"{selector_columns}:nth-child({column_index})"
                    column_value = scraper.get_text (selector_column)

                    # Convert to number
                    try:
                        column_value = float(column_value)
                    except:
                        pass

                    team_data.append (column_value)

                match_data.append (team_data)

            # Get max number or teams
            teams_num_selector = '.tournament-table__body > [mode="out-in"] > div:last-child > div:first-child'
            teams_num = scraper.get_text (teams_num_selector)

            match_data.append (teams_num)
            match_data.append (url)
            page_data.append (match_data)

        # Loop for format data
        logger.info("Formating data and sendint to API...")
        saved_matches = []
        for match_data in page_data:

            # Format data to write in spreadsheet
            formated_row = []
            match_name = f"{match_data[0][1]} - {match_data[1][1]}"
            formated_row.append (match_name)
            saved_matches.append (match_name)
            for team_data in match_data[:2]:

                # Get data
                position = team_data[0]
                team = team_data[1]
                p = team_data[2]
                ptos = team_data[9]
                gd_xgd = team_data[13]
                xg_sh = team_data[14]
                xga_sh = team_data[15]
                xg90 = team_data[16]
                xga90 = team_data[17]
                xg90_xga90 = team_data[18]
                xg90__xga90 = team_data[19]
                xg90_03_max	= team_data[20]
                xga90_03_max = team_data[21]
                xg90_xga90_03_max = team_data[22]
                xg90__xga90_03_max = team_data[23]
                xg90_index = team_data[24]
                xga90_index = team_data[25]
                xg90_noindex = team_data[26]
                xga90_noindex = team_data[27]
                xg90_xga90_noindex = team_data[28]
                xg90__xga90_noindex = team_data[29]

                # Save data in correct order
                formated_row.append (position)
                formated_row.append (team)
                formated_row.append (p)
                formated_row.append (ptos)
                formated_row.append (gd_xgd)
                formated_row.append (xg_sh)
                formated_row.append (xga_sh)
                formated_row.append (xg90)
                formated_row.append (xga90)
                formated_row.append (xg90_xga90)
                formated_row.append (xg90__xga90)
                formated_row.append (xg90_03_max)
                formated_row.append (xga90_03_max)
                formated_row.append (xg90_xga90_03_max)
                formated_row.append (xg90__xga90_03_max)
                formated_row.append (xg90_index)
                formated_row.append (xga90_index)
                formated_row.append (xg90_noindex)
                formated_row.append (xga90_noindex)
                formated_row.append (xg90_xga90_noindex)
                formated_row.append (xg90__xga90_noindex)

            formated_row.append (match_data[-2])
            formated_row.append (match_data[-1])            

            # Format params
            params = {
                "match": formated_row[0],
                "match_date": datetime.datetime.now(),
                "position_home": int(formated_row[1]),
                "team__home": formated_row[2],
                "played_home": formated_row[3],
                "pts_home": formated_row[4],
                "gd_xgd_home": formated_row[5],
                "xg_sh_home": formated_row[6],
                "xga_sh_home": formated_row[7],
                "xg90_home": formated_row[8],
                "xga90_home": formated_row[9],
                "xg90_xga90_plus_home": formated_row[10],
                "xg90_xga90_div_home": formated_row[11],
                "xg90_0_3_max_home": formated_row[12],
                "xga90_0_3_max_home": formated_row[13],
                "xg90_xga90_plus_03_max_home": formated_row[14],
                "xg90_xga90_div_0_3_max_home": formated_row[15],
                "xg90_index_home": formated_row[16],
                "xga90_index_home": formated_row[17],
                "xg90_no_index_home": formated_row[18],
                "xga90_no_index_home": formated_row[19],
                "xg90_xga90_plus_no_index_home": formated_row[20],
                "xg90_xga90_div_no_index_home": formated_row[21],
                "position_away": int(formated_row[22]),
                "team_away": formated_row[23],
                "played_away": formated_row[24],
                "pts_away": formated_row[25],
                "gd_xgd_away": formated_row[26],
                "xg_sh_away": formated_row[27],
                "xga_sh_away": formated_row[28],
                "xg90_away": formated_row[29],
                "xga90_away": formated_row[30],
                "xg90_plus_xga90_away": formated_row[31],
                "xg90_div_xga90_away": formated_row[32],
                "xg90_0_3_max_away": formated_row[33],
                "xga90_0_3_max_away": formated_row[34],
                "xg90_xga90_plus_0_3_max_away": formated_row[35],
                "xg90_xga90_div__0_3_max_away": formated_row[36],
                "xg90_index_away": formated_row[37],
                "xga90_index_away": formated_row[38],
                "xg90_no_index_away": formated_row[39],
                "xga90_no_index_away": formated_row[40],
                "xg90_xga90_plus_no_index_away": formated_row[41],
                "xg90_xga90_div_no_index_away": formated_row[42],
                "teams_num": formated_row[43],
                "url": formated_row[44]
            }

            # Debug lines
            import pprint
            pprint.pprint (params)

            # Send data to API
            try_request (api_url, params, send_data)

        # Close tab
        scraper.end_browser ()
        scraper.switch_to_tab (0) 
        
        # Pages debugs 
        logger.info ("\nData saved.")
        logger.info ("Matches: ")
        for match in saved_matches:
            logger.info (f"\t{match}")

        # requests continue prompt
        prompt = input ("\nContinue? ")
        if str(prompt).lower().strip() == "no":
            scraper.end_browser()
            break
        else:
            selector_next = ".next-matches-btn.next"
            classes_next = scraper.get_attrib (selector_next, "class")
            if "disable" in classes_next:
                logger.info ("No more matches. Program end.")
                scraper.end_browser()
                break
            else:
                scraper.click (selector_next)
                time.sleep (3)
                scraper.refresh_selenium ()



if __name__ == "__main__":
    main()