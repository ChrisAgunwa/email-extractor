#importing the necessary libraries

import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def extract_emails_from_website(url):
    """
    Extracts email addresses from a given website.

    Args:
        url (str): The URL of the website from which to extract email addresses.

    Returns:
        list: A list of email addresses extracted from the website.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
            return emails
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")
        return []


def save_emails_to_csv(emails, filename):
   """
    Saves a list of email addresses to a CSV file.

    Args:
        emails (list): A list of email addresses to be saved.
        filename (str): The name of the CSV file to which the emails will be saved.

    Returns:
        None
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email'])
        for email in emails:
            writer.writerow([email])


def extract_emails_from_websites(websites):
     """
    Extracts email addresses from multiple websites concurrently.

    Args:
        websites (list): A list of website URLs from which to extract email addresses.

    Returns:
        list: A list of unique email addresses extracted from the specified websites.
    """
    all_emails = set()  # Use a set to store unique emails
    with ThreadPoolExecutor() as executor:
        results = executor.map(extract_emails_from_website, websites)
        for emails in results:
            all_emails.update(emails)  # Add emails to the set
    return list(all_emails)  # Convert set back to list for compatibility with CSV



# List of websites to extract emails from
websites = [
    'https://goal.com',
    'https://marca.com',
    'https://heirstechnologies.com'
    # Add more websites as needed



  # Extract emails from multiple websites simultaneously
all_emails = extract_emails_from_websites(websites)

# Save emails to CSV file
save_emails_to_csv(all_emails, 'emails.csv')

print("Emails extracted and saved to emails.csv")
