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


def _none_or_value_to_str(value) -> str:
    if (value is None):
        return  "None"
    return  value



def _print_general_warning(general_warning: GeneralWarning):
    print(general_warning.id)
    print(general_warning.version)
    print(general_warning.start_date)
    print(general_warning.severity)
    print(general_warning.type)
    print(general_warning.title)
    print(" ")


def _print_general_warning_list(warnings: list[GeneralWarning]):
    for general_warning in warnings:
        _print_general_warning(general_warning)


def _print_detailed_warning_info_areas(areas: list[DetailedWarningInfoArea]):
    for area in areas:
        print("\tarea:")
        print("\t\t"+ "area_description: "+ _none_or_value_to_str(area.area_description))
        if area.geocode is not None:
            for geo in area.geocode:
                print("\t\t\tgeocode " + geo)

def _print_detailed_warning_infos(infos:  list[DetailedWarningInfo]):
    for info in infos:
        print("info:")
        print("\t"+ "event: "+ _none_or_value_to_str(info.event))
        print("\t"+ "severity: "+ _none_or_value_to_str(info.severity.name))
        print("\t"+ "date_expires: "+ _none_or_value_to_str(info.date_expires))
        print("\t"+ "headline: "+ _none_or_value_to_str(info.headline))
        print("\t"+ "description: "+ _none_or_value_to_str(info.description))

        if info.area is not None:
            _print_detailed_warning_info_areas(info.area)


def _print_detailed_warning(warning: DetailedWarning):
    print("id: "+_none_or_value_to_str(warning.id))
    print("sender: "+_none_or_value_to_str(warning.sender))
    print("date_sent: "+_none_or_value_to_str(warning.date_sent))
    print("status: "+_none_or_value_to_str(warning.status))

    if warning.infos is not None:
        _print_detailed_warning_infos(warning.infos)

    print(" ")





def _print_detailed_warnings_from_general_warnings(warnings: list[GeneralWarning]):
    for general_warning in warnings:
        detailed_warning = get_detailed_warning(general_warning.id)
        _print_detailed_warning(detailed_warning)
        print(" ")


# Manuelle Tests
def manual_test():
    for enum in WarnType:
        warnings = call_general_warning(enum)
        print("General Warnings for " + enum.name + ":")
        _print_general_warning_list(warnings)
        print("Detailed Warnings for " + enum.name + ":")
        _print_detailed_warnings_from_general_warnings(warnings)


//manual_test()
