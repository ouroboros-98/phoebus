import datetime
import json
import re
from pprint import pprint
from src.config import CONFIG as _
from src.driver import Driver
from src.search_form import SearchForm
from argparse import ArgumentParser

from selenium.webdriver.remote.webelement import WebElement

import time
import os

def setup_args():
    # Main actions (Required): create scan map, scrape shnaton, process data
    args = ArgumentParser(description='HUJI Exam Table scraper')
    MSG_USAGE = 'Usage: python phoebus.py <action> [options]'
    args.add_argument('action', type=str, help='Main action to perform', choices=['map', 'scrape', 'process'])
    return args.parse_args()


def create_scan_map():
    driver = Driver()

    driver.get(_.main_url)
    remaining = {}
    form  = SearchForm(driver)

    for f in _.relevant_faculties:
        form.get_all_faculties()
        remaining[f] = {}
        form.set_faculty(f)
        hug_options = form.get_all_hugim()
        for hug in hug_options:
            if hug in ['','0','00','000','0000','00000','000000']:
                continue
            form.set_hug(hug)
            maslul_options = form.get_all_maslulim()
            remaining[f][hug] = [m for m in maslul_options.keys() if m not in ['','0','00','000','0000','00000','000000']]
            form.reset_fields(maslul=True)


def scrape_shnaton():
    driver = Driver()

    driver.get(_.main_url)

    total_entries = validate_data_file()

    total_count = 0

    remaining = {}
    with open('scan_map.json', 'r', encoding='utf8') as f:
        remaining = json.load(f)

    for f in remaining.keys():
        for h in remaining[f].keys():
            for m in remaining[f][h]:
                total_count += 1

    progress = 1

    while remaining.keys():
        form  = SearchForm(driver)
        faculty_options = form.get_all_faculties()

        f = list(remaining.keys())[0]
        form.set_faculty(f)
        hug_options = form.get_all_hugim()
        hug = list(remaining[f].keys())[0]
        form.set_hug(hug)
        maslul_options = form.get_all_maslulim()
        
        maslul = remaining[f][hug][0]

        form.set_maslul(maslul)
        
        print(f'[ {progress}/{total_count} ] {f} - {hug} - {maslul}')

        results_page = form.search()
        while True:
            results = results_page.get_results()
            total_entries.extend(results_page.process_entries())
            if not results_page.next_page():
                break
        
        json.dump(total_entries, open('results.json', 'w'))
        progress += 1

        remaining[f][hug].remove(maslul)
        if not remaining[f][hug]:
            del remaining[f][hug]
        if not remaining[f]:
            del remaining[f]

        json.dump(remaining, open('scan_map.json', 'w'))


def validate_data_file():
    # check file exits
    not_exist = not os.path.exists('results.json')
    file_empty = not not_exist and os.stat('results.json').st_size == 0
    if not_exist or file_empty:
        with open('results.json', 'w', encoding='utf8') as f:
            f.write('[]')
            return []
    return json.load(open('results.json', 'r', encoding='utf8'))
        

def process_data():
    data = validate_data_file()
    
    # For arrangement in set (for duplicate removal), we will store each object to a tuple as follows:
    # (entry.date, entry.time, entry.location, entry.length) : entry

    regex = _.location_regex_list;

    total = 0

    processed = {}
    for entry in data:
        if "C1" in entry['location']:
            ...
        location = ""
        for r in regex:
            if re.match(r, entry['location']):
                location = re.match(r, entry['location']).group(0)
                entry['location'] = location
                total += 1
                break
        if not location:
            continue
        entry['date'] = entry['date'].replace('/', '-')
        key = (entry['date'], entry['time'], location, entry['exam_length'])
        if key not in processed:
            processed[key] = entry
    
    pprint(processed)

    csv_data = []

    # Example date format: 16-06-2024
    DATE_FORMAT = '%d-%m-%Y'
    TIME_FORMAT = '%H:%M'

    # Calculate End Times
    for key in processed.keys():
        entry = processed[key]
        dt = datetime.datetime(1900, 1, 1)
        dt = dt.strptime(entry['date'], DATE_FORMAT)
        dt = dt.strptime(entry['time'], TIME_FORMAT)
        dt = dt + datetime.timedelta(minutes=int(float(entry['exam_length'])*60))
        processed[key]['end_time'] = dt.strftime(TIME_FORMAT)



    # Sort by date, then location, then time

    processed = {k: v for k, v in sorted(processed.items(), key=lambda item: (time.strptime(item[0][0], DATE_FORMAT), item[0][2], time.strptime(item[0][1], TIME_FORMAT)))}    


    for key in processed.keys():
        entry = processed[key]
        csv_data.append([entry['date'], entry['location'], entry['time'], entry['end_time'], entry['exam_length'], entry['course_id'], entry['course_name'], entry['notes']])
    
    with open('processed.csv', 'w', encoding='utf8') as f:
        f.write('date,location,time,end_time,length,course_id,course_name,notes\n')
        for row in csv_data:
            row = [str(item).encode("utf-8").decode("utf-8") for item in row]
            row = ','.join(row) + '\n'
            f.write(row)
    
    print('Data processed and saved to processed.csv')
    print(f"Total entries (before filtering): {total}")
    


if __name__ == '__main__':
    args = setup_args()
    if args.action == 'map':
        create_scan_map()
    elif args.action == 'scrape':
        scrape_shnaton()
    elif args.action == 'process':
        process_data()

