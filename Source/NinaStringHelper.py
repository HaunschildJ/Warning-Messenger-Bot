
#TODO mit was werden die Tags ersetzt? Leerzeichen?, Absatz? etc...
def filter_html_tags(s : str) -> str:
    filteredString = ""
    openedBracketsCounter = 0

    for i in range(0, len(s)):
         c = s[i]

         if (c == '<'):
             openedBracketsCounter += 1

         if (openedBracketsCounter == 0):
             filteredString += c

         if (c == '>'):
             openedBracketsCounter -= 1
             if (openedBracketsCounter == 0 and i+1 < len(s) and  s[i+1] != '<'):
                filteredString += ' '

    return  filteredString

#fill till 12 places with zeros
def expand_location_id_with_zeros(location_id : str):
    amount_of_zeros = 12 - len(location_id)
    for i in range(0, amount_of_zeros):
        location_id += '0'

    return  location_id

