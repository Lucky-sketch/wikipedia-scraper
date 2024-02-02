from requests import Session
from bs4 import BeautifulSoup
import json
import csv
import re

class WikipediaScraper:
    """
    A class for scraping data from a country leaders website.
    """

    def __init__(self, session: Session):
        """
        Initialize the WikipediaScraper instance.

        Parameters:
        - session (Session): The requests Session object.
        """
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        self.check_endpoint = "/check"
        self.session: Session = session
        self.leaders_data = {}
        self.cookie = ""

    def refresh_cookie(self):
        """
        Refresh the cookie by querying the /cookie endpoint.
        """
        cookie_response = self.session.get(f"{self.base_url}{self.cookies_endpoint}")
        self.cookie = cookie_response.cookies

    def get_countries(self):
        """
        Get a list of supported countries from the /countries endpoint.

        Returns:
        - list: List of supported countries.
        """
        countries_response = self.session.get(f"{self.base_url}{self.country_endpoint}", cookies=self.cookie)
        return countries_response.json()

    def get_leaders(self, country):
        """
        Get leaders' data for a specific country from the /leaders endpoint.

        Parameters:
        - country (str): The country for which leaders' data is requested.
        """
        leaders_response = self.session.get(f"{self.base_url}{self.leaders_endpoint}", params={"country": country}, cookies=self.cookie)
        self.leaders_data[country] = leaders_response.json()

    def get_first_paragraph(self, wikipedia_url):
        """
        Fetch the HTML content of the Wikipedia page and extract the first paragraph.

        Parameters:
        - wikipedia_url (str): The Wikipedia URL of a leader.

        Returns:
        - str: The first paragraph text.
        """
        response = self.session.get(wikipedia_url, cookies=self.cookie)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all(name="p"):
            if not tag.find(name="b"): continue
            #The loop to get rid of all the elements that are not relevant like citation or voice-read
            for sup_tag in tag.find_all(name="sup"):
                sup_tag.decompose()
        #The loop to get rid of cases when the tag <p> with subtag <b> located in the table, which helps to find real first paragraph
        for tag in soup.find_all(name="tbody"):
            tag.decompose()

        for i in soup.find_all("p"):
            if i.find("b"):
                if i.text.strip():
                    return i.text

    def to_json_file(self, filepath):
        """
        Store the data structure into a JSON file.

        Parameters:
        - filepath (str): The path to the output JSON file.
        """
        with open(filepath, 'w') as json_file:
            json.dump(self.leaders_data, json_file, ensure_ascii=False, indent=4)

    def to_csv_file(self, filepath):
        """
        Store the data structure into a CSV file.

        Parameters:
        - filepath (str): The path to the output CSV file.
        """
        # Extracting field names from the leaders_data dictionary
        field_names = ["Country"] + list(self.leaders_data[list(self.leaders_data.keys())[0]][0].keys())

        # Writing to the CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)

            # Writing header
            writer.writeheader()
            # Writing data rows
            for country, leaders in self.leaders_data.items():
                for leader in leaders:
                    writer.writerow({"Country": country, **leader})

    def update_leaders_data(self, country, f_paragraph, id):
        """
        Update leaders' data with the first paragraph.

        Parameters:
        - country (str): The country of the leader.
        - f_paragraph (str): The first paragraph text.
        - id (str): The ID of the leader.
        """
        for x in self.leaders_data[country]:
            if x["id"] == id:
                x["first_paragraph"] = f_paragraph

    def cookie_fresh(self):
        """
        Check if the cookie is fresh by querying the /check endpoint.

        Returns:
        - bool: True if the cookie is valid, False otherwise.
        """
        response = self.session.get(f"{self.base_url}{self.check_endpoint}", cookies=self.cookie)
        return "The cookie is valid" in response.text

    @staticmethod
    def clean_paragraph(text: str) -> str:
        """
        Clean up the paragraph text by removing trailing newline and unnecessary parentheses.

        Parameters:
        - text (str): The text to be cleaned.

        Returns:
        - str: The cleaned text.
        """
        text = re.sub(r'\n$', '', text)
        text = re.sub(r'\(\s*\)', '', text)
        return text
