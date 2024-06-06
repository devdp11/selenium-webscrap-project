from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://thefork.pt")
driver.maximize_window()

locations = ["Braga", "Ponte de Lima", "Viana do Castelo", "Porto", "Amares"]