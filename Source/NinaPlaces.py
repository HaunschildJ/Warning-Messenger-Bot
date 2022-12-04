import requests


def get_kreis_id(name):
    """gibt Kreis-id von Ortsname oder Kreisname zurück"""

    if get_kreis_id_for_kreis(name) is not None:
        return get_kreis_id_for_kreis(name)
    elif get_kreis_id_for_ort(name) is not None:
        return get_kreis_id_for_ort(name)
    else:
        raise ValueError('Name nicht gefunden.')


def get_kreis_id_for_kreis(kreisname):
    """gibt Kreis-id von Kreis zurück"""
    converted_corona_kreise = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for kreis_id in converted_corona_kreise.keys():
        if converted_corona_kreise[kreis_id]['n'] == kreisname:
            return kreis_id

    return None  # wenn None, dann kein Kreis


def get_kreis_id_for_ort(ortsname):
    """gibt Kreis-id von Ort zurück"""
    kreisname = get_kreisname_for_ort(ortsname)
    return get_kreis_id_for_kreis(kreisname)


def get_kreisname_for_ort(ortsname):
    """gibt Kreisname von Ort zurück"""
    # ! wenn stadt, dann steht da name, Stadt
    bevoelkerungsstat_schluessel = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    gebiete_schluessel = bevoelkerungsstat_schluessel['daten']

    for gebiets_tripel in gebiete_schluessel:
        if gebiets_tripel[1] == ortsname:
            ortsname_id = gebiets_tripel[0]
            kreisname_id = ortsname_id[:5] # ist das wirklich ein string?!
            return get_kreisname(kreisname_id)

    raise ValueError('Ortsname konnte nicht gefunden werden.')


def get_ort_id_for_ort(ortsname):
    bevoelkerungsstat_schluessel = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    gebiete_schluessel = bevoelkerungsstat_schluessel['daten']

    for gebiets_tripel in gebiete_schluessel:
        if gebiets_tripel[1] == ortsname:
            return gebiets_tripel[0]  # ort_id


def get_name(name_id):
    """gibt Kreis- oder Ortsname von id zurück"""
    if get_ortsname(name_id) is not None:
        return get_ortsname(name_id)
    elif get_kreisname(name_id) is not None:
        return get_kreisname(name_id)
    else:
        raise ValueError('id nicht gefunden.')


def get_ortsname(ort_id):
    """gibt Ortsname von id zurück"""
    bevoelkerungsstat_schluessel = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    gebiete_schluessel = bevoelkerungsstat_schluessel['daten']

    for gebiets_tripel in gebiete_schluessel:
        if gebiets_tripel[0] == ort_id:
            return gebiets_tripel[1]

    return None


def get_kreisname(kreis_id):
    """gibt Kreisname von id zurück"""
    converted_corona_kreise = requests.get(
        'https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    for kreis_ids in converted_corona_kreise.keys():
        if kreis_ids == kreis_id:
            return converted_corona_kreise[kreis_ids]['n']

    return None
