from college_data_parser.DeadlineParser import DeadlineParser

def test_file_input():
    DP = DeadlineParser("tests/deadline_parser_test.json")

    DP.parseData() # Should populate data into deadline_parser_test.json

    data = {
        "college": "Massachusetts Institute of Technology",
        "EA_deadline": "11/1/2026",
        "RD_deadline": "1/4/2027"
    }

    DP.addData(data) # Should add the MIT data to the JSON file

    
    data = {
        "random_key": "Random"
    }

    message = ""
    try:
        DP.addData(data)
    except KeyError:
        message = "worked"

    assert message == "worked" # Should become "worked" as a KeyError was raised

    data = {
        "college": "Massachusetts Institute of Technology",
        "EA_deadline": "11/1/2026",
        "RD_deadline": "1/4/2027"
    }

    DP.addData(data) # Should not add a duplicate entry