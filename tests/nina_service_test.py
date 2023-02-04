import sys

sys.path.insert(0, "..\source")

"""
irgendwie geht import nina_service nicht. Man muss alles was man benutzt einzeln importieren
Das mit dem bootloader.util funktioniert auch nicht da nina_service, noch andere module wie place_converter importiert
"""

from nina_service import WarnType
from nina_service import GeneralWarning
from nina_service import call_general_warning
from nina_service import DetailedWarning
from nina_service import DetailedWarningInfo
from nina_service import DetailedWarningInfoArea
from nina_service import get_detailed_warning
from nina_service import get_detailed_warning_geo
from nina_service import DetailedWarningGeo
from nina_service import GeoCoordinates


def _none_or_value_to_str(value) -> str:
    if (value is None):
        return "None"
    return value


def _print_general_warning(general_warning: GeneralWarning):
    print(general_warning.id)
    print(general_warning.version)
    print(general_warning.start_date)
    print(general_warning.severity.value)
    print(general_warning.type)
    print(general_warning.title)
    print(" ")


def _print_detailed_warning_info_areas(areas: list[DetailedWarningInfoArea]):
    for area in areas:
        print("\tarea:")
        print("\t\t" + "area_description: " + _none_or_value_to_str(area.area_description))
        if area.geocode is not None:
            for geo in area.geocode:
                print("\t\t\tgeocode " + geo)


def _print_detailed_warning_infos(info: DetailedWarningInfo):
    print("info:")
    print("\t" + "event: " + _none_or_value_to_str(info.event))
    print("\t" + "severity: " + _none_or_value_to_str(info.severity.value))
    print("\t" + "date_expires: " + _none_or_value_to_str(info.date_expires))
    print("\t" + "headline: " + _none_or_value_to_str(info.headline))
    print("\t" + "description: " + _none_or_value_to_str(info.description))
    print("\t" + "language: " + _none_or_value_to_str(info.language))

    if info.area is not None:
        _print_detailed_warning_info_areas(info.area)


def _print_detailed_warning(warning: DetailedWarning):
    print("id: " + _none_or_value_to_str(warning.id))
    print("sender: " + _none_or_value_to_str(warning.sender))
    print("date_sent: " + _none_or_value_to_str(warning.date_sent))
    print("status: " + _none_or_value_to_str(warning.status))

    if warning.info is not None:
        _print_detailed_warning_infos(warning.info)

    print(" ")


def _print_detailed_warning_geo(warning: DetailedWarningGeo):
    for area in warning.affected_areas:
        print(area.coordinates)


# Manuelle Tests
def manual_test():
    CRED = '\033[91m'
    CEND = '\033[0m'
    for enum in WarnType:
        warnings = call_general_warning(enum)
        print(CRED + "###########################################################")
        print("################# Warnings for " + enum.name + ": #######################")
        print("##########################################################" + CEND)
        for warning in warnings:
            print("General Warning:")
            _print_general_warning(warning)
            print("Detailed Warning:")
            detailed_warning = get_detailed_warning(warning.id)
            _print_detailed_warning(detailed_warning)
            print("Detailed Warning GEO:")
            detailed_warning_geo = get_detailed_warning_geo(warning.id)
            _print_detailed_warning_geo(detailed_warning_geo)
            print("\n")


manual_test()
