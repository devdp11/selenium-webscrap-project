from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

# Initialize the webdriver service
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://m.imdb.com/chart/moviemeter/")
driver.maximize_window()

time.sleep(3)  # Wait for the page to load completely

movies = driver.find_elements(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')

for index in range(len(movies)):
    movies = driver.find_elements(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')
    movie_link = movies[index]
    
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", movie_link)
        driver.execute_script("arguments[0].click();", movie_link)
        
        time.sleep(1)
        print(f"Success on: open movie {index + 1}")
        
        try:
            user_reviews_span = driver.find_element(By.CSS_SELECTOR, 'span.three-Elements > span.score')
            driver.execute_script("arguments[0].scrollIntoView(true);", user_reviews_span)
            user_reviews_span.click()
            
            time.sleep(1)
            print(f"Success on: user reviews for movie {index + 1}")

            try:
                user_reviews_texts = driver.find_elements(By.CSS_SELECTOR, 'li.ipl-content-list__item')
                for user_review in user_reviews_texts:
                    try:
                        time.sleep(1)
                        user_name = user_review.find_element(By.CSS_SELECTOR, 'a.display-name-link')
                        comment_date = user_review.find_element(By.CSS_SELECTOR, 'span.review-date')
                        
                        comment_text_element = user_review.find_element(By.CSS_SELECTOR, 'div.text')
                        comment_text = comment_text_element.text
                        comment_text = comment_text.split('.')[0] if isinstance(comment_text, str) else comment_text
                        comment_text = comment_text.split('!')[0] if isinstance(comment_text, str) else comment_text
                        comment_text = comment_text.split('\n')[0] if isinstance(comment_text, str) else comment_text
                        
                        if comment_text.strip():
                            print(f"User comment by: {user_name.text}")
                            print(f"Comment date: {comment_date.text}")
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
