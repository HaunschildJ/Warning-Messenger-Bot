from dataclasses import dataclass
from enum import Enum
from datetime import datetime
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
    covid_info_API = "/appdata/covid/covidrules/DE/"
    response_raw = requests.get(baseUrl + covid_info_API + city_code + ".json")
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
    city_code = NinaPlaces.get_kreis_id(city_name)
    # der city_code muss 12 Stellig sein, was fehlt muss mit 0en aufgefüllt werden laut doku
    # https://github.com/bundesAPI/nina-api/blob/main/Beispielcode/Python/CoronaZahlenNachGebietscode.py
    city_code = NinaStringHelper.expand_location_id_with_zeros(city_code)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    covid_info_API = "/appdata/covid/covidrules/DE/"

    response_raw = requests.get(baseUrl + covid_info_API + city_code + ".json")
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


def _get_warning_severity(severity: str) -> WarningSeverity:
    try:
        return WarningSeverity[severity]
    except KeyError:
        return WarningSeverity.Unkown


class WarningType(Enum):
    Update = 0
    Alert = 1
    Unkown = 2


def _get_warning_type(type: str) -> WarningType:
    try:
        return WarningType[type]
    except KeyError:
        return WarningType.Unkown


@dataclass
class GeneralWarning:
    id: str
    version: int
    start_date: str
    severity: WarningSeverity
    type: WarningType
    title: str


def _translate_time(nina_time: str) -> str:
    dt = datetime.fromisoformat(nina_time)

    # Convert the datetime object to a string in a specific format
    normal_time_string = dt.strftime("%Y-%m-%d %I:%M")
    return normal_time_string


def _poll_general_warning(api_string: str) -> list[GeneralWarning]:
    response_raw = requests.get(baseUrl + api_string)
    response = response_raw.json()

    warning_list = []

    if response is None:
        return warning_list

    for i in range(0, len(list(response))):
        id = response[i]["id"]
        version = response[i]["version"]

        start_date = _translate_time(response[i]["startDate"])

        severity = _get_warning_severity(response[i]["severity"])
        type = _get_warning_type(response[i]["type"])
        title = response[i]["i18nTitle"]["de"]
        warning_list.append(
            GeneralWarning(id=id, version=version, start_date=start_date, severity=severity, type=type, title=title))

    return warning_list


def poll_biwapp_warning() -> list[GeneralWarning]:
    biwapp_API = "/biwapp/mapData.json"
    return _poll_general_warning(biwapp_API)


def poll_katwarn_warning() -> list[GeneralWarning]:
    katwarn_API = "/katwarn/mapData.json"
    return _poll_general_warning(katwarn_API)


def poll_mowas_warning() -> list[GeneralWarning]:
    mowas_API = "/mowas/mapData.json"
    return _poll_general_warning(mowas_API)


def poll_dwd_warning() -> list[GeneralWarning]:
    dwd_API = "/dwd/mapData.json"
    return _poll_general_warning(dwd_API)


def poll_lhp_warning() -> list[GeneralWarning]:
    lhp_API = "/lhp/mapData.json"
    return _poll_general_warning(lhp_API)


def poll_police_warning() -> list[GeneralWarning]:
    police_API = "/police/mapData.json"
    return _poll_general_warning(police_API)

"""
warningList = poll_biwapp_warning()  # for testing you just need to change which warning method you call here
for warning in warningList:
    print("\n")
    print(warning.id)
    print(warning.version)
    print(warning.severity)
    print(warning.type)
    print(warning.title)
    print(warning.start_date)
"""

@dataclass
class DetailedWarningInfoArea:
    area_description: str
    geocode: list[str]


@dataclass
class DetailedWarningInfo:
    event: str  # noch keine Ahnung was das sein soll
    severity: WarningSeverity
    date_expires: str
    headline: str
    description: str
    area: list[DetailedWarningInfoArea]


@dataclass
class DetailedWarning:
    id: str
    sender: str
    date_sent: str
    status: str
    infos: list[DetailedWarningInfo]


def _get_detailed_warning_infos_area_geocode(response_geocode) -> list[str]:
    geocode = []
    if response_geocode is None:
        return geocode

    for i in range(0, len(response_geocode)):
        geocode.append(response_geocode[i]["value"])

    return  geocode

def _get_detailed_warning_infos_area(response_area) -> list[DetailedWarningInfoArea]:
    area = []
    if response_area is None:
        return area

    for i in range(0, len(response_area)):
        area_description = response_area[i]["areaDesc"]
        geocode = _get_detailed_warning_infos_area_geocode(response_area[i]["geocode"])
        area.append(
            DetailedWarningInfoArea(area_description=area_description, geocode=geocode)
        )

    return  area

def _get_detailed_warning_infos(response_infos) -> list[DetailedWarningInfo]:
    infos = []
    if response_infos is None:
        return  infos

    for i in range(0, len(response_infos)):
        event = response_infos[i]["event"]
        severity = _get_warning_severity(response_infos[i]["severity"])
        date_expires = _translate_time(response_infos[i]["expires"])
        headline = response_infos[i]["headline"]
        description = NinaStringHelper.filter_html_tags(response_infos[i]["description"])
        area = _get_detailed_warning_infos_area(response_infos[i]["area"])

        infos.append(
            DetailedWarningInfo(event=event, severity=severity, date_expires=date_expires, headline=headline,
                                description=description, area=area)
        )

    return  infos

def get_detailed_warning(warning_id: str):
    """
    This method should be called after a warning with one of the poll_****_warning methods was received
    :param warning_id: warning id is extracted from the poll_****_warning method return type: GeneralWarning.id
    :return:
    """
    response_raw = requests.get(baseUrl + "/warnings/" + warning_id + ".json")
    response = response_raw.json()
    print(response_raw.text)

    id = response["identifier"]
    sender = response["sender"]
    date_sent = _translate_time(response["sent"])
    status = response["status"]
    infos = _get_detailed_warning_infos(response["info"])

    return DetailedWarning(id=id, sender=sender, date_sent=date_sent, status=status, infos=infos)





"""
warning = poll_biwapp_warning()[0] #for testing the individual warning method needs to return a warning (not always the case, just iterate through biwap, katwarn, police, etc...)
warning = get_detailed_warning(warning.id)
print(warning.id)
print(warning.status)
print(warning.sender)
print(warning.date_sent)
print("INFOS: ")
for i in range(0, len(warning.infos)):
    print("\t"+warning.infos[i].event)
    print("\t"+warning.infos[i].severity.name)
    print("\t"+warning.infos[i].date_expires)
    print("\t"+warning.infos[i].headline)
    print("\t"+warning.infos[i].description)
    print("\tAREA: ")
    for j in range(0, len(warning.infos[i].area)):
        print("\t\t"+ warning.infos[i].area[i].area_description)
        for l in range(0, len(warning.infos[i].area[j].geocode)):
            print ("\t\tGEOCODE:")
            print("\t\t\t"+ warning.infos[i].area[i].geocode[l])
"""