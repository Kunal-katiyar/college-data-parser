"""
college-data-parser.DeadlineParser

This module strips data from the CommonApp requirement grid in 
order to make a list of the deadlines of all CommonApp schools.
"""

from io import BytesIO
import pdfplumber
import requests
import json

class DeadlineParser:
    """
    The class that does the parsing.

    :param file: the file path that the JSON data should be uploaded to.
    """
    url = "https://content.commonapp.org/Files/ReqGrid.pdf"


    def __init__(self, file: str) :
        self.filePath = file
        response = requests.get(url)
        self.pdfData = BytesIO(response.content)

    def parseData(self):
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
                            "college": row[0].replace("\n", " "),
                            "ED_deadline": row[2],
                            "ED2_deadline": row[3],
                            "EA_deadline": row[4],
                            "EA2_deadline": row[5],
                            "REA_deadline": row[6],
                            "RD_deadline": row[7]
                        }
                        entries.append(data)

        with open(self.filePath, "w") as file:
            json.dump(entries, file, indent = 4)

    
