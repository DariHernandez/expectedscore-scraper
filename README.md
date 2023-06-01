<div><a href='https://github.com/github.com/darideveloper/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/github.com/darideveloper.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/expectedscore-scraper/blob/master/logo.png?raw=true' alt='Expectedscore Scraper' height='80px'/>

# Expectedscore Scraper

Extract data from page [expectedscore.com](https://expectedscore.com/) and save it in a Excel file. The program needs login to display the information.

Start date: **2021-12-15**

Last update: **2023-04-12**

Project type: **client's project**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://requests.readthedocs.io/en/latest/' target='_blank'> <img src='https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png' alt='Requests' title='Requests' height='50px'/> </a><a href='https://www.microsoft.com/es-mx/microsoft-365/excel/?rtc=1' target='_blank'> <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/2203px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png' alt='Excel' title='Excel' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a></div>

# Details

## Workflow

1. Login in the page
2. Get the last matches with pagination (12 at time)
3. Get data from matches (statistics from home and away teams)
4. Format data
5. Save the information in Excel
6. request to the user if want to continue with the next 12 matches, or stop the program. 

## Output data

The web scraping information will be saved in the file **output.xlsx**, in the sheet **data**.
Each time you run the program, the information will be overwritten.

**Note:** while running the program, DON'T OPEN the excel file.

# Install

## Install third party modules


``` bash
$ pip install -r requirements.txt
```

## Programs

For run the project, the following programs should be installed:

* [Google Chrome](https://www.google.com/intl/es/chrome) last version

# Settings

## config.json

All settings are in the config.json file. Create it with the following strucure:

```json
{
    "user": "email@gmail.com",
    "password": "mypass"
}
```

### user

User to  login in the page [expectedscore.com](https://expectedscore.com/)

### password

Password to login in the page [expectedscore.com](https://expectedscore.com/)

# Run

Run the __main__.py file or the project folder with your python 3.9 interpreter


