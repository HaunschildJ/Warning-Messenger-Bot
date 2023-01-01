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

    tags in form of <a .... href="https:link.com"> Hyperlinktext </a> ->  Hyperlinktext: https:link.com
    if no characters for the Hyperlinktext are provided, no link will be pasted in the output, for example:
    Hello World <a href="https:link.com"></a> -> Hello World
    but if there is at least one (whitespace counts as well) the link will be pasted
    Hello World <a href="https:link.com">_</a> -> Hello World _: https:link.com
    The link must be enclosed by " " chars for it to work


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
