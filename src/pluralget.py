from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import logging
import json
import requests
import sys
import re
import undetected_chromedriver as uc

class Pluralget:
  def __init__(self, userName, password, course, language):
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get('https://app.pluralsight.com/id')
    self.login(driver, userName, password)
    driver.get(course)
    urlList, videoName = self.getAllVideos(driver)
    print(len(urlList), len(videoName))
    captions = self.getCaptions(driver, language)
    driver.quit()
    #Downloads video
    self.downloadList(urlList, videoName, ".mp4")
    #Downloads captions
    self.downloadList(captions, videoName, ".vtt")

  def login(self, driver, userName, password):
    userNameElement = driver.find_element_by_id('Username')
    self.sendText(userNameElement, userName)
  
    passwordElement = driver.find_element_by_id('Password')
    self.sendText(passwordElement, password)
    sleep(3)

  def sendText(self, element, value):
    element.send_keys(value + Keys.ENTER)
  
  def downloadList(self, urlList, videoName, ext):
    for i in range(0, len(urlList)):
      fileName = videoName[i] + ext 
      with open(fileName, 'wb') as f:
        print("Downloading " + fileName)
        response = requests.get(urlList[i], stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=100):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
        print("\n")

  def displayAllSections(self, driver):
    sections = "//div[@class='module-header u-flex u-align-items-center']"
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, sections)))
    
    # Displays all elements of the menu
    tableContentXpath = driver.find_elements_by_xpath(sections)
    for element in tableContentXpath:
      driver.execute_script("arguments[0].click();", element)
      #element.click()

  def getAllVideos(self, driver):
    self.displayAllSections(driver)
    urlList = []
    videoName = []
    items = '//button[contains(@class,"content-item u-flex u-align-items-stretch u-pr-lg u-mx-0")]'
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, items)))
    elementsXpath = driver.find_elements_by_xpath(items)
    index = 1
    for element in elementsXpath:
      element.click()
      videoTitle = re.sub('\W+',' ', element.text)
      # Gets all request of the site
      for request in driver.requests:
        if request.response:
          # Gets the request that contains the video link
          if request.url.find("viewclip") != -1:
            jsonViewclipFile = json.loads(request.response.body)
            #print(jsonViewclipFile)
            urlVideo = jsonViewclipFile["urls"][0]["url"]
            if urlList.count(urlVideo) == 0:
              print(str(index) + ". " + videoTitle)
              urlList.append(urlVideo)
              videoName.append(str(index) + ". " + videoTitle)
              index = index + 1
      sleep(5)
    return urlList, videoName

  # Gets captions of differents languages
  def getCaptions(self, driver, language):
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//script[@id='__NEXT_DATA__']")))
    elementsXpath = driver.find_element_by_xpath("//script[@id='__NEXT_DATA__']")
    jsonModules = json.loads(elementsXpath.get_attribute('innerHTML'))
    data = jsonModules["props"]["pageProps"]["tableOfContents"]["modules"]
    url = "https://app.pluralsight.com/transcript/api/v1/caption/webvtt/"
    captions = []
    for d in data:
      contenItem = d["contentItems"]
      for caption in contenItem:
        captionId = caption["id"]
        captionVersion = caption["version"]
        captions.append(url + captionId + "/" + captionVersion + "/" + language)
    return captions

course = "https://app.pluralsight.com/course-player?clipId=bd84852c-2e10-46d9-8338-8a13428af0cf"
language = "es"
userName = "mail@mail.com"
password = "myInsecurePassword"
plural = Pluralget(userName, password, course, language)
