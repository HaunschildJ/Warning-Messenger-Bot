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
"""dictionary place_name : str -> place_id : str"""


def _fill_districts_dict() -> None:
    """
    Fills the _districts_dictionary dictionary with selected infos from https://warnung.bund.de/assets/json/converted_corona_kreise.json
    Format: district_key -> district_name
    """
    converted_covid_districts = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for district_id, district_description in converted_covid_districts.items():
        _districts_dictionary[district_id] = district_description["n"]


_fill_districts_dict()


def _fill_places_dict() -> None:
    """
    Fills the _places_dictionary dictionary with selected infos from
    https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31
    /download/Regionalschl_ssel_2021-07-31.json
    Format: place_name -> place_key
    """
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    for area_triple in bevoelkerungsstaat_key['daten']:
        _places_dictionary[area_triple[1]] = area_triple[0]


_fill_places_dict()


def get_district_id(name: str) -> str:
    """
    Returns the district ID of the given place name or district name

    Arguments:
        name (str): the name of the given district or place
    Returns:
        district_id (str): the ID of the given district or place name, if found
    """
    id_for_district = get_district_id_for_district_name(name)
    id_for_place = get_district_id_for_place_name(name)

    if id_for_district is not None:
        return id_for_district
    elif id_for_place is not None:
        return id_for_place
    else:
        raise ValueError('Name not found.')


def get_district_id_for_district_name(district_name: str) -> str:
    """
    Returns the district ID of the given district name

    Arguments:
        district_name (str): the name of the given district
    Returns:
        district_id (str): the ID of the given district name, if found
    """
    for district_id in _districts_dictionary.keys():
        if _districts_dictionary[district_id] == district_name:
            return district_id
    return None  # None, if no district was found


def get_district_id_for_place_name(place_name: str) -> str:
    """
    Returns the district ID of the given place name

    Arguments:
        place_name (str): the name of the given place
    Returns:
        district_id (str): the ID of the given place name, if found
    """
    district_name = get_district_name_for_place(place_name)  # TODO CHECK FOR ERROR BEFORE USING IT IN THE NEXT METHOD
    return get_district_id_for_district_name(district_name)


def get_place_for_postal_code(postal_code: str) -> str:
    """
    Returns the place name of the given postal code

    Arguments:
        postal_code (str): the given postal code
    Returns:
        place_name (str): the place name of the given postal code, if found
    """
    postal_code_table = requests.get(
        'https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q=&rows=-1').json()
    for record in postal_code_table['records']:
        record['fields'].pop('geometry', None)  # removes unimportant fields that take up a lot of space
    for record in postal_code_table['records']:
        if record['fields']['plz_code'] == postal_code:
            return record['fields']['plz_name']
    raise ValueError('Could not find matching postal code.')


def get_district_for_postal_code(postal_code: str) -> str:
    """
    Returns district name of given postal code

    Arguments:
        postal_code (str): the given postal code
    Returns:
        district_name (str): the district name of the given postal code, if found
    """
    place = get_place_for_postal_code(postal_code)  # TODO CHECK FOR ERROR BEFORE USING IT IN THE NEXT METHOD
    return get_district_name_for_place(place)


def get_similar_names(wrong_name: str) -> list:
    """
    Returns a list of similar place and district names, first place then district names

    Arguments:
        wrong_name (str): the given name to find similarities with
    Returns:
        similar_names (list): list of similar place and district names, if found
    """
    place_names = get_similar_places(wrong_name)
    district_names = get_similar_districts(wrong_name)
    similar_names = place_names + district_names

    if similar_names:
        return similar_names
    else:
        raise ValueError('Could not find similar names.')


def get_similar_districts(wrong_name: str) -> list:
    """
    Returns a list of similar district names

    Arguments:
        wrong_name (str): the given name to find similarities with
    Returns:
        similar_district_names (list): list of similar district names
    """
    district_names = _districts_dictionary.values()
    similar_district_names = process.extract(wrong_name, district_names, limit=10)
    similar_district_names = [x[0] for x in similar_district_names]
    return similar_district_names


def get_similar_places(wrong_name: str) -> list:
    """
    Returns a list of similar place names

    Arguments:
        wrong_name (str): the given name to find similarities with
    Returns:
        similar_place_names (list): list of similar place names
    """
    place_names = _places_dictionary.keys()
    similar_place_names = process.extract(wrong_name, place_names, limit=10)
    similar_place_names = [x[0] for x in similar_place_names]
    return similar_place_names


def get_district_name_for_place(place_name: str) -> str:
    """
    Returns the district name of the given place name

    Arguments:
        place_name (str): the name of the given place
    Returns:
        district_name (str): the district name of the given place name, if found
    """
    if _places_dictionary[place_name]:
        place_id = _places_dictionary[place_name]
        district_id = place_id[:5]
        return get_district_name(district_id)
    raise ValueError('place name could not be found.')


def get_place_id_for_place_name(place_name: str) -> str:
    """
    Returns the place ID name of the given place name

    Arguments:
        place_name (str): the name of the given place
    Returns:
        place_id (str): the place ID of the given place name, if found
    """
    place_id = _places_dictionary[place_name]
    if place_id:
        return place_id  # place_id
    raise ValueError('place name could not be found.')


def get_name_for_id(given_id: str) -> str:
    """
       Returns the district or place name of the given ID

       Arguments:
           given_id (str): the given ID of a place or a district
       Returns:
           name (str): the place or district name of the given ID, if found
       """

    place_name = get_place_name(given_id)
    if len(given_id) is 5:
        district_name = get_district_name(given_id)
    else:
        district_name = None

    if place_name is not None:
        return place_name
    elif district_name is not None:
        return district_name
    else:
        raise ValueError('Could not find ID.')


def get_place_name(place_id: str) -> str:
    """
       Returns the place name of the given ID

       Arguments:
           place_id (str): the given ID of a place or a district
       Returns:
           place_name (str): the place name of the given ID, if found
       """

    for place_name in _places_dictionary:
        if _places_dictionary[place_name] == place_id:
            return place_name
    return None


def get_district_name(district_id: str) -> str:
    """
        Returns the district name of the given district ID

        Arguments:
            district_id (str): the given district ID of a district
        Returns:
            district_name (str): the district name of the given ID, if found
        """
    district_name = _districts_dictionary[district_id]
    if district_name:
        return district_name
    return None
