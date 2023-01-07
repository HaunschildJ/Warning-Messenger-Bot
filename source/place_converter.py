from typing import List, Union, Any, Tuple

import requests
from fuzzywuzzy import process

# District => Kreis
# Place => Ort
# Places are needed for everything besides Covid info
# Districts are needed for Covid info
# Districts' IDs (5 numbers) are shorter than Places' IDs (12 numbers)


_districts_dictionary = {}
"""dictionary district_id : str -> district_name : str """

_places_dictionary = {}
"""dictionary place_id : str -> place_name : str"""

_postal_code_dictionary = {}
"""dictionary postal_code : str -> [place_name : str, district_id : str]"""


def _fill_districts_dict() -> None:
    """
    Fills the _districts_dictionary dictionary with selected infos from
    https://warnung.bund.de/assets/json/converted_corona_kreise.json
    Format: district_id -> district_name
    """
    converted_covid_districts = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for district_id, district_description in converted_covid_districts.items():
        _districts_dictionary[district_id] = district_description["n"]


def _fill_places_dict() -> None:
    """
    Fills the _places_dictionary dictionary with selected infos from
    https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31
    /download/Regionalschl_ssel_2021-07-31.json
    Format: place_id -> place_name
    """
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    for area_triple in bevoelkerungsstaat_key['daten']:
        _places_dictionary[area_triple[0]] = area_triple[1]


def _fill_postal_code_dict() -> None:
    """
    Fills the _postal_code_dictionary dictionary with selected infos from
    https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q=&rows=-1
    Format: postal_code : str -> [place_name : str, district_id : str]
    """
    postal_code_table = requests.get(
        'https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q=&rows=-1').json()
    for record in postal_code_table['records']:
        _postal_code_dictionary[record['fields']['plz_code']] = [record['fields']['plz_name'],
                                                                 record['fields']['krs_code']]


_fill_districts_dict()
_fill_places_dict()
_fill_postal_code_dict()


