from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utility_methods.utility_methods import *

import urllib.request
import os
import time


class InstagramBot:

    def __init__(self, username=None, password=None):
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

        self.driver = webdriver.Chrome(config['ENV']['CHROMEDRIVER_PATH'])

        self.logged_in = False

    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)

        # login button xpath changes after text is entered, find first
        login_btn = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]')

        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.click()

    @insta_method
    def search_tag(self, tag):
        """
        navigatees to a search for posts with a speicific tag on Insta

        """
        self.driver.get(self.get_tag_url.format(tag))

    @insta_method
    def nav_user(self, user):
        self.driver.get(self.nav_user_url.fromat(user))

    def follow_user(self, user):
        self.nav_user(user)

        follow_buttons = self.find_buttons('Follow')

        for button in follow_buttons:
            button.click()

    @insta_method
    def unfollow_user(self, user):
        self.nav_user(user)

        unfollow_buttons = self.find_buttons('Following')

        if unfollow_buttons:
            for button in unfollow_buttons:
                button.click()
                unfollow_confirmation = self.find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.').format('Following)')

    @insta_method
    def user_img_downloader(self, user):
        self.nav_user(user)

        img_sources = []
        downloaded = False
        while not downloaded:
            finished = self.infinite_scroll()

            img_sources.extend([img.get_attribute(
                'src') for img in self.driver.find_elements_by_class_name('FFVAD')])

            # this will clean up duplicates
        img_sources = list(set(img_sources))

        for idx, src in enumerate(img_sources):
            self.img_downloader(src, idx, user)

    @insta_method
    def auto_like_latest_posts(self, user, n_posts, like=True):
        action = 'Like' if like else 'Unlike'
        self.nav_user(user)

        images = []
        images.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in images[:n_posts]:
            img.click()
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath(
                    "//*[@aria-label='{}']".format(action)).click()

            except Exception as e:
                print(e)

            self.driver.find_elements_by_class_name('ckWGn')[0].click()

    """
        maximum likes aroud 15
        and unlikes the post if u have already liked it.
    """

    def img_downloader(self, source, img_filename, folder):

        folder_path = './{}.format(folder)'

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(img_filename)
        urllib.request.urlretrive(
            source, '{}/{}'.format(folder, img_filename))

    def infinite_scroll(self):
        SCROLL_PAUSE_TIME = 1
        self.last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight")

        time.sleep(SCROLL_PAUSE_TIME)
        self.new_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False

    def find_buttons(self, button_text):
        """
        find buttons for following and un following of user
        """
        buttons = self.driver.find_elements_by_xpath(
            "//*[text()='{}'".format(button_text))

        return buttons


if __name__ == '__main__':
    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstagramBot()
    bot.login()

    bot.auto_like_latest_posts('iabhi1610', 2, like=True)
