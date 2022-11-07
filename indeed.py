from selenium import webdriver 
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from argparse import PARSER
import requests, openpyxl
import csv
import os
import sys
from numpy import product
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import json 
import psycopg2
import pandas as pd
import io
from io import StringIO
from pandas import DataFrame
from time import sleep
import uuid
from io import StringIO
from flask import Flask, jsonify


uuid4 = uuid.uuid4()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

details_container = []


class Scraper:
    """Using webdriver to automate the webpage"""
    def __init__(self) -> None:
        options = FirefoxOptions()
        options.headless = True
        # self.opt.add_argument("--headless")
        # self.driver = webdriver.Chrome(service= Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.url = self.driver.get("https://uk.indeed.com/jobs?q=data%20engineer%20or%20data%20scientist&l=London%2C%20Greater%20London&vjk=f11971796d62ded9")
        self.driver.maximize_window()
        sleep(1)
  
        
    def navigate_page(self) -> None:
        """ This will accept all cookies """
        self.accept_cookies = self.driver.find_element(by=By.XPATH, value= "//button[@id='onetrust-accept-btn-handler']")
        self.accept_cookies.click()
        self.fourth_element = self.driver.find_element(by=By.XPATH, value="//td[@class='resultContent']")
        self.driver.find_elements(by=By.XPATH, value="//div[@id='mosaic-provider-jobcards']")
        sleep (2)
        self.data_scrape = []

        for i in range(25):
            
            # df = pd.DataFrame(i)
            # data_scrape = dict()
            sleep(3)
            
            details_containers_job_container= self.driver.find_elements(by=By.XPATH, value="//div[@class='slider_item css-kyg8or eu4oa1w0']")
            sleep(3)
            
            self.new_jobs = self.get_job_details(details_containers_job_container) 
             
            # print(self.data_scrape)
            i+=1
            sleep(3)
            self.data_scrape.append(self.new_jobs)  
            
            self.columns = ['Job_Link','Unique_ID', 'Title', 'Company_Name', 'Company_Location', 'Salary']
            self.data_scrape.append(self.df)
            self.data_scrape = [self.job_link,self.unique_id, self.title,  self.company_name,  self.company_location,  self.salary]
            pages = 3
            self.df_1 = pd.DataFrame(self.data_scrape, index=None)
            # self.df_1.transpose()
            # self.df_2 = pd.concat(self.df, self.df_1)
            
            self.df_1 =self.df_1.transpose()
            self.df_1.columns = self.columns
            
            # page+=1
            
            print(self.df_1)
            sleep(3)
            

            if os.path.exists('/home/cdp/Indeed_data_new.csv'):
                self.df_1.to_csv('/home/cdp/Indeed_data_new.csv',mode='a',header=True, index=False)
            else:
                self.df_1.to_csv('/home/cdp/Indeed_data_new.csv', mode='a',header=True, index=False)

            
            sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
           
            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//a[@aria-label='Next']").click()
            except:
                pass

            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//button[@class='icl-CloseButton icl-Card-close']").click()
            except:
                pass

            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//div[@id='popover-x']").click()
            except:
                pass
                
            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//div[@id='popover-x']").click()
            except:
                pass
            
            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//div[@id='popover-background']").click()
            except:
                pass
                     
            try:
                sleep(0.5)
                self.driver.find_element(by=By.XPATH, value="//a[@data-testid='pagination-page-next']").click()
            except:
                pass

    def data_store(self):
        dfs = []
        save_path = '/home/cdp/'
        if not os.path.exists(f'{save_path}/Indeed_jobs_Dataframe'):
                os.makedirs(f'{save_path}/Indeed_jobs_Dataframe')

        with open(f'{save_path}/Indeed_jobs_Dataframe/data_jobs_new.json', 'w+') as fp:
                json.dump(self.new_jobs, fp,  indent=4)
      

        if os.path.exists(f'{save_path}/Indeed_jobs_Dataframe/data_jobs_new.csv') and os.path.exists(f'{save_path}/Indeed_jobs_Dataframe/Indeed_jobs.json'):
            self.saving_data = True
            return self.saving_data, save_path

            
    def page_scroll(self) -> None:
        self.scrape()
        self.last_height = self.driver.execute_script('return document.body.scrollHeight')
        # sleep(3)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        # sleep(3)
        #new_height = driver.execute_script('return document.body.scrollHeight')
        #sleep(3)
        self.scroll_pause_time = 3
        i = 0
        self.number_of_scrolls = 3
        while i < self.number_of_scrolls:
            
            # print(self.df)
            # print(f"scrolled {i} time(s)")
            sleep(1)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)
            sleep(self.number_of_scrolls)
            
            self.new_height = self.driver.execute_script(
                        "return document.body.scrollHeight")
            if self.new_height == self.last_height:
                break
            i += 1
            self.last_height = self.new_height
            
        
        
    def scrape(self):
        """Assigning a new method to call another method"""
        # self.nevigate_page()
        # self.__get__job_details(self.job_containers)
        self.get_job_details(details_container)
              
    
    def get_job_details(self, details_container):
        """ Scraping all the details related to the job post"""
        
        list_of_all_jobs_details = []
        # details_container = []
        # global details_container
        new_unique_id = [] 
        # while True:
        self.job_link =[]
        self.unique_id = []
        self.title = []
        self.company_name =[]
        self.company_location =[]
        self.salary = []
        for job_listing in details_container:
            # global job_details_dictionary
            job_details_dictionary = dict()
            try:
                job_links = job_listing.find_element(by=By.XPATH, value=".//a").get_attribute('href')
                self.job_link.append(job_links)
            except NoSuchElementException:
                self.job_link.append('NaN')
                
            try:
                job_id = job_listing.find_element(by=By.XPATH, value=".//a").get_attribute('id')
                self.unique_id.append(job_id)
            except NoSuchElementException:
                self.unique_id.append('NaN')
            # job_details_dictionary["Title"] = job_listing.find_element(by=By.XPATH, value=".//h2").text
            try:
                job_titile = job_listing.find_element(by=By.XPATH, value="//a[@class='jcs-JobTitle css-jspxzf eu4oa1w0']").text
                self.title.append(job_titile)
            except NoSuchElementException:
                self.title.append('NaN')
            try:
                job_company = job_listing.find_element(by=By.XPATH, value=".//div/span[@class='companyName']").text
                self.company_name.append(job_company)
            except NoSuchElementException:
                self.company_name.append('NaN')
            try:
                job_location = job_listing.find_element(by=By.XPATH, value=".//div[@class='companyLocation']").text
                self.company_location.append(job_location)
            except NoSuchElementException:
                self.company_location.append('NaN')
            try:
                job_salary = job_listing.find_element(by=By.XPATH, value= ".//div[@class='metadata salary-snippet-container']").get_attribute('textContent')
                self.salary.append(job_salary)
            except NoSuchElementException:
                self.salary.append('NaN')
  
            self.df =pd.DataFrame ({'Job_Link':self.job_link,'Unique_ID': self.unique_id, 'Title': self.title, 'Company_Name': self.company_name, 'Company_Location': self.company_location, 'Salary': self.salary})
           

            
    def scraper_main(self) -> None:
        self.navigate_page()
        self.page_scroll()
        self.data_store()
        # self.download_image()
        # self.connect_to_db()
        self.aws_upload()
        self.driver.quit()
        
if __name__ == "__main__":
    DPS = Scraper()
    DPS.scraper_main()


        