def _get_suggestions_for_place_name(place_name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id'} with suggestions for the given place name

    Arguments:
        place_name (str): the given place name
    Returns:
        similar_places_dicts (list[dict]): list of suggested dicts
    """
    similar_place_names = process.extract(place_name, _places_dictionary, limit=11)
    similar_places_dicts = []
    for place_info in similar_place_names:
        similar_place_dict = {'place_name': place_info[0], 'place_id': place_info[2]}
        similar_places_dicts.append(similar_place_dict)
    return similar_places_dicts


def _get_place_dict_suggestions(place_name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} with suggestions for the given
    place name

    Arguments:
        place_name (str): the given place name
    Returns:
        place_dict_suggestions (list[dict]): list of suggested dicts
    """
    place_dict_suggestions = _get_suggestions_for_place_name(place_name)

    for place in place_dict_suggestions:
        district_id = place['place_id'][0:5]
        place['district_name'] = _districts_dictionary[district_id]
        place['district_id'] = district_id
    return place_dict_suggestions


def _get_suggestions_for_district_name(district_name: str) -> list[dict]:
    """
    Returns a list of dicts {'district_name', 'district_id'} with suggestions for the given district name

    Arguments:
        district_name (str): the given district name
    Returns:
        similar_districts_dicts (list[dict]): list of suggested dicts
    """
    similar_district_names = process.extract(district_name, _districts_dictionary, limit=11)
    similar_districts_dicts = []
    for district_info in similar_district_names:
        similar_district_dict = {'district_name': district_info[0], 'district_id': district_info[2]}
        similar_districts_dicts.append(similar_district_dict)
    return similar_districts_dicts


def _get_district_dict_suggestions(district_name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} with suggestions for the given
    district name

    Arguments:
        district_name (str): the given district name
    Returns:
        district_dict_suggestions (list[dict]): list of suggested dicts, dict['place_name'] can be None
    """
    district_dict_suggestions = _get_suggestions_for_district_name(district_name)

    for district in district_dict_suggestions:
        place_id = district['district_id'] + "0000000"  # ?
        try:
            place_name = _places_dictionary[place_id]
        except KeyError:
            district['place_name'] = None  # ?
        else:
            district['place_name'] = place_name
        district['place_id'] = place_id
    return district_dict_suggestions


def _get_place_and_district_dict_suggestions(name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} with suggestions for the given
    district or place name

    Arguments:
        name (str): the given name
    Returns:
        dict_suggestions (list[dict]): list of suggested dicts
    """
    district_dict_suggestions = _get_district_dict_suggestions(name)
    place_dict_suggestions = _get_place_dict_suggestions(name)
    for place_dict in place_dict_suggestions:
        for district_dict in district_dict_suggestions:
            if place_dict['place_id'] == district_dict['place_id']:
                district_dict_suggestions.remove(district_dict)
    dict_suggestions = place_dict_suggestions + district_dict_suggestions
    return dict_suggestions


def _get_dicts_for_postal_code(postal_code: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} that fit the place name and
    district id of given postal code (is not 100% accurate)

    Arguments:
        postal_code (str): the given postal code
    Returns:
        place_dict_suggestions (list[dict]): list of dicts with fitting suggested place name and district id
    """
    try:
        record = _postal_code_dictionary[postal_code]
    except KeyError:
        return []  # no postal code found
    else:
        place_name = record[0]
        district_id = record[1]

    unfiltered_place_dict_suggestions = _get_place_dict_suggestions(place_name)
    place_dict_suggestions = []
    for place_dict in unfiltered_place_dict_suggestions:
        if place_dict['district_id'] == district_id:
            place_dict_suggestions.append(place_dict)
    return place_dict_suggestions


def get_name_for_id(given_id: str) -> Any:
    """
       Returns the district or place name of the given ID, if found

       Arguments:
           given_id (str): the given ID of a place or a district
       Returns:
           name (str): the place or district name of the given ID, can be None if not found
       """

    if len(given_id) == 5:
        try:
            district_name = _districts_dictionary[given_id]
        except KeyError:
            return None
        else:
            return district_name
    else:
        try:
            place_name = _places_dictionary[given_id]
        except KeyError:
            return None
        else:
            return place_name


def get_dicts_for_exact_district_name(district_name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} with the given district name

    Arguments:
        district_name (str): the name of the given district
    Returns:
        district_dicts (list[dict]): list of dicts, can be empty
    """
    district_dicts = []
    for district_id in _districts_dictionary.keys():
        if _districts_dictionary[district_id] == district_name:
            place_id = district_id + "0000000"
            try:
                place_name = _places_dictionary[place_id]
            except KeyError:
                place_name = None
            district_dict = {'place_name': place_name, 'place_id': place_id, 'district_name': district_name,
                             'district_id': district_id}
            district_dicts.append(district_dict)
    return district_dicts  # can be empty


def get_dicts_for_exact_place_name(place_name: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} for the exact given place name

    Arguments:
        place_name (str): the given place name
    Returns:
        matching_place_dicts (list[dict]): list of suggested dicts
    """
    matching_place_dicts = []
    for place_id in _places_dictionary.keys():
        if _places_dictionary[place_id] == place_name:
            district_id = place_id[0:5]
            district_name = _districts_dictionary[district_id]
            place_dict = {'place_name': place_name, 'place_id': place_id, 'district_name': district_name,
                          'district_id': district_id}
            matching_place_dicts.append(place_dict)
    return matching_place_dicts


def get_dict_suggestions(given_string: str) -> list[dict]:
    """
    Returns a list of dicts {'place_name', 'place_id', 'district_name', 'district_id'} with suggestions for the given
    district or place name (alphabetic string) or postal code (numeric string)

    Arguments:
        given_string (str): the given name or postal code
    Returns:
        dict_suggestions (list[dict]): list of suggested dicts
    """
    if given_string.isnumeric():
        return _get_dicts_for_postal_code(given_string)
    else:
        return _get_place_and_district_dict_suggestions(given_string)


def get_place_name_from_dict(dictionary: dict) -> Any:
    """
    Returns the place name in a dictionary, if there is one

    Arguments:
        dictionary (dict): the given dictionary
    Returns:
        place_name (str): the place name saved in the dictionary, can be None
    """
    return dictionary['place_name']


def get_place_id_from_dict(dictionary: dict) -> str:
    """
    Returns the place id in a dictionary, if there is one

    Arguments:
        dictionary (dict): the given dictionary
    Returns:
        place_id (str): the place id saved in the dictionary
    """
    return dictionary['place_id']


def get_district_name_from_dict(dictionary: dict) -> str:
    """
    Returns the district name in a dictionary, if there is one

    Arguments:
        dictionary (dict): the given dictionary
    Returns:
        district_name (str): the district name saved in the dictionary
    """
    return dictionary['district_name']


def get_district_id_from_dict(dictionary: dict) -> str:
    """
    Returns the district id in a dictionary, if there is one

    Arguments:
        dictionary (dict): the given dictionary
    Returns:
        district_id (str): the district id saved in the dictionary
    """
    return dictionary['district_id']
