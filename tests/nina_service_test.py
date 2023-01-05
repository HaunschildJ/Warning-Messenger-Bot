import sys

sys.path.insert(0, "..\source")

"""
irgendwie geht import nina_service nicht. Man muss alles was man benutzt einzeln importieren
Das mit dem bootloader.util funktioniert auch nicht da nina_service, noch andere module wie place_converter importiert
"""

from nina_service import WarnType
from nina_service import GeneralWarning
from nina_service import call_general_warning


def _print_general_warning(general_warning: GeneralWarning):
    print(general_warning.id)
    print(general_warning.version)
    print(general_warning.start_date)
    print(general_warning.severity)
    print(general_warning.type)
    print(general_warning.title)


def _print_general_warning_list(warnings: list[GeneralWarning]):
    for general_warning in warnings:
        _print_general_warning(general_warning)


# Manuelle Tests
def manual_test():
    for enum in WarnType:
        warnings = call_general_warning(enum)
        _print_general_warning_list(warnings)


manual_test()
