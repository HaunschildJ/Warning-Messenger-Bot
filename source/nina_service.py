from dataclasses import dataclass
from datetime import datetime
from typing import List

from enum_types import WarningSeverity
from enum_types import WarnType
from enum_types import WarningType

import requests
import nina_string_helper

_BASE_URL = "https://warnung.bund.de/api31"


@dataclass
class CovidRules:
    vaccine_info: str
    contact_terms: str
    school_kita_rules: str
    hospital_rules: str
    travelling_rules: str
    fines: str


def _get_safely(dict, key: str):
    """
    Because some JSONs we get from the NINA API do not always contain all the fields that are defined by the NINA API
    we need to check if the field exists first. If it does, we get the Value from the field. If it does not we return None
    :param dict: The dictionary to check the key in
    :param key:  The kay of the field   for example: "fines" for CovidRules { "fines": "bla bla", }
    :return: None if the key is not in the dictionary, Value of the key if it is
    """
    try:
        return dict[key]
    except KeyError:
        return None


def get_covid_rules(district_id: str) -> CovidRules:
    """
    Gets current covid rules from the NinaApi for a city and returns them as a CovidRules class
    If the city_name is not valid, an indirect ValueError is thrown (forwarded from place_converter)
    :param district_id: Each district may have different covid_rules
    :return: CovidRules class
    :raises HTTPError:
    """
    district_id = nina_string_helper.expand_location_id_with_zeros(district_id)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    covid_info_api = "/appdata/covid/covidrules/DE/"
    response_raw = requests.get(_BASE_URL + covid_info_api + district_id + ".json")

    response = response_raw.json()

    vaccine_info = nina_string_helper.filter_html_tags(response["rules"][0]["text"])
    contact_terms = nina_string_helper.filter_html_tags(response["rules"][1]["text"])
    school_kita_rules = nina_string_helper.filter_html_tags(response["rules"][2]["text"])
    hospital_rules = nina_string_helper.filter_html_tags(response["rules"][3]["text"])
    travelling_rules = nina_string_helper.filter_html_tags(response["rules"][4]["text"])
    fines = nina_string_helper.filter_html_tags(response["rules"][5]["text"])

    return CovidRules(vaccine_info, contact_terms, school_kita_rules, hospital_rules, travelling_rules, fines)


@dataclass
class CovidInfo:
    infektionsgefahr_stufe: str
    sieben_tage_inzidenz_kreis: str
    sieben_tage_inzidenz_bundesland: str
    allgemeine_hinweise: str


def get_covid_infos(district_id: str) -> CovidInfo:
    """
    Gets current covid infos from the NinaApi for a certain city and returns them as a CovidInfo class
    If the city_name is not valid, an indirect ValueError is thrown (forwarded from place_converter)
    :param district_id:
    :return: CovidInfo class
    :raises HTTPError:
    """
    district_id = nina_string_helper.expand_location_id_with_zeros(district_id)

    # aktuelle Coronameldungen abrufen nach Gebietscode
    covid_info_api = "/appdata/covid/covidrules/DE/"

    response_raw = requests.get(_BASE_URL + covid_info_api + district_id + ".json")
    response = response_raw.json()
    infektion_danger_level = response["level"]["headline"]

    inzidenz_split = str(response["level"]["range"]).split("\n")

    sieben_tage_inzidenz_kreis = inzidenz_split[0]
    sieben_tage_inzidenz_bundesland = inzidenz_split[1]
    general_tips = nina_string_helper.filter_html_tags(response["generalInfo"])
    return CovidInfo(infektion_danger_level, sieben_tage_inzidenz_kreis, sieben_tage_inzidenz_bundesland, general_tips)


def _get_warning_severity(warn_severity: str) -> WarningSeverity:
    """
    translates a string into an enum of WarningSeverity
    :param warn_severity: the exact Enum as a String, for example: "Minor" <- valid
    :return: if the string is a valid enum, the enum if not: WarningSeverity.MINOR
    """
    try:
        return WarningSeverity(warn_severity)
    except KeyError:
        return WarningSeverity.MINOR


def _get_warning_type(warn_type: str) -> WarningType:
    """
    translates a string into an enum of WarningType
    :param warn_type: the exact Enum as a String, for example: "Minor" <- valid  " Minor" <- returns WarningType.Unknown
    :return: if the string is a valid enum, the enum if not: WarningType.Unknown
    """
    try:
        return WarningType[warn_type]
    except KeyError:
        return WarningType.Unknown


@dataclass
class GeneralWarning:
    id: str
    version: int
    start_date: str
    severity: WarningSeverity
    type: WarningType
    title: str


def _translate_time(nina_time: str) -> str:
    """
    translates the time strings we get from the nina api answers to actually readable times
    :param nina_time: time string we get from nina api
    :return: string in a readable format year-month-day hour:minute
    """
    dt = datetime.fromisoformat(nina_time)

    # Convert the datetime object to a string in a specific format
    normal_time_string = dt.strftime("%Y-%m-%d %I:%M")
    return normal_time_string


