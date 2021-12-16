import os
import time
from config import Config
from logs import logger
from tqdm import tqdm
from spreadsheet_manager.xlsx import SS_manager
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
        logger.info (f"\nCurrent page: {current_page}")

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
        
        # Matches loop
        # for link in tqdm(links_matches): 
        page_data = []
        for link in links_matches: 

            # Open match in second tab
            scraper.set_page (link)
            time.sleep (3)

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

                # Columns loop
                selector_columns = f"{selector_team} > div.cell"
                columns_elem = scraper.get_elems (selector_columns)
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

            page_data.append (match_data)

        # data matches loop
        formated_data = []
        for match_data in page_data:

            # Format data to write in spreadsheet
            formated_row = []
            match_name = f"{match_data[0][1]} - {match_data[1][1]}"
            formated_row.append (match_name)
            for team_data in match_data:

                # Get data
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

            formated_data.append (formated_row)

        # Save data in spreasheet
        file_path = os.path.join (os.path.dirname (__file__), "output.xlsx")
        ss = SS_manager(file_path)
        ss.set_sheet ("data")
        ss.write_data (formated_data, start_row=2)
        ss.save()
        print ("Done")






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