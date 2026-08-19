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

# 💻 Installation Instructions

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

# 🌐 Public Database
Anyone is allowed to use the public JSON files located in the `public_data` folder. If you end up using this
in a project, consider starring the repository. It takes a lot of time and effort to manually review the data, 
so I'd really appreciate the support!

# 📝 Documentation
## EssayParser.py

<details>
<summary><b><code>EssayParser.__init__(file)</code></b></summary>  
<br>

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file` | `str` | *Required* | The JSON file that the instance will write to and read from. |

**Raises:**
* `FileNotFoundError`: If `file` is not a valid file path in your project.
* `ConnectionError`: If the method fails to connect to the website for parsing.

**Example:**
```python
from CollegeAppParser import EssayParser

# Initialize an EssayParser object
EP = EssayParser('path/to/your_file.json')
```
</details>

<details>
<summary><b><code>EssayParser.getURLs()</code></b></summary>

<br>

**No Parameters**  
*This is a static method.*

**Raises:**
* `ConnectionError`: If the method fails to connect to the website for parsing.

**Returns:**
* `list`: The list of all links found in the main essay guide.

**Example:**
```python
from CollegeAppParser import EssayParser

# Print out all URLs
print(EssayParser.getURLs())
```
</details>

<details>
<summary><b><code>EssayParser.getAccessibleURLs()</code></b></summary>

<br>

**No Parameters**  
*This is a static method.*

**Raises:**
* `ConnectionError`: If the method fails to connect to the website for parsing.

**Returns:**
* `list`: The list of all accessible and parsable links found in the main essay guide.

**Example:**
```python
from CollegeAppParser import EssayParser

# Print out all accessible URLs
print(EssayParser.getAccessibleURLs())
```
</details>

<details>
<summary><b><code>EssayParser.getInaccessibleURLs()</code></b></summary>

<br>

**No Parameters**  
*This is a static method.*

**Raises:**
* `ConnectionError`: If the method fails to connect to the website for parsing.

**Returns:**
* `list`: The list of all inaccessible and unparsable links found in the main essay guide.

**Example:**
```python
from CollegeAppParser import EssayParser

# Print out all inaccessible URLs
print(EssayParser.getInaccessibleURLs())
```
</details>

<details>
<summary><b><code>EssayParser.parseEssays()</code></b></summary>

<br>

**No Parameters**  

**Functionality:**
* Populates `file` with the full parsed essay data.

**Returns:**
* The number of essay entries that need manual review.

**Example:**
```python
from CollegeAppParser import EssayParser

# Create a new EssayParser object
EP = EssayParser('path/to/your_file.json')
print(EP.parseEssays()) # Prints out the number of entries that need review, usually ~100
```
</details>

<details>
<summary><b><code>EssayParser.review()</code></b></summary>

<br>

**No Parameters**  

**Functionality:**
* Manually queries the user about each entry in `file` marked as `'needs_review'`.

**Example:**
```python
from CollegeAppParser import EssayParser

# Create a new EssayParser object
EP = EssayParser('path/to/your_file.json')
EP.parseEssays()
EP.review() # Sends inputs to the terminal for each flagged entry
```
</details>

<details>
<summary><b><code>EssayParser.addData(entries)</code></b></summary>

<br>

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `entries` | `dict` or `list` | *Required* | The data that will be added to the JSON file, as a single `dict` or as a list of them |

**Raises:**
* `KeyError`: If any of the manual entries contain a key not within the set `["link", "university", "essay", "college", "optional", "needs_review"]`

**Example:**
```python
from CollegeAppParser import EssayParser

# Create a new EssayParser object
EP = EssayParser('path/to/your_file.json')
EP.parseEssays()

data = [
{
    "university": "AAAAA Test University",
    "essay": "Test Essay"
},
{
    "university": "AAAAB Test University",
    "essay": "Test Essay"
},
{
    "university": "ZZZZZ Test University",
    "essay": "Test Essay"
}
]

