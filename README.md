# G00gle D0rks script
Google Dorks Script is a script aimed for (semi)-automatic google dork search

## Requirements
* Having Python3 installed
* Having Selenium installed

## Setup
Please follow these steps prior to running the script:

* First, clone the repository:
```
git clone https://github.com/teneluce/g00gle_d0rk_script.git
cd g00gle_d0rk_script
```
* Then, create a Python virtual environment:
```
python3 -m venv .
source bin/activate
```
* Install Selenium: 
```pip3 install selenium```

* Modify the script to adapt it to your context (in fuction main)
* Modify the file all_dorks.txt to adapt it to your needs

## How to use it
* Launch the script with this command:
```python3 script.py```
A browser window will open. Let it proceed.

* At a moment, Google will ask you to solve a captcha (for obvious reasons). The script will then pause, waiting for you to solve the captcha. Once it is done, the script will resume. Note that captcha are most likely to appear more than once, depending on your queries amount (in all_dorks.txt)

* Once all queries have been searched, the script will let the browser window opened. If you want to close it and terminate the task, press Enter in the terminal.

* The results are in ./output/{target}_{timestamp}.txt

## Improvements
If you have suggestions to improve this tool, please contact me at tenebraslucem@proton.me

