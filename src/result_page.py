from src.driver import Driver
from src.config import CONFIG as _
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import re

EXAM_DATA_TABLE = _.x('results_page', 'course_entry', 'exam_data_container')
EXAM_DATA_ROW = EXAM_DATA_TABLE + _.x('results_page', 'course_entry', 'exam_table_semester_b_row')
EXAM_DATA_ROW_DATE = EXAM_DATA_ROW + _.x('results_page', 'course_entry', 'exam_table_row_date')
EXAM_DATA_ROW_TIME = EXAM_DATA_ROW + _.x('results_page', 'course_entry', 'exam_table_row_time')
EXAM_DATA_ROW_LOCATION = EXAM_DATA_ROW + _.x('results_page', 'course_entry', 'exam_table_row_location')
EXAM_DATA_ROW_NOTES = EXAM_DATA_ROW + _.x('results_page', 'course_entry', 'exam_table_row_notes')

class CourseEntry:
    def __init__(self, driver : Driver, elem):
        self.driver = driver
        self.elem = elem
        
        self.show_dates_button = driver.find_x(_.x('results_page', 'course_entry', 'btn_exam_dates'), parent=elem,timeout=0.1)
        if not self.show_dates_button:
            return
        
        exam_length_ = driver.find_x(_.x('results_page', 'course_entry', 'label_exam_length'), parent=elem).text
        self.exam_length = re.search(r'\d.\d\d', exam_length_).group()

        self.course_name = driver.find_x(_.x('results_page', 'course_entry', 'label_course_name'), parent=elem).text

        raw_course_id = driver.find_x(_.x('results_page', 'course_entry', 'label_course_id'), parent=elem).text
        self.course_id = re.search(r'\d{5,6}', raw_course_id).group()
        
        self.exam_entries = []

    def remove_elem(self):
       self.driver.remove_elem(self.elem)
    
    def show_dates(self):
        self.show_dates_button.click()
    
    def get_date_table_entries(self):
        table = self.driver.find_x(_.x('results_page', 'course_entry', 'exam_data_container'), parent=self.elem, timeout=0.1)
        if not table:
            self.show_dates()
            table = self.driver.find_x(EXAM_DATA_TABLE, parent=self.elem, timeout=3)
            
        rows = self.driver.find_x_multi(EXAM_DATA_ROW, parent=table)
        
        entries = []
        
        for row in rows:
          try:  
            # Sample date format: 01-01-2024
            raw_date = self.driver.find_x(EXAM_DATA_ROW_DATE, parent=row, timeout=.1).text
            date = raw_date.split('-')
            year = int(date[2])
            month = int(date[1])
            day = int(date[0])


            raw_time = self.driver.find_x(EXAM_DATA_ROW_TIME, parent=row, timeout=.1).text
            time = raw_time.split(':')
            hour = int(time[0])
            minute = int(time[1])

            notes = self.driver.find_x(EXAM_DATA_ROW_NOTES, parent=row, timeout=.1).text

            location = self.driver.find_x(EXAM_DATA_ROW_LOCATION, parent=row, timeout=.1).text

            new_entry = {
                'course_id': self.course_id,
                'course_name': self.course_name,
                'exam_length': self.exam_length,
              'date': (year, month, day),
              'time': (hour, minute),
              'notes': notes,
              'location': location
            }

            entries.append(new_entry)
            # print(new_entry)
            
          except Exception as e:
            print('Error processing row: ', e)
            print(row.text)
            print('\n\n')
            continue

        self.exam_entries = entries
        self.show_dates()
        self.remove_elem()
        return entries


class ResultPage:
    def __init__(self, driver : Driver):
        self.driver = driver
        self.results = None
        self.entries = None
    
    def get_results(self):
        if self.results is None:
            self.results = self.driver.find_x_multi(_.x('results_page', 'course_entry','main'))
        
        return self.results
    
    def process_entries(self,force=False):

        script = ""
        with open('src/phoebus_scrape.js', 'r',encoding="utf8") as f:
            script = f.read()
        
        try:
            self.entries = self.driver.execute_script(script)
        except TimeoutException as e:
            print('Timeout error while processing entries')
            print(e)
            return []
        
        return self.entries

    def next_page(self):
        next_button = self.driver.find_x("//a[@title='העמוד הבא']",timeout=2)
        if next_button:
            next_button.click()
            self.entries = None
            self.results = None
            return True
        return False