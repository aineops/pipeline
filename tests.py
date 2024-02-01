import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

class SeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 3)
        self.fake = Faker()

    def test_selenium_actions(self):
        driver = self.driver
        wait = self.wait

        # Naviguer vers la page d'accueil de l'application
        driver.get("http://localhost:8080/")

        # Vérifier la présence de l'onglet 'Home' et naviguer dans l'application
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Home']")))
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='button']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='ownerNew']"))).click()

        # Remplir le formulaire avec des données aléatoires générées par Faker
        firstName = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='firstName']")))
        firstName.send_keys(self.fake.first_name())

        lastName = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='lastName']")))
        lastName.send_keys(self.fake.last_name())

        address = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='address']")))
        address.send_keys(self.fake.street_address())

        city = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='city']")))
        city.send_keys(self.fake.city())

        phoneNumber = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='905554443322']")))
        phoneNumber.send_keys(self.fake.numerify(text='############'))

        # Soumettre le formulaire et naviguer à travers l'application
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Owners']")))
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Veterinarians']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Veterinarians']")))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
