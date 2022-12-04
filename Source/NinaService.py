import requests
import NinaStringHelper
import NinaPlaces

baseUrl = "https://warnung.bund.de/api31"


# infos: quelle, infektionsgefahrsstufe, sieben-tage-Inzidenz Kreis und Bundesland, general tips
# regeln: vaccinations, contact_terms, schools_kitas, hostpitals, travelling, fine,

class Covid_Rules:
    def __init__(self, vaccine_info : str, contact_terms : str, school_kita_rules : str, hospital_rules : str, travelling_rules : str, fines : str):
        self.vaccine_info = vaccine_info
        self.contact_terms = contact_terms
        self.school_kita_rules = school_kita_rules
        self.hospital_rules = hospital_rules
        self.travelling_rules = travelling_rules
        self.fines = fines

def get_covid_rules(city_name) -> Covid_Rules:
    city_code = NinaPlaces.get_kreis_id(city_name)
    # der city_code muss 12 Stellig sein, was fehlt muss mit 0en aufgefüllt werden laut doku
    # https://github.com/bundesAPI/nina-api/blob/main/Beispielcode/Python/CoronaZahlenNachGebietscode.py
    city_code = NinaStringHelper.expand_location_id_with_zeros(city_code)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"
    responseRaw = requests.get(baseUrl + coronaInfoAPI + city_code + ".json")
    response = responseRaw.json()

    vaccine_info = NinaStringHelper.filter_html_tags(response["rules"][0]["text"])
    contact_terms = NinaStringHelper.filter_html_tags(response["rules"][1]["text"])
    school_kita_rules = NinaStringHelper.filter_html_tags(response["rules"][2]["text"])
    hospital_rules = NinaStringHelper.filter_html_tags(response["rules"][3]["text"])
    travelling_rules = NinaStringHelper.filter_html_tags(response["rules"][4]["text"])
    fines = NinaStringHelper.filter_html_tags(response["rules"][5]["text"])

    return Covid_Rules(vaccine_info, contact_terms, school_kita_rules, hospital_rules, travelling_rules, fines)



class CovidInfos:
    def __init__(self, infektion_danger_level : str, sieben_tage_inzidenz_kreis : str, sieben_tage_inzidenz_bundesland : str, general_tips : str):
        self.infektion_danger_level = infektion_danger_level
        self.sieben_tage_inzidenz_kreis = sieben_tage_inzidenz_kreis
        self.sieben_tage_inzidenz_bundesland = sieben_tage_inzidenz_bundesland
        self.general_tips = general_tips



def get_covid_infos(city_name) -> CovidInfos:

    city_code =  NinaPlaces.get_kreis_id(city_name)
    # der city_code muss 12 Stellig sein, was fehlt muss mit 0en aufgefüllt werden laut doku
    # https://github.com/bundesAPI/nina-api/blob/main/Beispielcode/Python/CoronaZahlenNachGebietscode.py
    city_code = NinaStringHelper.expand_location_id_with_zeros(city_code)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"

    responseRaw = requests.get(baseUrl + coronaInfoAPI + city_code + ".json")
    response = responseRaw.json()
    infektion_danger_level = response["level"]["headline"]

    inzidenz_split = str(response["level"]["range"]).split("\n")

    sieben_tage_inzidenz_kreis = inzidenz_split[0]
    sieben_tage_inzidenz_bundesland = inzidenz_split[1]
    general_tips = NinaStringHelper.filter_html_tags(response["generalInfo"])
    return CovidInfos(infektion_danger_level, sieben_tage_inzidenz_kreis, sieben_tage_inzidenz_bundesland, general_tips)