EP.addData(data) # Will add that custom data to the JSON, sorted alphabetically
```
</details>

## DeadlineParser.py
<details>
<summary><b><code>DeadlineParser.__init__(file)</code></b></summary>

<br>

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file` | `str` | *Required* | The JSON file that the instance will write to and read from. |

**Raises:**
* `FileNotFoundError`: If `file` is not a valid file path in your project.
* `ConnectionError`: If the method fails to connect to the website for parsing.

**Example:**
```python
from CollegeAppParser import DeadlineParser

# Initialize a DeadlineParser object
DP = DeadlineParser('path/to/your_file.json')
```
</details>

<details>
<summary><b><code>DeadlineParser.parseDeadlines()</code></b></summary>

<br>

**No Parameters**  

**Functionality:**
* Populates `file` with the full parsed deadline data.

**Example:**
```python
from CollegeAppParser import DeadlineParser

# Create a new DeadlineParser object
DP = DeadlineParser('path/to/your_file.json')
DP.parseDeadlines() # Populates the JSON file
```
</details>

<details>
<summary><b><code>DeadlineParser.addData(entries)</code></b></summary>

<br>

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `entries` | `dict` or `list` | *Required* | The data that will be added to the JSON file, as a single `dict` or as a list of them |

**Raises:**
* `KeyError`: If any of the manual entries contain a key not within the set `["university", "ED_deadline", "ED2_deadline", "EA_deadline", "EA2_deadline", "REA_deadline", "RD_deadline"]`

**Example:**
```python
from CollegeAppParser import DeadlineParser

# Create a new DeadlineParser object
DP = DeadlineParser('path/to/your_file.json')
DP.parseDeadlines()

data = [
    {
        "university": "Massachusetts Institute of Technology",
        "EA_deadline": "11/1/2026",
        "RD_deadline": "1/4/2027"
    },
    {
        "university": "University of Texas at Austin",
        "EA_deadline": "10/15/2026",
        "RD_deadline": "12/1/2026"
    },
    {
        "university": "Georgia Institute of Technology",
        "EA_deadline": "10/15/2026",
        "EA2_deadline": "11/2/2026",
        "RD_deadline": "1/6/2027"
    }
]

DP.addData(data) # Will add that custom data to the JSON, sorted alphabetically
```
</details>

## Public Database Documentation

**These structures are the same that `EssayParser.parseEssays()` and `DeadlineParser.parseDeadlines()` create.**

<details>
<summary><b><code>essay_data.json</code></b></summary>

<br>

| Key | Type | Description |
| :--- | :--- | :--- |
| `link` | `str` | The link to the CollegeEssayAdvisors article for the essay/university. |
| `university` | `str` | The university that the essay belongs to. |
| `essay` | `str` | The actual content of the essay. |
| `college` | `str` | The college within the university that the essay belongs to (usually `"General"` with the exception of a few colleges. |
| `optional` | `bool` | Whether the essay is optional or not (may not be accurate 100% of the time). |
| `needs_review` | `bool` | Whether the entry needs review (will be `false` for all public database entries). |

</details>

<details>
<summary><b><code>deadline_data.json</code></b></summary>

<br>

| Key | Type | Description |
| :--- | :--- | :--- |
| `university` | `str` | The university that these deadlines belong to. |
| `ED_deadline` | `str` | The ED deadline of the university (`""` if N/A). |
| `ED2_deadline` | `str` | The ED2 deadline of the university (`""` if N/A). |
| `EA_deadline` | `str` | The EA deadline of the university (`""` if N/A). |
| `EA2_deadline` | `str` | The EA2 deadline of the university (`""` if N/A). |
| `REA_deadline` | `str` | The REA deadline of the university (`""` if N/A). |
| `RD_deadline` | `str` | The RD deadline of the university (`""` if N/A, `"Rolling"` if rolling). |

</details>


## 📄 License
Distributed under the terms of the MIT License. Check out the `LICENSE` file for more concrete legal information.
