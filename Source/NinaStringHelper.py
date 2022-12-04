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
                filteredString += '\n'

    return  filteredString