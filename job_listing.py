import requests
from bs4 import BeautifulSoup
import csv

headers_param = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# Send a GET request to Website
glassdoor = requests.get('https://www.glassdoor.com/List/Best-Jobs-in-America-LST_KQ0,20.htm', headers=headers_param)
jobs = glassdoor.content
soup = BeautifulSoup(jobs, 'html.parser')

# Initialize an empty list to store job data
job_data = []

# Find all job listings on the page
job_listings = soup.find_all('div', class_='d_flex align_items_lg_center px_sm px_lg_0 py_sm ListTable_listingRow__z_lPz')

# Iterate over each job listing
for job_listing in job_listings:
    title = job_listing.find('div', attrs={'data-test': 'job-title-link'})
    salary = job_listing.find('div', attrs={'data-test': 'median-base-salary'}).contents[0]
    satisfaction = job_listing.find('div', attrs={'data-test': 'job-satisfaction'}).contents[0]
    openings_count = job_listing.find('div', attrs={'data-test': 'job-openings-count'}).contents[0]
    
    job_data.append({
        "Title": title.text,
        "Salary": salary.text,
        "Satisfaction": satisfaction.text.split('/')[0],
        "Openings": openings_count.text
    })

# Define the file path for the CSV file
file_path = '/Users/nurlanjalil/Documents/Python/job_listing.csv'

# Check if there is any job data to save
if job_data:
    with open(file_path, 'w', newline='') as file:
        fieldnames = ['Title', 'Salary', 'Satisfaction', 'Openings']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for job in job_data:
            writer.writerow(job)
    print(f'CSV file saved successfully at: {file_path}')
else:
    print('No data to save')
