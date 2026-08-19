"""
college-data-parser.DeadlineParser

This module strips data from the CommonApp requirement grid in 
order to make a list of the deadlines of all CommonApp schools.
"""

from io import BytesIO
import pdfplumber
import requests
import json
import os

class DeadlineParser:
    """
    The class that parses the CommonApp data.

    :param file: the file path that the JSON data should be uploaded to.
    """

    url = "https://content.commonapp.org/Files/ReqGrid.pdf"
    required_keys = ["university", "ED_deadline", "ED2_deadline", "EA_deadline", "EA2_deadline", "REA_deadline", "RD_deadline"]

    def __init__(self, file: str) :
        if not os.path.exists(file):
            raise FileNotFoundError("File "+file+" not found")
        self.filePath = file
        
        response = requests.get(self.url)
        if (response.status_code != 200):
            raise ConnectionError("Failed to connect to " + self.url)
        
        self.pdfData = BytesIO(response.content)

    def parseDeadlines(self):
        """
        Parses the file and replaces the entered file's JSON data with that data.
        """

        entries = []
        with pdfplumber.open(self.pdfData) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                for row in table:
                    if row[3] != None and row[2] != "ED":
                        data = {
                            "university": row[0].replace("\n", " "),
                            "ED_deadline": row[2],
                            "ED2_deadline": row[3],
                            "EA_deadline": row[4],
                            "EA2_deadline": row[5],
                            "REA_deadline": row[6],
                            "RD_deadline": row[7]
                        }
                        if data["university"] != "":
                            entries.append(data)

        with open(self.filePath, "w") as file:
            json.dump(entries, file, indent = 4)

    def addData(self, entries):
        """
        Adds custom deadline data to the json file, for instance for colleges that
        do not show up on the CommonApp grid (such as MIT).

        :param entries: The deadline data of the college you wish to add, either as a 
        list of dictonaries or as one dictionary.
        """

        with open(self.filePath, "r") as file:
            filedata = json.load(file)

        if isinstance(entries, dict):
            entries = [entries]

        entries = sorted(entries, key=lambda x: x["university"].lower())

        if isinstance(entries, list):
            i = 0
            j = 0
            newData = []

            for data in entries:
                for item in self.required_keys:
                    if not item in data:
                        data[item] = ""

                if (data.keys() != filedata[0].keys()):
                    raise KeyError("Only the following keys may be present: 'university', 'ED_deadline', 'ED2_deadline', 'EA_deadline', 'EA2_deadline', 'REA_deadline', 'RD_deadline'")

            newData = []
            while i < len(filedata) and j < len(entries):
                if (filedata[i]["university"] == entries[j]["university"]):
                    newData.append(entries[j])
                    j += 1
                    i += 1
                
                else:
                    newData.append(filedata[i])
                    i += 1
            
            while j < len(entries):
                newData.append(entries[j])
                j += 1

            while i < len(filedata):
                newData.append(filedata[i])
                i += 1
                
            filedata = newData
        else:
            raise TypeError("Invalid: data must either be a list or dict")

        filedata = sorted(filedata, key=lambda x: x["university"].lower())

        with open(self.filePath, "w") as f:
            json.dump(filedata, f, indent=4)



    
