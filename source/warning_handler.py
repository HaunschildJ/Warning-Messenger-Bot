import nina_service
import place_converter
import data_service


def update_all_warnings():
    print("updating warnings")
    warnings = nina_service.get_all_active_warnings()
    counter = 1
    all_warnings = data_service.get_active_warnings_dict()
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
    data_service.set_active_warnings_dict(all_warnings)


def get_all_relevant_warning_ids(general_warnings: list[nina_service.GeneralWarning],
                                 relevant_postal_codes: list[str]) -> list[str]:
    all_warnings = data_service.get_active_warnings_dict()
    result_ids = []
    for warning in general_warnings:
        try:
            postal_codes_for_warning = all_warnings[warning.id]
        except KeyError:
            print("Warning ID:" + warning.id + " was not found --> updating")
            update_all_warnings()
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


def init_warning_handler():
    print("Initializing Warning Handler")
    update_all_warnings()
