# CollegeAppParser

![Python 3.13.1](https://img.shields.io/badge/Python-3.13-blue?logo=python) 

CollegeAppParser is a Python package that allows for safe, efficient parsing of critical college application data:
application deadlines and supplemental essays. The publicly available database, derived from this package (located in the
`public_data` folder), is a repository of over **450 essay prompts** from over **150 different colleges**, 
and contains the deadlines of around **700 colleges**.

# 📦 Python Package Features

- **Easy-to-understand functions**: Functions are separated across two classes, `EssayParser` and `DeadlineParser`, both of which have simple yet powerful functionality (defined in documentation below).
- **Automatic + manual filtering**: The `DeadlineParser` class automatically parses the CommonApp data and filters out irrelevant rows, while `EssayParser` marks potentially faulty readings for the user to easily review while filtering out obviously wrong ones to minimize manual effort.
- **Reliable data**: Both functionalities use some of the most up-to-date info possible -- info from the CommonApp requirements grid and from the CollegeEssayAdvisors website.
- **Safety measures**: The `EssayParser` class has features to ensure the accuracy of manually-collected data, such as the filtering mentioned above but also access to the list of guide websites which could not be reached (which varies day to day), as well as protections for accidental operations in manual filtering.
- **Customizability**: Even if a college is not present in either database, both classes contain methods to add custom data to the JSON in bulk.

# 🗄️ Public Database Features
- **Easily Parsable**: Data is structured within both the `deadline_data.json` and `essay_data.json` files in a way that makes them easily parsable by common JSON methods.
- **Comprehensive Data**: The `deadline_data.json` contains all standard deadlines for each university (ED, ED2, EA, EA2, REA, and RD). `essay_data.json` has the link of the CollegeEssayAdvisors supplemental essay guide, as well as the college within the university the essay is assigned to, if any.
- **Manually Checked**: The database has been manually checked and reviewed both with the `CollegeAppParser` class methods and meticulously by hand. (But if anything seems off, you can always make a pull request to change something!)

# Installation Instructions

Simply run
```bash
pip install git+https://github.com/Kunal-katiyar/CollegeAppParser
```
to install the package.

In your code, place
```python
from CollegeAppParser import DeadlineParser, EssayParser
```
or whichever of the two packages you need.

# Public Database
Anyone is allowed to use the public JSON files located in the `public_data` folder. If you end up using this
in a project, consider starring the repository. It takes a lot of time and effort to manually review the data, 
so I'd appreciate the support!

