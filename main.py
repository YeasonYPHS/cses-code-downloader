from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
import os
import time 
import getpass


USERNAME = str(input("Input user name:"))
PASSWORD = str(getpass.getpass("Input password:"))

driver = webdriver.Chrome()
driver.get('https://cses.fi/login')

#time.sleep(2)

username = driver.find_element(By.ID, "nick")
password = driver.find_element(By.NAME, "pass")
login_button = driver.find_element(By.XPATH, "//input[@value=\"Submit\"]")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)
login_button.click()

time.sleep(2)

if(driver.execute_script("return window.location.href") == "https://cses.fi/login"):
    print("Incorrect username or password")
    driver.quit()
    exit()

driver.get('https://cses.fi/problemset/')

problem_list = driver.find_elements(By.CLASS_NAME, "task")

curr_directory = os.getcwd()

def save_code(link):
    driver.switch_to.new_window()
    driver.get(link)

    #code_block = driver.find_element(By.CLASS_NAME, "prettyprinted")
    code = driver.execute_script("return document.getElementsByClassName(\"linenums\")[0].innerText")
    title = driver.find_element(By.TAG_NAME, "h1").get_attribute("innerText")

    title = title.replace(" ", "-")
    f = open(title+".cpp", "w")
    f.write(code)
    f.close()

    driver.close()
    driver.switch_to.window(driver.window_handles[1])

def get_code(link):
    driver.switch_to.new_window()

    link = link.replace("task", "view")

    driver.get(link)

    #print(driver.find_element(By.TAG_NAME, "title").get_attribute("innerText"))
    code_list = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for item in code_list :
        if item.find_element(By.CLASS_NAME, "task-score").get_attribute("class").find("full") != -1:
            save_code(item.find_element(By.CLASS_NAME, "details-link").get_attribute("href"))
            break


    driver.close()
    driver.switch_to.window(driver.window_handles[0])

for problem in problem_list:
    """
    try:
        foo = problem.find_element(By.CLASS_NAME, "task-score icon full")
        valid = 1
    except:
        valid = 0
    
    if valid == 0:
        print(valid)
        continue
    """
    if problem.find_element(By.CLASS_NAME, "task-score").get_attribute("class").find("full") == -1:
        continue

    link = str(problem.find_element(By.TAG_NAME, "a").get_attribute("href"))
    #print(link)
    get_code(link)
    #time.sleep(2)
    #driver.get('https://cses.fi/problemset/')



time.sleep(10)
