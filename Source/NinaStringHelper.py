def in_bound(s : str, i: int) -> bool:
    return  i >= 0 and i < len(s)


#sucht ab index im string s ob die nächsten characters genau dem string sub_str entsprechen
def find_specific(s : str, index: int, sub_str : str) -> bool:
    return (s.find(sub_str, index, index + len(sub_str)) != -1)

#gibt den substring ab index im string s bis zum nächsten stop_char zurück
#kommt kein stop_char, gibt er den Rest des strings zurück
def extract_till_char(s : str, index: int, stop_char : str) -> str:
    extracted_string = ""
    for i in range(index, len(s)):
        if (s[i] == stop_char):
            break
        extracted_string += s[i]
    return  extracted_string

"""
filtert html tags aus dem string s heraus.
</p> tags (Achtung nur geschlossene) werden mit einem \n ersetzt
<a> tags in Form <a .... href="https:link.com"> Hyperlinktext </a>
werden ersetzt mit Hyperlinktext: https:link.com
"""
def filter_html_tags(s : str) -> str:
    filteredString = ""
    openedBracketsCounter = 0

    link = ""   #brauchen wir um hlinks aus den html tags rauszukopieren, da wir diese eigentlich insgesamt löschen
    in_text = False

    for i in range(0, len(s)):
         c = s[i]

         if (c == '<'):
             in_text = False
             openedBracketsCounter += 1


         if (openedBracketsCounter == 0):
             filteredString += c
             if (len(link) != 0 and i+1 < len(s) and s[i+1] == "<" and in_text):
                 filteredString += ": " + link
                 link = ""


         if (find_specific(s, i, "/p")):
            filteredString += '\n'

         if (find_specific(s, i, "href=")):
            link = extract_till_char(s, i + len("href=\""), '"')

         if (c == '>'):
             openedBracketsCounter -= 1
             in_text = True


    return  filteredString


#fill till 12 places with zeros
def expand_location_id_with_zeros(location_id : str):
    amount_of_zeros = 12 - len(location_id)
    for i in range(0, amount_of_zeros):
        location_id += '0'

    return  location_id

