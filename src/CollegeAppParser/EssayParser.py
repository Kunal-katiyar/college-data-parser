"""
college-data-parser.EssayParser

This module strips data from the publicly-available CollegeEssayAdvisors website
in order to make a catalog of the supplemental essays of most schools that require them.
"""

import requests
from bs4 import BeautifulSoup
import json
import os


class EssayParser:
    """
    The class that parses the CollegeEssayAdvisors data.
    
    :param file: the file path that the JSON data should be uploaded to.
    """
     
    url = "https://www.collegeessayadvisors.com/supplemental-essay-guide/"
    required_keys = ["link", "university", "essay", "college", "optional", "needs_review"]
    default_values = {
        "link": "", 
        "university": "", 
        "essay": "", 
        "college": "General", 
        "optional": False, 
        "needs_review": False
    }

    def __init__(self, file: str):
        if not os.path.exists(file):
            raise FileNotFoundError("File "+file+" not found")
        self.filePath = file

        self.response = requests.get(self.url)
        if (self.response.status_code != 200):
            raise ConnectionError("Failed to connect to " + self.url)

    @staticmethod
    def getURLs():
        """
        Returns a list of all links found in the main essay guide.
        """

        response = requests.get("https://www.collegeessayadvisors.com/supplemental-essay-guide/")

        if (response.status_code != 200):
            raise ConnectionError("Failed to connect to " + url)
        
        page = BeautifulSoup(response.text, 'html.parser')
        linkcontainer = page.find('div', class_='row results-grid')

        return [link.get('href') for link in linkcontainer.find_all('a')]

    @staticmethod
    def getAccessibleURLs():
        """
        Returns a list of all links found in the main essay guide that
        CAN be parsed and contain relevant information.
        """

        results = []
        for link in EssayParser.getURLs():
            inner = BeautifulSoup(requests.get(link).text, 'html.parser')
            if inner.title.text != "403 Forbidden" and inner.find('div', class_='guide-content') is not None:
                results.append(link)

        return results

    @staticmethod
    def getInaccessibleURLs():
        """
        Returns a list of all links found in the main essay guide that
        CANNOT be parsed or contain irrelevant information.
        """

        results = []
        for link in EssayParser.getURLs():
            inner = BeautifulSoup(requests.get(link).text, 'html.parser')

            if inner.title.text == "403 Forbidden" or inner.find('div', class_='guide-content') is None:
                results.append(link)
                

        return results 

    def parseEssays(self):
        """
        Creates a table of all POTENTIAL essays and replaces the entered file's 
        JSON data with that data.

        Returns the number of entries that need review.
        """

        entries = []

        page = BeautifulSoup(self.response.text, 'html.parser')
        linkcontainer = page.find('div', class_='row results-grid')

        total_review = 0

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
                    if child != None and child.name == 'h3':

                        optional = ("optional" in child.text.lower())                        
                        final_text = child.text.strip()

                        if (len(final_text) > 3):
                            needs_review = ((child.find_next_sibling() != None and child.find_next_sibling().name == "h3") or 
                                            (child.find_previous_sibling() != None and child.find_previous_sibling().name == "h3")
                                            or len(final_text) < 40)
                            
                            if needs_review:
                                total_review += 1

                            data = {
                                "link": href,
                                "university": text,
                                "essay": final_text,
                                "college": "General",
                                "optional": optional,
                                "needs_review": needs_review
                            }
                        
                            entries.append(data)

        with open(self.filePath, 'w') as file:
            json.dump(entries, file, indent=4)

        return total_review

    def review(self):
        """
        Loops through all JSON data and manually queries the user about essays that are marked as 
        'needs_review.'
        """

        with open(self.filePath, "r") as file:
            data = json.load(file)

        previous = 0
        i = 0

        print("---- Type 'stop' to stop parsing and save data ----")
        print("---- Type 'back' to go back to the previous response ----")
        while i < len(data):
            entry = data[i]
            if (entry["essay"] == ""):
                continue

            i += 1

            if entry["needs_review"]:

                print(entry["essay"])
                result = input("(k)eep, (m)ark, or (r)emove: ")
            
                if result == "r":
                    i -= 1
                    data.remove(entry)
                    continue

                elif result == "k":
                    entry["needs_review"] = False

                elif result == "stop":
                    break

                elif result == "back":
                    i = previous
                    data[i]["needs_review"] = True

                previous = i - 1


        with open(self.filePath, 'w') as file:
            json.dump(data, file, indent=4)

    def addData(self, new_data):
        """
        Used for manually adding data to the JSON file, if any colleges with essays are not included or 
        essays have wrongly been omitted.
        """

        if isinstance(new_data, dict):
            new_data = [new_data]

        with open(self.filePath, "r") as file:
            data = json.load(file)

        new_data = sorted(new_data, key=lambda x: x["university"].lower())

        for entry in new_data:
            if "university" not in entry:
                raise KeyError("The 'university' key must be present in all entry values")
            
            for item in self.required_keys:
                if not item in entry:
                    entry[item] = self.default_values[item]

            if entry.keys() != data[0].keys():
                raise KeyError("Only the following keys may be present: 'link', 'university', 'essay', 'college', 'optional', 'needs_review'")
        
        i = 0
        j = 0

        while i < len(data) and j < len(new_data):
            if data[i]["university"] <= new_data[j]["university"]:
                i += 1
            else:
                data.insert(i, new_data[j])
                j += 1

        while j < len(new_data):
            data.append(new_data[j])
            j += 1

        with open(self.filePath, 'w') as file:
            json.dump(data, file, indent=4)