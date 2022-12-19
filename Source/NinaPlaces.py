import requests
from fuzzywuzzy import process


# District = Kreis
# ? = Ort
# Ortsnamen werden benötigt für alles außer Corona
# Kreisnamen werden für Corona benötigt
# Kreise haben eine kürzere ID als Orte, wenn sie als Ort benutzt werden sollen, müssen 7 Nullen an ID gehängt werden
# Bsp Kreis: ID:
# Bsp Ort: ID:
def get_kreis_id(name):
    """returns Kreis-ID of given Ort-Name or Kreis-Name"""
    if get_kreis_id_for_kreis(name) is not None:
        return get_kreis_id_for_kreis(name)
    elif get_kreis_id_for_ort(name) is not None:
        return get_kreis_id_for_ort(name)
    else:
        raise ValueError('Name not found.')


def get_kreis_id_for_kreis(kreis_name):
    """returns Kreis-ID of given Kreis-Name"""
    converted_corona_kreise = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for kreis_id in converted_corona_kreise.keys():
        if converted_corona_kreise[kreis_id]['n'] == kreis_name:
            return kreis_id
    return None  # wenn None, dann kein Kreis


def get_kreis_id_for_ort(ort_name):
    """returns Kreis-ID of given Ort-Name"""
    kreis_name = get_kreisname_for_ort(ort_name)
    return get_kreis_id_for_kreis(kreis_name)


def get_ort_for_plz(plz):
    """returns Ort-Name of given Postleitzahl (both Strings)"""
    plz_table = requests.get(
        'https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q=&rows=-1').json()
    for record in plz_table['records']:
        if record['fields']['plz_code'] == plz:
            return record['fields']['plz_name']
    raise ValueError('Could not find matching PLZ.')


def get_kreis_for_plz(plz):
    """returns Kreis-Name of given Postleitzahl (both Strings)"""
    ort = get_ort_for_plz(plz)
    return get_kreisname_for_ort(ort)


def get_similar_names(wrong_name):
    """returns a list of similar Ort- and Kreis-Names, first Ort- then Kreis-Names"""
    ort_names = get_similar_orte(wrong_name)
    kreis_names = get_similar_kreise(wrong_name)
    similar_names = ort_names + kreis_names

    if similar_names:
        return similar_names
    else:
        raise ValueError('Could not find similar names.')


def get_similar_kreise(wrong_name):
    """returns a list of similar Kreis-Names"""
    converted_corona_kreise = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    kreis_names = [value['n'] for value in converted_corona_kreise.values()]
    similar_kreis_names = process.extract(wrong_name, kreis_names, limit=10)
    similar_kreis_names = [x[0] for x in similar_kreis_names]
    return similar_kreis_names


def get_similar_orte(wrong_name):
    """returns a list of similar Ort-Names"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']
    ort_names = [area_triple[1] for area_triple in area_keys]
    similar_ort_names = process.extract(wrong_name, ort_names, limit=10)
    similar_ort_names = [x[0] for x in similar_ort_names]
    return similar_ort_names


def get_kreisname_for_ort(ort_name):
    """returns Kreis-Name of given Ort-Name"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']

    for area_triple in area_keys:
        if area_triple[1] == ort_name:
            ort_id = area_triple[0]
            kreis_id = ort_id[:5]  # ist das wirklich ein string?
            return get_kreisname(kreis_id)

    raise ValueError('Ort-Name could not be found.')


def get_ort_id_for_ort(ort_name):
    """returns Ort-ID of given Ort-Name"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']

    for area_triple in area_keys:
        if area_triple[1] == ort_name:
            return area_triple[0]  # ort_id


def get_name_for_id(given_id):
    """returns Kreis- or Ort-Name of given ID"""
    if get_ortsname(given_id) is not None:
        return get_ortsname(given_id)
    elif get_kreisname(given_id) is not None:
        return get_kreisname(given_id)
    else:
        raise ValueError('Could not find ID.')


def get_ortsname(ort_id):
    """returns Ort-Name of given Ort-ID"""
    bevoelkerungsstaat_key = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    area_keys = bevoelkerungsstaat_key['daten']

    for area_triple in area_keys:
        if area_triple[0] == ort_id:
            return area_triple[1]

    return None


def get_kreisname(kreis_id):
    """returns Kreis-Name of given Kreis-ID"""
    converted_corona_kreise = requests.get(
        'https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for kreis_ids in converted_corona_kreise.keys():
        if kreis_ids == kreis_id:
            return converted_corona_kreise[kreis_ids]['n']

    return None
