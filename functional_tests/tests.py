from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase



class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser=webdriver.Opera()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()




    def test_layout_and_styling(self):
        #Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1200, 768)
        time.sleep(5)
        #She notice the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x']+inputbox.size['width']/2,
                600-29.5,
                delta=5
                )





    def check_for_row_in_list_table(self, row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):


        #Edith has heard about a cool new online to-do app. She goes to check out its page
        self.browser.get(self.server_url)

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


    #She is ivited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                input_box.get_attribute('placeholder'),
                'Enter a to-do item'
                )
    #She types "Buy peacock feathers" into a text box (Edith's hobby is tring fly-fishing lurres)
        input_box.send_keys('Buy peacock feathers')

    #When she hits enter, the page updates, and now the page lists
    #"1: Buy peacock feathers" as an iem in to-do list

        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

    #There is still a text box inviting her to add another item. She enters
    #"Use feathers to make a fly" (Edith is very methadical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
            
    #The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        """    
        #Edith wonders whether the site will remember her list. Then she sees
        #that the site has generated o unique URL for her -- there is some 
        #explanatory text to that effect.
    
        #She visits that URL - her to-do list is still there.
    
        #Satisfied, she goes back to sleep
    
            self.fail('Finish the test!')
        """
        #Now a new user, Francis, comes along to the site.
    
        #We use a new browser session to make sure that no information
        ##of Edith's is coming through from cookies etc#
    
        self.browser.quit()
        self.browser = webdriver.Opera()
    
        #Francis visit the home page. Ther is no sign of Edith's list
    
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
    
        #Francis starts a new list by entering a new item. He
        #is less interesting than Edith...
    
        input_box=self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
    
    
        #Francis gets his own unique URL
    
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)


        #Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
    
        #Satisfied, thay both go back to sleep