def _poll_general_warning(api_string: str) -> list[GeneralWarning]:
    """
    biwapp, katwarn, mowas, dwd, lhp and police-warnings are all generally the same
    this is the general method to poll those
    :param api_string: the string for the exact api we poll for
    :return: a list of all warnings that are actual. An empty list is returned if there are none
    :raises HTTPError:
    """
    response_raw = requests.get(_BASE_URL + api_string)
    response = response_raw.json()

    warning_list = []

    if response is None:
        return warning_list

    for i in range(0, len(list(response))):
        id_response = response[i]["id"]
        version = response[i]["version"]

        start_date = _translate_time(response[i]["startDate"])

        severity = _get_warning_severity(response[i]["severity"])
        response_type = _get_warning_type(response[i]["type"])
        title = response[i]["i18nTitle"]["de"]
        warning_list.append(GeneralWarning(id=id_response, version=version, start_date=start_date, severity=severity,
                                           type=response_type, title=title))

    return warning_list


def poll_biwapp_warning() -> list[GeneralWarning]:
    """
    polls the current biwap warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    biwapp_api = "/biwapp/mapData.json"
    return _poll_general_warning(biwapp_api)


def poll_katwarn_warning() -> list[GeneralWarning]:
    """
    polls the current katwarn warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    katwarn_api = "/katwarn/mapData.json"
    return _poll_general_warning(katwarn_api)


def poll_mowas_warning() -> list[GeneralWarning]:
    """
    polls the current mowas warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    mowas_api = "/mowas/mapData.json"
    return _poll_general_warning(mowas_api)


def poll_dwd_warning() -> list[GeneralWarning]:
    """
    polls the current dwd warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    dwd_api = "/dwd/mapData.json"
    return _poll_general_warning(dwd_api)


def poll_lhp_warning() -> list[GeneralWarning]:
    """
    polls the current lhp warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    lhp_api = "/lhp/mapData.json"
    return _poll_general_warning(lhp_api)


def poll_police_warning() -> list[GeneralWarning]:
    """
    polls the current police warnings
    :return: a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    police_api = "/police/mapData.json"
    return _poll_general_warning(police_api)


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
        geocode.append(_get_safely(response_geocode[i], "value"))

    return geocode


def _get_detailed_warning_infos_area(response_area) -> list[DetailedWarningInfoArea]:
    area = []
    if response_area is None:
        return area

    for i in range(0, len(response_area)):
        area_description = _get_safely(response_area[i], "areaDesc")
        geocode = _get_detailed_warning_infos_area_geocode(_get_safely(response_area[i], "geocode"))
        area.append(
            DetailedWarningInfoArea(area_description=area_description, geocode=geocode)
        )

    return area


def _get_detailed_warning_infos(response_infos) -> list[DetailedWarningInfo]:
    infos = []
    if response_infos is None:
        return infos

    for i in range(0, len(response_infos)):
        info = response_infos[i]

        event = _get_safely(info, "event")
        severity = _get_warning_severity(_get_safely(info, "severity"))
        headline = _get_safely(info, "headline")
        description = nina_string_helper.filter_html_tags(_get_safely(info, "description"))
        area = _get_detailed_warning_infos_area(_get_safely(info, "area"))

        date_expires = _get_safely(info, "expires")
        if date_expires is not None:
            date_expires = _translate_time(date_expires)

        infos.append(
            DetailedWarningInfo(event=event, severity=severity, date_expires=date_expires, headline=headline,
                                description=description, area=area)
        )

    return infos


def get_detailed_warning(warning_id: str) -> DetailedWarning:
    """
    This method should be called after a warning with one of the poll_****_warning methods was received
    :param warning_id: warning id is extracted from the poll_****_warning method return type: GeneralWarning.id
    :return: the detailed Warning as a DetailedWarning class
    :raises HTTPError:
    """
    response_raw = requests.get(_BASE_URL + "/warnings/" + warning_id + ".json")
    response = response_raw.json()

    id_response = _get_safely(response, "identifier")
    sender = _get_safely(response, "sender")
    status = _get_safely(response, "status")

    date_sent = _get_safely(response, "sent")
    if date_sent is not None:
        date_sent = _translate_time(date_sent)

    # _get_detailed_warning_infos already checks if the input is None
    infos = _get_detailed_warning_infos(_get_safely(response, "info"))

    return DetailedWarning(id=id_response, sender=sender, date_sent=date_sent, status=status, infos=infos)


def _poll_disaster_warnings() -> list[GeneralWarning]:
    result = [poll_biwapp_warning(), poll_mowas_warning(), poll_katwarn_warning()]
    return _filter_disaster_warnings(result)


def _poll_general_warnings() -> list[GeneralWarning]:
    result = [poll_police_warning(), poll_biwapp_warning(), poll_mowas_warning(), poll_katwarn_warning()]
    return _filter_disaster_warnings(result)


def _filter_disaster_warnings(warnings: list[list[GeneralWarning]]) -> list[GeneralWarning]:
    result = []
    for listWarning in warnings:
        for singleWarning in listWarning:
            result.append(singleWarning)
    return result


_call_general_warning_map = {
    WarnType.WEATHER: poll_dwd_warning,
    WarnType.FLOOD: poll_lhp_warning,
    WarnType.DISASTER: _poll_disaster_warnings,
    WarnType.GENERAL: _poll_general_warnings,
}


def call_general_warning(warning: WarnType) -> list[GeneralWarning]:
    """
    The Nina Api has different API calls for each warning that all basically work the same.
    Since we each user can subscribe to each warning individually we need to save their subscriptions.
    This is done using the WarnType enum.
    This method eases the calling of a specific poll_warning_method depending on the given WarnType
    :param warning: A WarnType enum that specifies which warning should be polled from the Nina API
    :return:  a list of GeneralWarnings, list ist empty if there are no current warnings
    :raises HTTPError:
    """
    if warning == WarnType.NONE:
        return []
    return _call_general_warning_map[warning]()
