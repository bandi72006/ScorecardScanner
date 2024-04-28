from selenium import webdriver

driver = webdriver.Chrome()
url = "https://www.worldcubeassociation.org/competitions/DubaiOpen2024/registrations"

driver.get(url)

all_rows = driver.find_elements("xpath", '/html/body/main/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
data = []    # list of dictionaries with Author and Book Name

# As the first row is table head, we iterate from 1 to get the data.
for index in range(1, len(all_rows)):
    all_columns = all_rows[index].find_elements("xpath","./td")
    print(all_columns[0].text)
driver.quit()

