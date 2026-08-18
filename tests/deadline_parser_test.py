from college_data_parser.DeadlineParser import DeadlineParser

def test_deadline_parser():
    DP = DeadlineParser("tests/deadline_parser_test.json")

    DP.parseDeadlines() # Should populate data into deadline_parser_test.json

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

    DP.addData(data) # Should add the college data to the JSON file

    
    data = {
        "random_key": "Random" # Adding invalid data to the JSON
    }

    message = False
    try:
        DP.addData(data)
    except KeyError:
        message = True

    assert message # Should become True as a KeyError was raised

    data = {
        "university": "Massachusetts Institute of Technology",
        "EA_deadline": "11/1/2026",
        "RD_deadline": "1/4/2027"
    }

    DP.addData(data) # Should not add a duplicate MIT entry

