from selenium.webdriver.common.by import By
from whatsTrending.proxy import proxyChrome, chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, url_contains, presence_of_all_elements_located
from .models import Auth
import os

def getProxyDriver():
	return proxyChrome(os.environ.get("PROXY_HOST"), int(os.environ.get("PROXY_PORT")))

def getDriver():
	return chrome()

def getReAuthenticatedDriver(useProxy):
	driver = {}

	if useProxy:
		driver = getProxyDriver()
	else:
		driver = getDriver()

	driver.get("http://x.com/login")

	# Get Username Input
	input = WebDriverWait(driver, 20).until(presence_of_element_located([By.CSS_SELECTOR, 'input[type="text"]']))
	input.send_keys(os.environ.get('X_USER'))
	submitUsername = driver.find_element(By.XPATH, "//button[contains(.//text(), 'Next')]")
	submitUsername.click()

	# Get Password Input
	passwordInput = WebDriverWait(driver, 20).until(presence_of_element_located([By.CSS_SELECTOR, 'input[type="password"]']))
	passwordInput.send_keys(os.environ.get('X_PASS'))
	loginBtn = driver.find_element(By.XPATH, "//button[contains(.//text(), 'Log')]")
	loginBtn.click()

	# Wait until authentication completes	
	WebDriverWait(driver, 20).until(url_contains('home'))

	return driver

def createAuthCookie(cookie):
	return Auth(cookie=cookie).save()

def updateAuthCookie(newCookie, cookieObj):
	cookieObj.cookie = newCookie
	cookieObj.save()

def getAuthenticatedWindow(useProxy):
	cookies = Auth.objects.all()

	if cookies.count() == 0:
		driver = getReAuthenticatedDriver(useProxy)
		createAuthCookie(cookie=driver.get_cookie('auth_token'))
		return driver
	
	cookie = cookies[0].cookie

	driver = {}
	
	if useProxy:
		driver = getProxyDriver()
	else:
		driver = getDriver()

	driver.get("http://x.com")

	driver.add_cookie(cookie)

	# Go to the Home path to refresh and enable authentication
	driver.get("http://x.com/home")

	# If the cookie is invalid
	# user will be redirected to login path
	if "login" in driver.current_url:
		driver = getReAuthenticatedDriver()
		updateAuthCookie(newCookie=driver.get_cookie('auth_token'), cookieObj=cookies[0])
		return driver
	
	return driver

def getIP(driver):
	driver.get('http://api.ipify.org')
	return driver.find_element(By.TAG_NAME, 'body').text


def getTrendingData(useProxy):
	driver = getAuthenticatedWindow(useProxy)

	trendingEls = WebDriverWait(driver, 20).until(presence_of_all_elements_located([By.XPATH, '//div[contains(@aria-label, "Trending now")]//div[@tabindex="0"]//div[contains(@style, "color: rgb(231, 233, 234)")]']))	

	topics = []

	for el in trendingEls:
		topics.append(el.text)

	ip = getIP(driver)

	data = {
		"topics": topics,
		"ip": ip
	}
	
	return data
