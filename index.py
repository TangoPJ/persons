import json
import re
import pandas as pd


def read_data_from_file(file):
    """Initial data

    :param file: the absolute path to the JSON file
    :return: JSON format file
    """

    with open(file, encoding='utf8') as f:
        opened_file = json.load(f)
    return opened_file


def division_name_surname(obj):
    """This function divides into a surname and a name

    :param param: JSON format data
    :return: JSON format data with name and surname fields
    """

    for person in obj:
        person["Surname"], person["Name"] = person["Name"].split()


def get_person_not_in_bg(sm, bg):
    """The function return persons from small data, who are not in the big data
    :param sm: small_data JSON
    :param bg: big_data JSON
    :return: list of persons
    """

    return [v for v in sm if v['Surname'] not in str([_['Surname'] for _ in bg])]


def namesake_age_difference(sm, bg):
    """Namesakes with an age difference of 10 years
    :param sm: small_data JSON
    :param bg: big_data JSON
    :return: list of persons
    """
    return [v for v in sm if
            v['Surname'] in str([_['Surname'] for _ in bg if abs(int(v["Age"]) - int(_["Age"])) == 10])]


def get_eng_letters(dt):
    """The function searches the English letters in the surname or in the name of persons

    :param dt: data JSON format
    :return: list of person
    """
    return [v for v in dt if re.search(r'[a-zA-Z]', v["Name"]) or re.search(r'[a-zA-Z]', v["Surname"])]


def main():
    small_data = 'small_data_persons.json'
    big_data = 'big_data_persons.json'
    result_data = 'main_data.xlsx'

    small_dataset = read_data_from_file(small_data)
    big_dataset = read_data_from_file(big_data)

    division_name_surname(small_dataset)
    division_name_surname(big_dataset)

    small_dataset.sort(key=lambda k: k['Surname'])
    big_dataset.sort(key=lambda k: k['Name'])

    with pd.ExcelWriter(result_data) as writer:
        data = {
            "small_data": small_dataset,
            "big_data": big_dataset,
            "persons_who_are_not_in_big_data": get_person_not_in_bg(small_dataset, big_dataset),
            "namesake_age_difference": namesake_age_difference(small_dataset, big_dataset),
            "english_letters_in_small_data": get_eng_letters(small_dataset),
            "english_letters_in_big_data": get_eng_letters(big_dataset),
        }

        for key, value in data.items():
            df = pd.DataFrame(value)
            df.to_excel(writer, key)


if __name__ == '__main__':
    main()
