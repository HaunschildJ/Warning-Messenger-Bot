
#TODO mit was werden die Tags ersetzt? Leerzeichen?, Absatz? etc...
def filter_html_tags(s : str) -> str:
    filtered_string = ""
    opened_brackets_counter = 0

    for i in range(0, len(s)):
         c = s[i]

         if c == '<':
             opened_brackets_counter += 1

         if opened_brackets_counter == 0:
             filtered_string += c

         if c == '>':
             opened_brackets_counter -= 1
             if opened_brackets_counter == 0 and i+1 < len(s) and  s[i + 1] != '<':
                filtered_string += ' '

    return  filtered_string

#fill till 12 places with zeros
def expand_location_id_with_zeros(location_id : str):
    amount_of_zeros = 12 - len(location_id)
    for i in range(0, amount_of_zeros):
        location_id += '0'

    return  location_id

