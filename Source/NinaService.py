import requests

baseUrl = "https://warnung.bund.de/api31"


# infos: quelle, infektionsgefahrsstufe, sieben-tage-Inzidenz Kreis und Bundesland, general tips
# regeln: vaccinations, contact_terms, schools_kitas, hostpitals, travelling, fine,
"""
class Covid_Rules:
    def __init__(self, vaccine_info : str, contact_terms : str, school_kita_rules : str, hospital_rules : str, travelling_rules : str, fines : str):
        self.vaccine_info = vaccine_info
        self.contact_terms = contact_terms
        self.school_kita_rules = school_kita_rules
        self.hospital_rules = hospital_rules
        self.travelling_rules = travelling_rules
        self.fines = fines

def get_corona_rules(city_name) -> str:
    #code bekommen wir später, nur dummy
    city_code = "091620000000"

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"
    response = requests.get(baseUrl + coronaInfoAPI + city_code + ".json").json()
    vaccine_info = response["rules"][0]["text"]

    #TODO

    return vaccine_info
"""


class CovidInfos:
    def __init__(self, infektion_danger_level : str, sieben_tage_inzidenz_kreis : str, sieben_tage_inzidenz_bundesland : str, general_tips : str):
        self.infektion_danger_level = infektion_danger_level
        self.sieben_tage_inzidenz_kreis = sieben_tage_inzidenz_kreis
        self.sieben_tage_inzidenz_bundesland = sieben_tage_inzidenz_bundesland
        self.general_tips = general_tips
        pass


def get_covid_infos(city_name) -> CovidInfos:
    #code bekommen wir später, nur dummy
    city_code = "091620000000"

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"
    response = requests.get(baseUrl + coronaInfoAPI + city_code + ".json").json()
    infektion_danger_level = response["level"]["headline"]

    inzidenz_split = str(response["level"]["range"]).split("\n")

    sieben_tage_inzidenz_kreis = inzidenz_split[0]
    sieben_tage_inzidenz_bundesland = inzidenz_split[1]
    general_tips = response["generalInfo"]
    return CovidInfos(infektion_danger_level, sieben_tage_inzidenz_kreis, sieben_tage_inzidenz_bundesland, general_tips)

info = get_covid_infos("")
print(info.general_tips)



#TODO ParseHTML Tags






