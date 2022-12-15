import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Ortsnamen werden benötigt für alles außer Corona
# Kreisnamen werden für Corona benötigt
# Kreise haben eine kürzere ID als Orte, wenn sie als Ort benutzt werden sollen, müssen 7 Nullen an ID gehängt werden
# Bsp Kreis: ID:
# Bsp Ort: ID:
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


def get_ort_for_plz(plz):
    plz_table = requests.get('https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany'
                             '-postleitzahl&q=&facet=plz_name&facet=lan_name&facet=lan_code').json()


def get_similar_names(wrong_name):
    """Gibt ähnliche Ort- und Kreisnamen zurück, zuerst Orte dann Kreise"""
    orte = get_similar_orte(wrong_name)
    kreise = get_similar_kreise(wrong_name)
    similar_names = orte + kreise

    if similar_names:
        return similar_names
    else:
        raise ValueError('Keine ähnlichen Namen gefunden.')


def get_similar_kreise(wrong_name):
    """Gibt ähnliche Kreisnamen zurück"""
    converted_corona_kreise = requests.get('https://warnung.bund.de/assets/json/converted_corona_kreise.json').json()
    kreisnamen = [value['n'] for value in converted_corona_kreise.values()]
    similar_kreise = process.extract(wrong_name, kreisnamen, limit=10)
    similar_kreise = [x[0] for x in similar_kreise]
    return similar_kreise


def get_similar_orte(wrong_name):
    """Gibt ähnliche Ortnamen zurück"""
    bevoelkerungsstaat_schluessel = requests.get(
        'https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07'
        '-31/download/Regionalschl_ssel_2021-07-31.json').json()
    gebiete_schluessel = bevoelkerungsstaat_schluessel['daten']
    ortnamen = [gebiets_tripel[1] for gebiets_tripel in gebiete_schluessel]

    # without_stadt = []
    # for ort in ortnamen:
    #   ort = ort.replace(', Stadt', '')
    #   ort = ort.replace(', Landeshauptstadt', '')
    #   ort = ort.replace(', Wissenschaftsstadt', '')
    #   without_stadt.append(ort)

    similar_orte = process.extract(wrong_name, ortnamen, limit=10)
    similar_orte = [x[0] for x in similar_orte]
    return similar_orte


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
            kreisname_id = ortsname_id[:5]  # ist das wirklich ein string?!
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
