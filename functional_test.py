from selenium import webdriver


browser=webdriver.Opera()
browser.get('http://localhost:8585')

assert 'Django' in browser.title
