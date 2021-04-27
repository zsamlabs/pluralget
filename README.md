# PluralGet

## Requirements

* Python 3
* Selenium driver

## Installation

pip3 install -r requirements.txt

## Steps

Download driver  
Firefox https://github.com/mozilla/geckodriver/releases  
Chrome https://chromedriver.chromium.org/

Extract the content in **drivers/linux** or **drivers/windows**
and change the driver name 
line **15** of the file 
~~~
src/pluralget.py
~~~
After change the lines **109**, and **110** by course URL and the caption code
es = Spanish
en = English

~~~
course = "https://app.pluralsight.com/course-player?clipId=47ae435f-738e-48ca-87d1-7ed9eabfef32"
language = "es"
~~~

# Execution
python3.9 src/pluralget.py  

Start google-chrome in mode **debug**, it's very important because the site verify the activity of the navigator
~~~
google-chrome --remote-debugging-port=9222
~~~
Login with the valid credentials in the site

# Example

