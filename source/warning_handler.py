import nina_service
import place_converter
import data_service
import time
import threading


def get_all_relevant_warning_ids(general_warnings: list[nina_service.GeneralWarning],
                                 relevant_postal_codes: list[str]) -> list[str]:
    """
    This method will return the relevant warning ids of the given general_warnings list.\n
    A warning id is relevant if a postal codes in the active area of the warning is in the relevant_postal_codes list

    Args:
        general_warnings: list of GeneralWarnings Enum for the relevant warnings
        relevant_postal_codes: list of strings with the relevant postal codes

    Returns:
        list of strings with the relevant warning ids for the given parameters
    """
    all_warnings = data_service.get_active_warnings_dict()
    result_ids = []
    for warning in general_warnings:
        try:
            postal_codes_for_warning = all_warnings[warning.id]
        except KeyError:
            continue

        for postal_code in relevant_postal_codes:
            if postal_code in postal_codes_for_warning:
                if warning.id not in result_ids:
                    result_ids.append(warning.id)
                    break

    return result_ids


def get_random_postal_code_for_active_warning(general_warning: nina_service.GeneralWarning) -> str:
    """
    This method will return a relevant postal code for the given general_warning\n
    If the given warning is not an active warning or not in the json then a default postal code will be returned

    Args:
        general_warning: GeneralWarning Enum with the warning a relevant postal code should be determined

    Returns:
        string with postal code the given warning is relevant for
    """
    all_warnings = data_service.get_active_warnings_dict()
    if general_warning.id not in all_warnings:
        print("Warning ID:" + general_warning.id + " was not found -->  no random postal code")
        return "64283"
    return all_warnings[general_warning.id][0]


def write_postal_codes(warning_id: int, geo_areas, counter: int):
    try:
        print("Processing Warning Number: " + str(counter))

        all_postal_codes = []
        for area in geo_areas:
            for coordinates in area.coordinates:
                dicts_in_polygon = place_converter.get_postal_code_dicts_in_polygon(coordinates)
                for dict_in_polygon in dicts_in_polygon:
                    postal_code = place_converter.get_postal_code_from_dict(dict_in_polygon)
                    if postal_code not in all_postal_codes:
                        all_postal_codes.append(postal_code)

        data_service.write_to_active_warnings_dict(warning_id, all_postal_codes)

    except Exception as e:
        print("ERROR: processing warning:" + str(counter) + " with id:" + str(warning_id) + " failed\n" + str(e))


def start_warning_handler_loop():
    while True:
        all_saved_warnings = data_service.get_active_warnings_dict()
        all_active_warnings = nina_service.get_all_active_warnings()
        """
            First: remove all warnings in active_warnings.json that are not active anymore
            """
        for saved_warning_id in all_saved_warnings:
            is_active = False
            for active_warning in all_active_warnings:
                if active_warning[0].id == saved_warning_id:
                    is_active = True
                    break
            if not is_active:
                data_service.remove_from_active_warnings_dict(saved_warning_id)

        """
            Second: compute and add all warnings that are new to active_warnings.json
        """
        counter = 0
        for active_warning in all_active_warnings:
            counter += 1
            if active_warning[0].id in all_saved_warnings:
                continue

            geo_areas = nina_service.get_detailed_warning_geo(active_warning[0].id).affected_areas
            write_postal_codes(active_warning[0].id, geo_areas, counter)

        time.sleep(120)


def init_warning_handler():
    """
    This method will be called when the bot is initialized
    """
    print("Initializing Warning Handler")
    warning_handler_thread = threading.Thread(target=start_warning_handler_loop)
    warning_handler_thread.start()
