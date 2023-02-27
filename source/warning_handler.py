import nina_service
import place_converter
import data_service
import time


def update_all_warnings() -> dict:
    """
    This method will add the relevant postal codes of all active warnings to the active_warnings.json\n
    Updating the relevant postal codes for a warning has massive overhead --> this method can take a few minutes\n
    If another thread is already called this method and is not done yet, this method will wait until the other thread
    is done and then finish

    Returns:
        dict with the active warnings json
    """
    print("updating warnings")
    all_warnings = data_service.get_active_warnings_dict()
    # check if another thread is already updating all warnings
    if all_warnings == {}:
        data_service.set_active_warnings_dict({"is_already_running": True})
    else:
        if all_warnings["is_already_running"]:
            while all_warnings["is_already_running"]:
                time.sleep(1)
                all_warnings = data_service.get_active_warnings_dict()
            return all_warnings
        all_warnings["is_already_running"] = True
        data_service.set_active_warnings_dict(all_warnings)

    # if there was no other thread already updating warnings
    warnings = nina_service.get_all_active_warnings()
    counter = 1
    for warning in warnings:
        general_warning = warning[0]
        warning_id = general_warning.id
        try:
            if warning_id not in all_warnings:
                geo_areas = nina_service.get_detailed_warning_geo(warning_id).affected_areas
                all_postal_codes = []
                for area in geo_areas:
                    for coordinates in area.coordinates:
                        dicts_in_polygon = place_converter.get_postal_code_dicts_in_polygon(coordinates)
                        for dict_in_polygon in dicts_in_polygon:
                            postal_code = place_converter.get_postal_code_from_dict(dict_in_polygon)
                            if postal_code not in all_postal_codes:
                                all_postal_codes.append(postal_code)
                all_warnings[warning_id] = all_postal_codes
        except:
            print("ERROR: processing warning:" + str(counter) + " with id:" + str(warning_id) + " failed")
        print("processed warnings: " + str(counter) + "/" + str(len(warnings)))
        counter += 1
    all_warnings["is_already_running"] = False
    data_service.set_active_warnings_dict(all_warnings)
    return all_warnings


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
            print("Warning ID:" + warning.id + " was not found --> updating")
            all_warnings = update_all_warnings()
            try:
                postal_codes_for_warning = all_warnings[warning.id]
            except KeyError:
                print("Warning ID was not found even after updating --> skip")
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
        print("Warning ID:" + general_warning.id + " was not found --> updating")
        all_warnings = update_all_warnings()
        if general_warning.id not in all_warnings:
            print("Warning ID was not found even after updating --> no random postal code")
            return "64283"
    return all_warnings[general_warning.id][0]


def init_warning_handler():
    """
    This method will be called when the bot is initialized
    """
    print("Initializing Warning Handler")
    all_warnings = data_service.get_active_warnings_dict()
    all_warnings["is_already_running"] = False
    data_service.set_active_warnings_dict(all_warnings)
    update_all_warnings()
