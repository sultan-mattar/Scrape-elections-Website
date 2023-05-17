from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd
# Create an empty list to hold the data
data = []
executable_path = 'msedgedriver.exe'
df = pd.read_excel('C:/Users/Sulta/dataset.xlsx')

def scraper():
    driver = webdriver.Edge(executable_path)
    # navigate to the elections page
    driver.get("https://www.elections.il.gov/CampaignDisclosure/CandidateSearch.aspx")
    driver.maximize_window()
    time.sleep(2)
    # enter login details and submit the form
    menu = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddlParty'))
    menu.select_by_visible_text('Democratic')
    login_button =  driver.find_element(By.ID, "ContentPlaceHolder1_btnSubmit")
    login_button.click()
    print('Search Successfully!')
    time.sleep(5)

    #---------------------------------------------------------------------------------------------

    # Select The Page Size
    menuSize = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_gvCandidates_pnlLeft_phPagerTemplate_gvCandidates_PageSize'))
    menuSize.select_by_visible_text('All')
    time.sleep(20)

    print('The NOW! Ready')

    Candidate_Name = driver.find_elements(By.XPATH,'//tbody/tr/td[1]/a')
    Candidate_Name_url = driver.find_elements(By.XPATH,'//tbody/tr/td[1]/a')
    Address = driver.find_elements(By.XPATH,'//tbody/tr/td[2]')
    District_Type = driver.find_elements(By.XPATH,'//tbody/tr/td[4]')
    Office = driver.find_elements(By.XPATH,'//tbody/tr/td[5]')
    District = driver.find_elements(By.XPATH,'//tbody/tr/td[6]')

    print('loop')
    
    for i in range(len(Candidate_Name)):
        temporary_data ={
                   'Candidate_Name': Candidate_Name[i].text,
                   'Address': Address[i].text,
                   'District_Type': District_Type[i].text,
                   'Office': Office[i].text,
                   'District':District[i].text,
                   'URL': Candidate_Name_url[i].get_attribute('href')
                   }
        data.append(temporary_data)
        
    
    column_list = df['URL'].tolist()
    print(len(column_list))

    print("loop")
    for i in range(len(column_list)):  # 8941
        try:
            driver.get(column_list[i])
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//tbody/tr/td[1]/a'))).click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if EC.visibility_of_element_located((By.LINK_TEXT, 'Last'))(driver):
                last_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Last')))
                last_element.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                PDF_File = driver.find_element(By.XPATH, '//tbody/tr/td[1]/a') and driver.find_element(By.LINK_TEXT, value='D-1 Statement of Organization')
                PDF_File.click()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                PDF_URL = driver.current_url
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                # Proceed with your code if the element is visible
                print("Element 'Last' is visible.")
            else:
                # Handle the condition when the element is not visible
                print("Element 'Last' is not visible.")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                PDF_File = driver.find_elements(By.XPATH, '//tbody/tr/td[1]/a') and driver.find_element(By.LINK_TEXT, value='D-1 Statement of Organization')
                PDF_File.click()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                PDF_URL = driver.current_url
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except NoSuchElementException:
            PDF_URL = "NO PDF File"
        temporary_data = {'PDF_File': PDF_URL}
        data.append(temporary_data)

    df_data = pd.DataFrame(data)
    df_data.to_excel('data.xlsx', index=False)
    print("The PDF link has been downloaded")
    driver.quit()
  

scraper()




