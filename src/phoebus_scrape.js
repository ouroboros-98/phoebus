XPATHS = {
  "search_form": {
    "faculty_input": "//select[@name='faculty']",
    "hug_input": "//select[@name='hug']",
    "maslul_input": "//select[@name='maslul']",
    "low_details_radiobox": "//input[@id='small']",
    "search_button": "//div[@align='center']/input[@name='search'][@type='button']"
  },
  "results_page": {
    "course_entry": {
      "main": "//div[@class='courseTitle']/ancestor::a[@name][not(@scanned)]",
      "label_course_id": "//table[contains(@summary,'כותרת')]//td[3]/b",
      "label_course_name": "//table[contains(@summary,'כותרת')]//td[2]",
      "btn_exam_dates": "//td[contains(@id,'examDates')]/a",
      "label_exam_length": "//td[contains(text(),'משך הבחינה')]",
      "exam_data_container": "//table[contains(@summary,'רשימת מועדי בחינות לקורס')]",
      "exam_table_semester_b_row": "//td[contains(text(),'סמסטר ב')]/parent::tr[not(@scanned)]",
      "exam_table_row_date": "//td[1]",
      "exam_table_row_time": "/td[2]",
      "exam_table_row_notes": "/td[3]",
      "exam_table_row_location": "/td[4]"
    }
  }
};

const _x = (path, parent = document) => document.evaluate(path, parent, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
const __x = (path, parent = document) => document.evaluate(path, parent, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
const waitForElementXPath = (path, parent = document) => {
  return new Promise((resolve) => {
    const checkElement = () => {
      const element = _x(path, parent);
      if (element) {
        resolve(element);
      } else {
        setTimeout(checkElement, 100);
      }
    };
    checkElement();
  });
};


let entries = [];

const X_BLOCK = XPATHS.results_page.course_entry.main;
const ID = X_BLOCK + XPATHS.results_page.course_entry.label_course_id;
const NAME = X_BLOCK + XPATHS.results_page.course_entry.label_course_name;
const EXAM_LENTGH = X_BLOCK + XPATHS.results_page.course_entry.label_exam_length;
const BUTTON = X_BLOCK + XPATHS.results_page.course_entry.btn_exam_dates;
const CONTAINER = X_BLOCK + XPATHS.results_page.course_entry.exam_data_container;
const ROWS = CONTAINER + XPATHS.results_page.course_entry.exam_table_semester_b_row;
const DATE = ROWS+XPATHS.results_page.course_entry.exam_table_row_date;
const TIME = ROWS+XPATHS.results_page.course_entry.exam_table_row_time;
const NOTES = ROWS + XPATHS.results_page.course_entry.exam_table_row_notes;
const LOCATIONS = ROWS + XPATHS.results_page.course_entry.exam_table_row_location;

const exam_length_regex = '\\d\\.\\d\\d';


await waitForElementXPath(X_BLOCK);
course_blocks = __x(X_BLOCK);

for (let i = 0; i < course_blocks.snapshotLength; i++) {
  let course_block = course_blocks.snapshotItem(i);
  console.log("Course Block", course_block);

  console.log("ID XPath", ID);
  await waitForElementXPath(ID);
  let course_id = _x(ID, course_block).textContent.trim();
  // Leave only digits
  course_id = course_id.replace(/\D/g, "");
  console.log("Course ID", course_id);

  let course_name = _x(NAME, course_block).textContent.trim();
  //console.log("Course Name", course_name);

  let exam_length_raw;
  try {
    exam_length_raw = _x(EXAM_LENTGH, course_block).textContent.trim();
  }
  catch (e) {
    console.log("No Exam Length Found");
    return entries;
  }

  let exam_length = exam_length_raw.match(exam_length_regex)[0];
  console.log("Exam Length", exam_length);
  
  let exam_dates_btn;
  try{
  exam_dates_btn = _x(BUTTON, course_block);
  }
  catch (e) {
    console.log("No Exam Dates Button Found");
    return entries;
  }
  //console.log("Exam Dates Button", exam_dates_btn);

  if (exam_dates_btn) {
    exam_dates_btn.click();
    await waitForElementXPath(CONTAINER, course_block);

    let exam_table = _x(XPATHS.results_page.course_entry.exam_data_container, course_block);
    //console.log("Container", exam_table);

    
    let rows = __x(ROWS, exam_table);
    //console.log("Rows", rows);

    for (let j = 0; j < rows.snapshotLength; j++) {
      let row = rows.snapshotItem(j);
      //console.log("Row", row);

      const date_node = _x(DATE, row);
      //console.log("Date",date_node);
      let date = date_node.textContent.trim();

      const time_node = _x(TIME, row);
      //console.log("Time",time_node);
      let time = time_node.textContent.trim();

      const notes_node = _x(NOTES, row);
        //console.log("Notes",notes_node);
      let notes = notes_node.textContent.trim();

      const location_node = _x(LOCATIONS, row);
        //console.log("Location",location_node);
      let location = location_node.textContent.trim();

      row.setAttribute("scanned", "true");

      entries.push({
        course_id,
        course_name,
        exam_length,
        date,
        time,
        notes,
        location
      });
    }
  }

  course_block.setAttribute("scanned", "true");
}

return entries;