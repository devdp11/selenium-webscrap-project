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
        
        movie_name = driver.find_element(By.CSS_SELECTOR, 'span.hero__primary-text')
        print(f"Success on: open movie {movie_name.text}")
        
        try:
            user_reviews_span = driver.find_element(By.CSS_SELECTOR, 'span.three-Elements > span.score')
            driver.execute_script("arguments[0].scrollIntoView(true);", user_reviews_span)
            user_reviews_span.click()
            
            print(f"Success on: user reviews for movie {movie_name.text}")

            try:
                user_reviews_texts = driver.find_elements(By.CSS_SELECTOR, 'li.ipl-content-list__item')
                for user_review in user_reviews_texts:
                    try:
                        user_name = user_review.find_element(By.CSS_SELECTOR, 'a.display-name-link')
                        print(f"User comment by: {user_name.text}")
                        
                        comment_text_element = user_review.find_element(By.CSS_SELECTOR, 'div.text')
                        comment_text = comment_text_element.text
                        comment_text = comment_text.split('.')[0] if isinstance(comment_text, str) else comment_text
                        comment_text = comment_text.split('!')[0] if isinstance(comment_text, str) else comment_text
                        comment_text = comment_text.split('\n')[0] if isinstance(comment_text, str) else comment_text
                        
                        if comment_text.strip():
                            print(f"Comment text: {comment_text}")
                    except Exception as e:
                        print(f"Error retrieving user name or comment text for movie {index + 1}: {e}")

                driver.back()
            except Exception as e:
                print(f"Error on: user comments for movie {index + 1}: {e}")

        except Exception as e:
            print(f"Error on: user reviews for movie {index + 1}: {e}")

        driver.back()
    except Exception as e:
        print(f"Error on: open movie {index + 1}: {e}")
        driver.back()

driver.quit()
