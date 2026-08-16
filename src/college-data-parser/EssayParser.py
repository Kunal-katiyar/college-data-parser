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
            raise ConnectionError("Failed to connect to https://www.collegeessayadvisors.com/supplemental-essay-guide/")
        self.filePath = file

    def getURLs(self):
        """
        Returns a list of all links found in the main essay guide.
        """

        page = BeautifulSoup(self.response.text, 'html.parser')
        linkcontainer = page.find('div', class_='row results-grid')
        return [link.get('href') for link in linkcontainer.find_all('a')]

    def getAccessible(self):
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

    def getInaccessible(self):
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
        Returns a list of all POTENTIAL essays found within the links.
        """
        
    
        