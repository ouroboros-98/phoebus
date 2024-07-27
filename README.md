# HUJI Shnaton Exam Table Scraper
This small project is a Python-based web scraper designed to extract exam table data from the HUJI 'Shnaton' website.
The scraper navigates through the website, selects specific faculties and courses, and extracts relevant exam data.

## Features
- **Create Scan Map**: Given relevant faculties, the scan map will contain all departments and degrees which will be scanned for exam data.
- **Scrape Data**: This feature navigates through the website, selects the faculties and courses from the scan map, and extracts the exam data.
- **Process Data:** This feature processes the scraped data, removes duplicates, calculates exam end times, and saves the data in a CSV file.

## Dependencies
Install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```

## Usage
The script can be run from the command line with the following syntax:
```bash
python phoebus.py <action>
```
Where <action> can be one of the following:  
- `map`: to create a scan map
- `scrape`: to scrape data
- `process`: to process the scraped data

## Configuration
The config.json file contains various configuration options, such as the URL of the HUJI Shnaton, relevant faculties to be scraped, and XPaths for various elements on the website.  

## Output
The script outputs a processed.csv file containing the processed exam data. The CSV file includes the following columns: date, location, start time, end time, length, course ID, course name, and notes.