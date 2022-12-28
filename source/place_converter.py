import requests
from fuzzywuzzy import process


# District => Kreis
# Place => Ort
# Place names are needed for everything besides Covid info
# District names are needed for Covid info
# Kreise haben eine kürzere ID als Orte, wenn sie als Ort benutzt werden sollen, müssen 7 Nullen an ID gehängt werden

def get_district_id(name: str):
    """returns district ID of given place name or district name (both Strings)"""
    if get_district_id_for_district_name(name) is not None:
        return get_district_id_for_district_name(name)
    elif get_district_id_for_place_name(name) is not None:
        return get_district_id_for_place_name(name)
    else:
        raise ValueError('Name not found.')


def get_district_id_for_district_name(district_name: str):
    """returns district ID of given district name (both Strings)"""
    converted_covid_districts = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for district_id in converted_covid_districts.keys():
        if converted_covid_districts[district_id]['n'] == district_name:
            return district_id
    return None  # None, if no district was found


def get_district_id_for_place_name(place_name: str):
    """returns district ID of given place name (both Strings)"""
    district_name = get_district_name_for_place(place_name)
    return get_district_id_for_district_name(district_name)


def get_place_for_postal_code(postal_code: str):
    """returns place name of given postal code (both Strings)"""
    postal_code_table = requests.get(
        'https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q=&rows=-1').json()
    for record in postal_code_table['records']:
        record['fields'].pop('geometry', None)  # removes unimportant fields that take up a lot of space
    for record in postal_code_table['records']:
        if record['fields']['plz_code'] == postal_code:
            return record['fields']['plz_name']
    raise ValueError('Could not find matching postal code.')


def get_district_for_postal_code(postal_code: str):
    """returns district name of given postal code (both Strings)"""
    place = get_place_for_postal_code(postal_code)
    return get_district_name_for_place(place)


def get_similar_names(wrong_name: str):
    """returns a list of similar place and district names, first place then district names"""
    place_names = get_similar_places(wrong_name)
    district_names = get_similar_districts(wrong_name)
    similar_names = place_names + district_names

    if similar_names:
        return similar_names
    else:
        raise ValueError('Could not find similar names.')


def get_similar_districts(wrong_name: str):
    """returns a list of similar district names"""
    converted_covid_districts = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    district_names = [value['n'] for value in converted_covid_districts.values()]
    similar_district_names = process.extract(wrong_name, district_names, limit=10)
    similar_district_names = [x[0] for x in similar_district_names]
    return similar_district_names


def get_similar_places(wrong_name: str):
    """returns a list of similar place names"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']
    place_names = [area_triple[1] for area_triple in area_keys]
    similar_place_names = process.extract(wrong_name, place_names, limit=10)
    similar_place_names = [x[0] for x in similar_place_names]
    return similar_place_names


def get_district_name_for_place(place_name: str):
    """returns district name of given place name"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']
    for area_triple in area_keys:
        if area_triple[1] == place_name:
            place_id = area_triple[0]
            district_id = place_id[:5]  # is this a string?
            return get_district_name(district_id)
    raise ValueError('place name could not be found.')


def get_place_id_for_place_name(place_name: str):
    """returns place ID of given place name"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']
    for area_triple in area_keys:
        if area_triple[1] == place_name:
            return area_triple[0]  # place_id


def get_name_for_id(given_id: str) -> None:
    """returns district or place name of given ID"""
    if get_place_name(given_id) is not None:
        return get_place_name(given_id)
    elif get_district_name(given_id) is not None:
        return get_district_name(given_id)
    else:
        raise ValueError('Could not find ID.')


def get_place_name(place_id: str) -> None:
    """returns place name of given place ID"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']
    for area_triple in area_keys:
        if area_triple[0] == place_id:
            return area_triple[1]
    return None


def get_district_name(district_id: str) -> None:
    """returns district name of given district ID"""
    converted_covid_districts = requests.get(
        'https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for district_ids in converted_covid_districts.keys():
        if district_ids == district_id:
            return converted_covid_districts[district_ids]['n']
    return None
