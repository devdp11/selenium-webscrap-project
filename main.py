from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://m.imdb.com/chart/moviemeter/")
driver.maximize_window()

movies = driver.find_elements(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')

for index in range(len(movies)):
    movies = driver.find_elements(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')
    movie_link = movies[index]
    
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", movie_link)
        driver.execute_script("arguments[0].click();", movie_link)
        
        print(f"Succe on: open movie {index + 1}")
        
        try:
            user_reviews_span = driver.find_element(By.CSS_SELECTOR, 'span.three-Elements > span.score')
            driver.execute_script("arguments[0].scrollIntoView(true);", user_reviews_span)
            user_reviews_span.click()
            
            print(f"Succe on: user reviews for movie {index + 1}")
            driver.back()
        except Exception as e:
            print(f"Error on: user reviews for movie {index + 1}: {e}")

        driver.back()
    except Exception as e:
        print(f"Error on: open movie {index + 1}: {e}")
        driver.back()

driver.quit()