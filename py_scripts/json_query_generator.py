import json

def sqv_list():
    # This function checks for all ID's in the file "fixed_ID" against those in the search_query json-file. New ID's will be stored in this funtion
    with open('temp_ID_timelines/fixed_ID','r') as fixed_ID, open('search.json','r') as search_json:
        temporary_fixed = list(fixed_ID)

        for lines in search_json:
            json_file = json.loads(lines)
            id_in_json = json_file.keys()
            for key in id_in_json:
                for id_items in temporary_fixed:
                    if id_items.replace("\n","") != key and len(id_items.replace("\n","")) > 4:
                        yield id_items.replace("\n","")


def sqv_formatter():
    # This function formats the new ID's into a json-fitting query string
    for item in sqv_list():
        yield {str(item) : {u"remove": False, u"since_id": 1, u"user_id": int(item)}}

def query_update():
    # Update the json query-file with the new data
    with open('search.json') as query_file:
        data = json.load(query_file)

    for id_item in sqv_formatter():
        data.update(id_item)

    with open('search.json','w') as query_file:
        json.dump(data, query_file)


query_update()
