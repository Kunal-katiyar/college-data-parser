from college_data_parser.EssayParser import EssayParser
import json

def test_essay_parser():
    EP = EssayParser("tests/essay_parser_test.json")

    print(EP.getInaccessibleURLs()) # Should print a list of all URLs that are inaccesible or cannot be parsed
    print(EP.getAccessibleURLs()) # Should print a list of all URLs that are accesible and can be parsed

    print("number that need review: " + str(EP.parseEssays())) # Should print the number of essays that need review
                                                                 # as well as populate the JSON file

    EP.review() # Should print to the console asking about all essays that need review

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

    EP.addData(data) # Should add the above three data points to the JSON file

    data = {
        "random_data": "data"
    }
    message = False
    try:
        EP.add(data)
    except KeyError:
        message = True

    assert message # Should become true as a KeyError was raised from the bad key
