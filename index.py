import json
import re
import pandas as pd
 
 
def read_json(path):
    """Loads JSON from a file
 
   :param path: absolute path to a JSON file
   :return: dataset, containing JSON data
   """
 
    with open(path, encoding='utf8') as f:
        data = json.load(f)
    return data
 
 
def split_full_name(container):
    """Splits the full name into name and surname
 
   :param container: raw dataset
   :return: processed dataset
   """
 
    for person in container:
        person["Surname"], person["Name"] = person["Name"].split()
 
 
def find_missing(small, big):
    """Filters small data, returning persons, missing in the big data
 
   :param small: small_data dataset
   :param big: big_data dataset
   :return: list of persons
   """
 
    return [v for v in small if v['Surname'] not in str([_['Surname'] for _ in big])]
 
 
def find_namesakes_with_age_diff(small, big, diff=10):
    """Finds namesakes with an age difference of diff years
 
   :param small: small_data dataset
   :param big: big_data dataset
   :param diff: age difference
   :return: list of persons
   """
    return [v for v in small if
            v['Surname'] in str([_['Surname'] for _ in big if abs(int(v["Age"]) - int(_["Age"])) == diff])]
 
 
def find_latin_letters(dt):
    """Finds Latin letters in the surname or in the name of persons
 
   :param dt: data JSON format
   :return: list of person
   """
    return [v for v in dt if re.search(r'[a-zA-Z]', v["Name"]) or re.search(r'[a-zA-Z]', v["Surname"])]
 
 
def main():
    small_path = 'small_data_persons.json'
    big_path = 'big_data_persons.json'
    result_data = 'main_data.xlsx'
 
    small_dataset = read_json(small_path)
    big_dataset = read_json(big_path)
 
    split_full_name(small_dataset)
    split_full_name(big_dataset)
 
    small_dataset.sort(key=lambda k: k['Surname'])
    big_dataset.sort(key=lambda k: k['Name'])
 
    with pd.ExcelWriter(result_data) as writer:
        data = {
            "small_data": small_dataset,
            "big_data": big_dataset,
            "persons_who_are_not_in_big_data": find_missing(small_dataset, big_dataset),
            "namesake_age_difference": find_namesakes_with_age_diff(small_dataset, big_dataset),
            "english_letters_in_small_data": find_latin_letters(small_dataset),
            "english_letters_in_big_data": find_latin_letters(big_dataset),
        }
 
        for key, value in data.items():
            df = pd.DataFrame(value)
            df.to_excel(writer, key)
 
 
if __name__ == '__main__':
    main()
