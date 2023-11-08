import requests
from bs4 import BeautifulSoup
import csv

def scrape_jobs(url, limit=30):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize a list to store job data
        job_data = []

        # Find and store job titles, locations, job descriptions, and links to job listings
        for job_card in soup.find_all("div", class_="base-card"):
            job_info = job_card.find("h3", class_="base-search-card__title")
            if job_info:
                job_title = job_info.get_text(strip=True)
                job_location = job_card.find("span", class_="job-search-card__location").get_text(strip=True)
                job_link = job_card.find("a", class_="base-card__full-link")["href"]

                # Send an HTTP GET request to the job listing page to extract the job description
                job_listing_response = requests.get(job_link)
                if job_listing_response.status_code == 200:
                    job_listing_soup = BeautifulSoup(job_listing_response.text, 'html.parser')
                    job_description = job_listing_soup.find("div", class_="description")
                else:
                    job_description = "Description not available"

                job_data.append([job_title, job_location, job_description, job_link])

                # Limit the number of job listings to scrape
                if len(job_data) >= limit:
                    break

        # Define the CSV file name
        csv_filename = "job_data.csv"

        # Save the job data to a CSV file
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Job Title', 'Location', 'Description', 'Job Link'])
            csv_writer.writerows(job_data)

        print(f"Data saved to {csv_filename}")
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

# Set the URL to scrape
url_to_scrape = "https://www.linkedin.com/jobs/search/?currentJobId=3745901935&f_TPR=r2592000&keywords=IT%20jobs&origin=JOB_SEARCH_PAGE_JOB_FILTER"
  # Replace with your desired URL

# Set the limit for the number of job listings to scrape
scrape_limit = 30  # Change this value to the number you want

# Call the scrape_jobs function with the specified URL and limit
scrape_jobs(url_to_scrape, scrape_limit)
