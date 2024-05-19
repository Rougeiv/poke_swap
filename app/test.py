from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import unittest
import multiprocessing
from app import create_app, db
from config import TestConfig
from app.models import User

# Get the directory of the current script
script_dir = os.path.dirname(__file__)
# Construct the path to the Edge WebDriver executable
edge_driver_path = os.path.join(script_dir, 'msedgedriver.exe')

# Setup the WebDriver
try:
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service)

    try:
        # Open the website
        driver.get("http://127.0.0.1:5000")

        # Maximize the window
        driver.maximize_window()

        # Add a sleep to ensure the page loads completely (if necessary)
        sleep(5)


        element = driver.find_element(By.XPATH, "/html/body/nav/div/ul/li[5]/a")
        element.click()

        # Wait for the username input element and enter the username
        username_element = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/form/p[1]/input")
        username_element.send_keys("Mythicrif")
        
        # Sleep for 2 seconds
        sleep(2)

        # Wait for the password input element and enter the password
        password_element = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/form/p[2]/input")
        password_element.send_keys("SuperCoolPassword!!")
        
        # Sleep for 2 seconds
        sleep(2)

        # Wait for the submit button and click it
        submit_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/form/input[2]")
        submit_button.click()

        sleep (5)

        catch_pokemon_link = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/a")
        catch_pokemon_link.click()

        sleep(4)

        catch_1_pokemon = driver.find_element(By.XPATH,"/html/body/div/div/button[1]")
        catch_1_pokemon.click()

        sleep(5)

        catch_10_pokemon = driver.find_element(By.XPATH,"/html/body/div/div/button[2]")
        catch_10_pokemon.click()

        sleep(8)
        back_to_main = driver.find_element(By.XPATH,"/html/body/nav/a")
        back_to_main.click()

        sleep(4)

        trade_offer_link = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[2]/div/div/a")
        trade_offer_link.click()

        sleep(4)

        select_offer = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/div[1]/button")
        select_offer.click()

        sleep(2)
        select_first_offer = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div[2]/div/div[1]/img")
        select_first_offer.click()
        sleep(2)

        select_request = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/div[3]/button")
        select_request.click()

        sleep(2)
        select_first_request = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div[2]/div/div[1]/img")
        select_first_request.click()

        sleep(2)
        post_trade = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[2]/div/button")
        post_trade.click()


        sleep(5)
        closer_success = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div/div[3]/button")
        closer_success.click()

        sleep(5)
        
        back_to_main = driver.find_element(By.XPATH,"/html/body/nav/a")
        back_to_main.click()
        sleep(4)

        click_first_trade = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/a[1]/div/div/h5")
        click_first_trade.click()


        sleep(4)
        accept_trade = driver.find_element(By.XPATH,"/html/body/div/div[1]/button")
        accept_trade.click()

        sleep(4)

        back_to_main = driver.find_element(By.XPATH,"/html/body/nav/a")
        back_to_main.click()

        sleep(4)
    finally:
        # Close the WebDriver
        driver.quit()

except Exception as e:
    print(f"An error occurred: {e}")
    raise
