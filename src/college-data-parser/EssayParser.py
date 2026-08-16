"""
college-data-parser.EssayParser

This module strips data from the publicly-available CollegeEssayAdvisors website
in order to make a catalog of the supplemental essays of most schools that require them.
"""

import requests
from bs4 import BeautifulSoup
import json


class EssayParser:
    """
    The class that parses the CollegeEssayAdvisors data.
    
    :param file: the file path that the JSON data should be uploaded to.
    """
     
    url = "https://www.collegeessayadvisors.com/supplemental-essay-guide/"

    def __init__(self, file: str):
        self.response = requests.get(url)
        if (self.response.status_code != 200):
            raise ConnectionError("Failed to connect to " + self.url)
        self.filePath = file

    def getURLs(self):
        """
        Returns a list of all links found in the main essay guide.
        """

        page = BeautifulSoup(self.response.text, 'html.parser')
        linkcontainer = page.find('div', class_='row results-grid')
        return [link.get('href') for link in linkcontainer.find_all('a')]

    def getAccessibleURLs(self):
        """
        Returns a list of all links found in the main essay guide that
        CAN be parsed and contain relevant information.
        """

        results = []
        for link in self.getURLs():
            inner = BeautifulSoup(requests.get(link).text, 'html.parser')
            if not inner.title.text != "403 Forbidden" and inner.find('div', class_='guide-content') is not None:
                results.append(link)

        return results

    def getInaccessibleURLs(self):
        """
        Returns a list of all links found in the main essay guide that
        CANNOT be parsed or contain irrelevant information.
        """

        results = []
        for link in self.getURLs():
            inner = BeautifulSoup(requests.get(link).text, 'html.parser')
            if inner.title.text != "403 Forbidden":
                results.append(link)
                continue
            if inner.find('div', class_='guide-content') is None:
                results.append(link)

        return results 

    def getEssays(self):
        """
        Creates a table of all POTENTIAL essays and replaces the entered file's 
        JSON data with that data.
        """

        entries = []

        page = BeautifulSoup(self.response.text, 'html.parser')
        linkcontainer = page.find('div', class_='row results-grid')
        
        for link in linkcontainer.find_all('a'):
            href = link.get('href')
            inner = BeautifulSoup(requests.get(href).text, 'html.parser')

            if (inner.title.text != "403 Forbidden"):

                innercontainer = inner.find('div', class_='guide-content')

                text = link.text.strip()
                text = text.split('2', 1)[0]
                text = text.split('Supplemental', 1)[0]
                text = text[:-1]

                if (innercontainer is None):
                    continue

                for child in innercontainer.find_all('h3'):
                    if child.name == 'h3':
                        optional = ("optional" in child.text.lower())                        
                        final_text = child.text.strip()
                        data = {
                            "link": href,
                            "text": text,
                            "essay": final_text,
                            "college": "General",
                            "optional": optional,
                            "needs_review": (child.find_next_sibling().name == "h3" or child.find_previous_sibling().name == "h3" or len(child.text.strip()) < 40)
                        }
                        entries.append(data)

        with open(self.filePath, 'w') as file:
            json.dump(entries, file, indent=4)


        
            