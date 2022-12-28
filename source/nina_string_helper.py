def in_bound(s: str, i: int) -> bool:
    """
    Checks if i is smaller than the length of the String s and greater or equal to 0
    """
    return 0 <= i < len(s)


def find_specific(s: str, index: int, sub_str: str) -> bool:
    """
    searches in string s, starting at index, if the next characters are sub_str

    Arguments:
         s: String that is the main String
         index: Integer with the starting index
         sub_str: String with the SubString
     Returns:
         Boolean if the substring is really the substring of the string s at the index
    """
    return s.find(sub_str, index, index + len(sub_str)) != -1


def extract_till_char(s: str, index: int, stop_char: str) -> str:
    """
    searches in string s, starting at index, the substring until character stop_char occurs

    Arguments:
        s: String that is the main String
        index: Integer with the starting index
        stop_char: Character that signals the char to stop at
    Returns:
        The substring starting at index until the character stop_char occurs
    """
    extracted_string = ""
    for i in range(index, len(s)):
        if s[i] == stop_char:
            break
        extracted_string += s[i]
    return extracted_string


def filter_html_tags(s: str) -> str:
    """
    filters html tags from the string s.
    </p> tags (only closed once) will be replaced with \n
    <a> tags -> <a .... href="https:link.com"> Hyperlinktext </a>
    &nbsp; (== nonbreaking space) replaced with space

    Arguments:
        s: String that will be filtered. Has to be valid html code.
    Returns:
        Filtered String
    """
    filtered_string = ""
    opened_brackets_counter = 0

    link = ""  # brauchen wir um hlinks aus den html tags rauszukopieren, da wir diese eigentlich insgesamt löschen
    in_text = False

    s = s.replace("&nbsp;", " ")

    for i in range(0, len(s)):
        c = s[i]

        if c == '<':
            in_text = False
            opened_brackets_counter += 1

        if opened_brackets_counter == 0:
            filtered_string += c
            if len(link) != 0 and i + 1 < len(s) and s[i + 1] == "<" and in_text:
                filtered_string += ": " + link
                link = ""

        if find_specific(s, i, "/p"):
            filtered_string += '\n'

        if find_specific(s, i, "href="):
            link = extract_till_char(s, i + len("href=\""), '"')

        if c == '>':
            opened_brackets_counter -= 1
            in_text = True

    return filtered_string


def expand_location_id_with_zeros(location_id: str) -> str:
    """
    Fills given String with 0 until it has 12 characters

    Arguments:
        location_id: String that will be filled
    Returns:
        The filled String
    """
    amount_of_zeros = 12 - len(location_id)
    for i in range(0, amount_of_zeros):
        location_id += '0'

    return location_id
