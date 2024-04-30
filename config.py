from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    print(competitors)
    driver.quit()

