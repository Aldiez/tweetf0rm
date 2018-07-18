import json
import glob, os
import fileinput
import re

extracted_path = r"temp_ID_timelines"
if not os.path.exists(extracted_path):
    os.makedirs(extracted_path)


# function: check whether the string (user ID) is in the document. If not, return the string
def check_file(string, path):
    if str(string) not in open(path).read():
        return str(string)


def json_iterator(data):
    for lines in data:
        json_lines = json.loads(lines)

        # set path to ID files
        temp_path_fixedID = 'temp_ID_timelines/fixed_ID'
        temp_path_tempID = 'temp_ID_timelines/temp_ID'

        # extract reply author ID and screen name and safe them in a new file

        # fetch id and name
        user_id = json_lines["user"]["id"]
        user_screen_name = json_lines["user"]["screen_name"]

        # fetch id and name of reply
        if json_lines["entities"]["user_mentions"] and len(json_lines["entities"]["user_mentions"][0]) > 0:
            reply_id = json_lines["entities"]["user_mentions"][0]["id"]
            reply_name = json_lines["entities"]["user_mentions"][0]["screen_name"]

            substring = {reply_id:reply_name}

            with open(temp_path_fixedID,'a') as fix_ID:
                subchecked = check_file(reply_id, temp_path_fixedID)
                if isinstance(subchecked, str):
                    fix_ID.write(subchecked+"\n")
                    fix_ID.close()
                    with open(temp_path_tempID,'a') as temp_ID:
                        temp_ID.write(str(substring)+"\n")
                        temp_ID.close()

        # concatenate string from id and name
        string = {user_id:user_screen_name}

        # check id and name in fixed_ID file for already existing instances
        with open(temp_path_fixedID,'a') as fix_ID:
            checked = check_file(user_id, temp_path_fixedID)
            if isinstance(checked, str):
                fix_ID.write(checked+"\n")
                fix_ID.close()
                with open(temp_path_tempID,'a') as temp_ID:
                    temp_ID.write(str(string)+"\n")
                    temp_ID.close()


def file_iterator():
    todo_path = os.path.join(os.getcwd(), "data", "timelines")

    ROOT = [os.path.join(todo_path, filename) for filename in os.listdir(todo_path)]


    for x in ROOT:
        if os.path.isdir(x):
            for item in os.listdir(x):
                print(item)
                data = open(os.path.join(x, item),"r")
                json_iterator(data)

file_iterator()
