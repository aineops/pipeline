from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time

# Création d'une instance de Faker
fake = Faker()

# Démarrer une nouvelle session de navigateur Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Naviguer vers la page d'accueil de l'application
driver.get("http://localhost:8080/") # Remplacez par l'URL réelle

# Initialiser l'objet WebDriverWait
wait = WebDriverWait(driver, 3)

# Vérifier la présence de l'onglet 'Home' et naviguer dans l'application
wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Home']")))
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='button']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='ownerNew']"))).click()

# Remplir le formulaire avec des données aléatoires générées par Faker
firstName = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='firstName']")))
firstName.send_keys(fake.first_name())

lastName = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='lastName']")))
lastName.send_keys(fake.last_name())

address = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='address']")))
address.send_keys(fake.street_address())

city = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='city']")))
city.send_keys(fake.city())

phoneNumber = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='905554443322']")))
phoneNumber.send_keys(fake.numerify(text='############'))

# Soumettre le formulaire et naviguer à travers l'application
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Owners']")))
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Veterinarians']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Veterinarians']")))

# Fermeture du navigateur
driver.quit()

