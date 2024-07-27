import time
from src.driver import Driver
from src.config import CONFIG as _
from src.result_page import ResultPage
from selenium.webdriver.common.keys import Keys

class SearchForm():
    def __init__(self, driver : Driver):
        driver.get(_.main_url)

        self.select_faculty   = None
        self.values_faculty   = None
        self.options_faculty  = None

        self.select_hug     =   None
        self.values_hug     =   None
        self.options_hug    =   None

        self.maslul_select     =   None
        self.values_maslul     =   None
        self.options_maslul    =   None

        self.details_radio  =   None
        self.search_button  =   None
        
        self.driver = driver

    def restart(self):
        self.driver.get(_.main_url)
        self.reset_fields(faculty=True, hug=True, maslul=True)

    def reset_fields(self, faculty=False, hug=False, maslul=False):
        if faculty:
            self.select_faculty = None
            self.values_faculty = None
            self.options_faculty = None

        if hug:
            self.select_hug = None
            self.values_hug = None
            self.options_hug = None

        if maslul:
            self.maslul_select = None
            self.values_maslul     =   None
            self.options_maslul    =   None


    def get_all_faculties(self,include_zeroes=False):
        if self.select_faculty is None:
            self.select_faculty = self.driver.find_x(_.x('search_form', 'faculty_input'))
        
        if self.options_faculty is None:
          self.options_faculty = self.driver.get_select_options(self.select_faculty)

          if not include_zeroes:
              self.options_faculty = [option for option in self.options_faculty if option.get_attribute('value') not in ['','0','00','000','0000','00000','000000']]
          
          self.values_faculty = {option.get_attribute('value') : option for option in self.options_faculty}
        return self.values_faculty
    
    def get_all_hugim(self,include_zeroes=False):
        if self.select_hug is None:
            self.select_hug = self.driver.find_x(_.x('search_form', 'hug_input'))
        
        if self.options_hug is None:
          self.options_hug = self.driver.get_select_options(self.select_hug)

        #   if not include_zeroes:
        #       self.options_hug = [option for option in self.options_hug if option.get_attribute('value') not in ['','0','00','000','0000','00000','000000']]
          
          self.values_hug = {option.get_attribute('value') : option for option in self.options_hug}
        return self.values_hug
    
    def get_all_maslulim(self,include_zeroes=False):
        if self.maslul_select is None:
            self.maslul_select = self.driver.find_x(_.x('search_form', 'maslul_input'))
        
        if self.options_maslul is None:
          self.options_maslul = self.driver.get_select_options(self.maslul_select)

          if not include_zeroes:
              self.options_maslul = [option for option in self.options_maslul if option.get_attribute('value') not in ['','0','00','000','0000','00000','000000']]
          
          self.values_maslul = {option.get_attribute('value') : option for option in self.options_maslul}
        return self.values_maslul

    def set_faculty(self, faculty_id:str) -> bool:
        if faculty_id not in self.values_faculty:
            return None
        
        self.driver.set_select_option(self.select_faculty,faculty_id)

        self.reset_fields(hug=True, maslul=True)

        self.get_all_hugim()

    def set_hug(self, hug_id:str) -> bool:
        if hug_id not in self.values_hug:
            return None
        
        self.driver.set_select_option(self.select_hug,hug_id)
        self.reset_fields(maslul=True)

        self.get_all_maslulim()

    def set_maslul(self, maslul_id:str) -> bool:
        if maslul_id not in self.values_maslul:
            return None
        if self.maslul_select is None:
            self.maslul_select = self.driver.find_x(_.x('search_form', 'maslul_input'))
        
        self.driver.set_select_option(self.maslul_select,maslul_id)

    def search(self):
        if self.details_radio is None:
            self.details_radio = self.driver.find_x(_.x('search_form', 'low_details_radiobox'))

        self.details_radio.click()
        
        if self.search_button is None:
            self.search_button = self.driver.find_x(_.x('search_form', 'search_button'))
        
        self.search_button.click()

        return ResultPage(self.driver)
    
