import csv
import uuid
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://m.imdb.com/chart/moviemeter/")
driver.maximize_window()

time.sleep(5)

with open('./assets/data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["uuid", "movie_name", "movie_date", "movie_rating", "movie_genre", "comment_user", "comment_date", "comment_text"])

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
                movie_name = driver.find_element(By.CSS_SELECTOR, 'span.hero__primary-text').text
                date_elements = driver.find_elements(By.CSS_SELECTOR, 'a.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color')
                movie_date = None

                for date_element in date_elements:
                    date_text = date_element.text
                    if date_text.isdigit():
                        movie_date = date_text
                        break

                if not movie_date:
                    print(f"No valid date found for movie {index + 1}: {movie_name}")
                    driver.back()
                    continue

                try:
                    movie_rating_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="hero-rating-bar__aggregate-rating__score"] span.sc-bde20123-1.cMEQkK'))
                    )
                    movie_rating = movie_rating_element.text
                except Exception as e:
                    print(f"Rating not found for movie {index + 1}: {movie_name}")
                    movie_rating = "N/A"

                genre_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ipc-chip-list__scroller a.ipc-chip span.ipc-chip__text')
                genres = "; ".join([genre.text for genre in genre_elements])

                print(f"Movie name: {movie_name}")
                print(f"Movie date: {movie_date}")
                print(f"Movie rating: {movie_rating}")
                print(f"Movie genres: {genres}")

                try:
                    user_reviews_span = driver.find_element(By.CSS_SELECTOR, 'span.three-Elements > span.score')
                except Exception as e:
                    print(f"User reviews span not found for movie {index + 1}: {movie_name}")
                    driver.back()
                    continue

                driver.execute_script("arguments[0].scrollIntoView(true);", user_reviews_span)
                user_reviews_span.click()
                
                time.sleep(2)
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
                                
                                writer.writerow([str(uuid.uuid4()), movie_name, movie_date, movie_rating, genres, user_name.text, comment_date.text, comment_text])

                        except Exception as e:
                            print(f"Error retrieving user name or comment text for movie {index + 1}: {e}")

                    driver.back()
                except Exception as e:
                    print(f"Error on: user comments for movie {index + 1}: {e}")

            except Exception as e:
                print(f"Error on: movie details for movie {index + 1}: {e}")

            driver.back()
        except Exception as e:
            print(f"Error on: open movie {index + 1}: {e}")
            driver.back()

driver.quit()