from dataclasses import  dataclass
from enum import Enum
import requests
import NinaStringHelper
import NinaPlaces


baseUrl = "https://warnung.bund.de/api31"


# infos: quelle, infektionsgefahrsstufe, sieben-tage-Inzidenz Kreis und Bundesland, general tips
# regeln: vaccinations, contact_terms, schools_kitas, hostpitals, travelling, fine,

@dataclass
class CovidRules:
    vaccine_info: str
    contact_terms: str
    school_kita_rules: str
    hospital_rules: str
    travelling_rules: str
    fines: str

def get_covid_rules(city_name) -> CovidRules:
    city_code = NinaPlaces.get_kreis_id(city_name)
    # der city_code muss 12 Stellig sein, was fehlt muss mit 0en aufgefüllt werden laut doku
    # https://github.com/bundesAPI/nina-api/blob/main/Beispielcode/Python/CoronaZahlenNachGebietscode.py
    city_code = NinaStringHelper.expand_location_id_with_zeros(city_code)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"
    response_raw = requests.get(baseUrl + coronaInfoAPI + city_code + ".json")
    response = response_raw.json()

    vaccine_info = NinaStringHelper.filter_html_tags(response["rules"][0]["text"])
    contact_terms = NinaStringHelper.filter_html_tags(response["rules"][1]["text"])
    school_kita_rules = NinaStringHelper.filter_html_tags(response["rules"][2]["text"])
    hospital_rules = NinaStringHelper.filter_html_tags(response["rules"][3]["text"])
    travelling_rules = NinaStringHelper.filter_html_tags(response["rules"][4]["text"])
    fines = NinaStringHelper.filter_html_tags(response["rules"][5]["text"])

    return CovidRules(vaccine_info, contact_terms, school_kita_rules, hospital_rules, travelling_rules, fines)

@dataclass
class CovidInfos:
    infektion_danger_level: str
    sieben_tage_inzidenz_kreis: str
    sieben_tage_inzidenz_bundesland: str
    general_tips: str


def get_covid_infos(city_name) -> CovidInfos:
    city_code =  NinaPlaces.get_kreis_id(city_name)
    # der city_code muss 12 Stellig sein, was fehlt muss mit 0en aufgefüllt werden laut doku
    # https://github.com/bundesAPI/nina-api/blob/main/Beispielcode/Python/CoronaZahlenNachGebietscode.py
    city_code = NinaStringHelper.expand_location_id_with_zeros(city_code)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    coronaInfoAPI = "/appdata/covid/covidrules/DE/"

    response_raw = requests.get(baseUrl + coronaInfoAPI + city_code + ".json")
    response = response_raw.json()
    infektion_danger_level = response["level"]["headline"]

    inzidenz_split = str(response["level"]["range"]).split("\n")

    sieben_tage_inzidenz_kreis = inzidenz_split[0]
    sieben_tage_inzidenz_bundesland = inzidenz_split[1]
    general_tips = NinaStringHelper.filter_html_tags(response["generalInfo"])
    return CovidInfos(infektion_danger_level, sieben_tage_inzidenz_kreis, sieben_tage_inzidenz_bundesland, general_tips)



class WarningSeverity(Enum):
    Minor = 0
    Moderate = 1
    Severe = 2
    Unkown = 3

class WarningType(Enum):
    Update = 0
    Alert = 1
    Unkown = 2

@dataclass
class GeneralWarning:
    id: str
    version: int
    start_date: str
    severity: WarningSeverity
    type: WarningType
    title: str


def poll_general_warning(api_string : str) -> list[GeneralWarning]:
    response_raw = requests.get(baseUrl + api_string)
    response = response_raw.json()

    print(response_raw.text)

    warning_list = []

    if response is None:
        return warning_list

    for i in range(0, len(list(response))):
        id = response[i]["id"]
        version = response[i]["version"]
        start_date = response[i]["startDate"]

        try:
            severity = WarningSeverity[response[i]["severity"]]
        except KeyError:
            severity = WarningSeverity.Unkown

        try:
            type = WarningType[response[i]["type"]]
        except KeyError:
            type = WarningType.Unkown

        title = response[i]["i18nTitle"]["de"]
        warning_list.append(GeneralWarning(id = id, version= version, start_date= start_date, severity=severity, type= type, title= title))

    return warning_list


def poll_biwapp_warning() -> list[GeneralWarning]:
    biwapp_API = "/biwapp/mapData.json"
    return poll_general_warning(biwapp_API)


def poll_katwarn_warning() -> list[GeneralWarning]:
    katwarn_API = "/katwarn/mapData.json"
    return poll_general_warning(katwarn_API)


def poll_mowas_warning() -> list[GeneralWarning]:
    mowas_API = "/mowas/mapData.json"
    return poll_general_warning(mowas_API)


def poll_dwd_warning() -> list[GeneralWarning]:
    dwd_API = "/dwd/mapData.json"
    return poll_general_warning(dwd_API)


def poll_lhp_warning() -> list[GeneralWarning]:
    lhp_API = "/lhp/mapData.json"
    return poll_general_warning(lhp_API)


def poll_police_warning() -> list[GeneralWarning]:
    police_API = "/police/mapData.json"
    return poll_general_warning(police_API)


"""
warningList = poll_biwapp_warning() #for testing you just need to change which warning method you call here
for warning in warningList:
    print("\n")
    print(warning.id)
    print(warning.version)
    print(warning.severity)
    print(warning.type)
    print(warning.title)
"""









