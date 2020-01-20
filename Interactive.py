
from pyppeteer import launch
import os
import sys
import asyncio
from env import creds

pages = []
project_Locations = []

# Launch a new headed brower
async def head_browser():
    return await launch({"headless": False})

# Launch a new headless brower
async def headless_browser():
    return await launch({"headless": True})

# Create a new page and load argument url
async def new_page(browser, url):
    page = await browser.newPage()
    return await page.goto(url)

#Query url than load on current page
async def goto_url(browser, page, url):
    return await page.goto(url)

# Focus page tab by index
async def use_index_page(browser, index):
    pages = browser.pages
    return pages[index]

# Focus page tab by name
async def use_name_page(name):
    # not sure if this is nessisary anymore. Are able to name.goto() etc
    return name

# Give current page a name
async def set_name_page(page, name):
    #pagewithname.index =index(name) or something
    # Needs method of keeping together. and being able to move tabs around while retaining name match
    return page

# Closes current page
async def close_page(page):
    return await page.close()

# basically page.setviewport() with defaults for my sites
async def set_size_page(page):
    set

# Save a screenshot of current page saved at '_screenshot_path'
async def screenshot_page(page):
    return page

# Make a copy of the current page
async def split_page(browser, page):
    page2 = await browser.newPage()
    await page2.goto_url(page.url)
    return page2

# Save current session of tabs
async def save_session(browser, session_id):
    # print(browser.pages, 'session_id.tabs')
    pass

# Load current session of tabs
async def load_session(browser, session_id):
    # data = data from file
    # if data.head:
        # session = head_browser()
    # else:
        # session = headless_browser()
    # for page in data.pagelist:
        # pagelist.append(await session.newPage())
    # return pagelist
    pass

# Tools for site logins
class Logins():
    def __init__(self, user, password, project):
      self.page = page
      self.user = user
      self.password = password
      self.project = project

    # Create new page and log into Amp
    async def login_amp(self):
        # self.page.goto(project+ampurlsuffix)
        pass

    # Create new page and log into qv
    async def login_qv(self):
        pass

    # Create new page and log into Certify
    async def login_certify(self):
        pass

    # Create new page and log into Keller
    async def login_keller(self):
        pass

    # Create new page and log into Vortex
    async def login_vortex(self):
        pass

    # Create new page and log into Gmail
    async def login_gmail(self):
        pass

class Alarm_Investior():
    def __init__(self, page, axis, tiemstamp):
      self.page = page
      self.axis = axis
      self.timestamp = timestamp

    def launch(self):
        self.page = await Logins.login_amp(creds.user, creds.password, page,'captiolcomplex')


    def Open_plot_spread(self):
        pass

    def Open_plot_axis(self, axis):
        pass

    def Open_values(self):
        pass

    def Open_value_axis(self, axis):
        pass

    def Open_archive(self)

class dailys():
    def __init__(self, page):
        self.page = page

    async def weather_update(self):
          #scrape various weather data
        for location in project_Locations:
            self.page.goto(location.url)

class tool():
    def __init__(self, browser, page, data):
        self.page = page
        self.browser = browser
        self.data = data

    def save_note(self):
        # print('data: ' + self.data + 'page: ' + self.page, '/output/Notes.txt')
        pass

class qv_tool():
    def __init__(self, browser, page, data, project):
        self.browser = browser
        self.page = page
        self.data = data
        self.project = project


    # Change Quickviews Current View
    async def goto_view(self, view):
        pass

    # Navigate to pdf reports page
    async def goto_reports(self):
        pass

    # Navigate to data sources page
    async def goto_datasource(self):
        pass

    # Navigate to log book journal
    async def goto_journal(self):
        pass

    # scrape whatever is avaible from current job site
    async def scrape_site(self):
        pass

    # scrape whatever is avaible from current page
    async def scrape_page(self):
        pass


# Preset options for running data through image magick
class mkgif():
    def __init__(self, page, data, sensor_info):
        self.page = page
        self.data = data
        self.sensor_id = sensor_info[0]
        self.sensor_type = sensor_info[1]
        self.sensor_daterange = sensor_info[2]

    # Open new gif after rendering
    def show_file_when_done(self):
        pass

    # Render gathered Images as gif
    def render(self):
        pass

    # set gif speed
    def set_speed(self):
        pass

    # set gif loop value
    def set_loop(self):
        pass

    # This will assist with gathering screenshots of SAA data for gif creation
    async def take_incremental_screenshot(self):
        # mkdir screenshotfolder
        # query
        # open up target sensor
        # screenshot
        # align_next_day
        #
        # screenshotfolder/screenshot, move date back day/week, repeat.
        pass

    # navigate to target sensors first requested date
    def align_first_day(self):
        # select target sensor
        # open plot
        # Navigate to start date
        # Begin screenshot, next day loop
        pass

    # navigate to target sensors next requested date
    def align_next_day(self):
        # Navigate plot to next date
        pass

    # Delete temporary files created while assembling gif
    async def clean_up(self):
        # Search and Del variables available from pyppeteers doc
        # archive screenshots and delete mkgif working directorys
        pass


