from dataclasses import  dataclass
from enum import Enum
import requests
import NinaStringHelper
import NinaPlaces


baseUrl = "https://warnung.bund.de/api31"


# infos: quelle, infektionsgefahrsstufe, sieben-tage-Inzidenz Kreis und Bundesland, general tips
# regeln: vaccinations, contact_terms, schools_kitas, hostpitals, travelling, fine,

@dataclass
class Covid_Rules:
    vaccine_info: str
    contact_terms: str
    school_kita_rules: str
    hospital_rules: str
    travelling_rules: str
    travelling_rules: str
    fines: str

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

    responseRaw = requests.get(baseUrl + coronaInfoAPI + city_code + ".json")
    response = responseRaw.json()
    infektion_danger_level = response["level"]["headline"]

    inzidenz_split = str(response["level"]["range"]).split("\n")

    sieben_tage_inzidenz_kreis = inzidenz_split[0]
    sieben_tage_inzidenz_bundesland = inzidenz_split[1]
    general_tips = NinaStringHelper.filter_html_tags(response["generalInfo"])
    return CovidInfos(infektion_danger_level, sieben_tage_inzidenz_kreis, sieben_tage_inzidenz_bundesland, general_tips)



class WarningSeverity(Enum):
    Severe = 1

class WarningType(Enum):
    Alert = 1

@dataclass
class General_Warning:
    id: str;
    version: int;
    severity: WarningSeverity;
    type: WarningType;
    title: str;


def poll_biwapp_warning() -> list[General_Warning]:
    kat_warn_API = "/biwapp/mapData.json"
    responseRaw = requests.get(baseUrl + kat_warn_API)
    response = responseRaw.json()

    warningList = []

    if (response is None):
        return warningList

    for i in range(0, len(list(response))):
        id = response[i]["id"]
        version = response[i]["version"]
        severity = WarningSeverity.Severe
        type = WarningType.Alert
        title = response[i]["i18nTitle"]["de"]
        warningList.append(General_Warning(id = id, version= version,severity=severity, type= type, title= title))

    return warningList

"""
warningList = poll_biwapp_warning()

print(warningList[0].id)
print(warningList[0].version)
print(warningList[0].severity)
print(warningList[0].type)
print(warningList[0].title)
"""

















