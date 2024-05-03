from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml

def editYAMLFile(key, value):
    with open("config.yaml") as file:
        configFile = yaml.safe_load(file)

    for data in configFile:
        if data == key:
            configFile[key] = value


    with open("config.yaml", "w") as f:
        yaml.dump(configFile, f)


def editCompLink(url):
    url += "/registrations" #Specifically to competitor page
    chrome_options = Options()

    chrome_options.add_argument("--headless=new") 

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    all_rows = driver.find_elements("xpath", '//*[@id="competition-data"]/div/div[1]/div[2]/div[2]/table/tbody/tr')

    competitors = []
    for index in range(1, len(all_rows)):
        all_columns = all_rows[index].find_elements("xpath","./td")
        competitors.append(all_columns[0].text)

    editYAMLFile("compLink", url[:-14]) #String splicing gets rid of "/registration page"
    driver.quit()

    editYAMLFile("competitorList", competitors)

def editCompName(compName):
    editYAMLFile("compName", compName)

def editCompEvents(eventsDict):
    editYAMLFile("eventsList", eventsDict)

def getCompetitors():
    with open("config.yaml") as file:
        configFile = yaml.safe_load(file)

    return configFile["competitorList"]

