import requests
from bs4 import BeautifulSoup


def export():
    response = requests.get(
        "https://dynasis.iutsf.org/index.php?group_id=6&id=14")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    result = soup.find_all("script")
    test = result[4].get_text()
    i = 0
    i2 = 0
    while i < len(test):
        if test[i] == "[" and test[i + 1] == "{":
            i2 = i + 2
            i += 2
        if test[i] == "}" and test[i + 1] == "]":
            test = test[i2:i + 2]
            break
        i += 1
    i = 0
    edt = []
    tempdict = {}
    tempstr = ''
    while i < len(test):
        if test[i] == 't' and test[i + 1] == 'i' and test[
                i + 2] == 't' and test[i + 3] == 'l' and test[i + 4] == 'e':
            i += 8
            while test[i] != "'" and i < len(test):
                if test[i] == "\\":
                    i += 4
                tempstr = tempstr + test[i]
                i += 1
            tempdict['title'] = tempstr
            tempstr = ''
        if test[i] == 's' and test[i + 1] == 't' and test[
                i + 2] == 'a' and test[i + 3] == 'r' and test[i + 4] == 't':
            i += 8
            while test[i] != "'" and i < len(test):
                if test[i] == "\\":
                    i += 4
                tempstr = tempstr + test[i]
                i += 1
            tempdict['start'] = tempstr
            tempstr = ''
        if test[i] == 'e' and test[i + 1] == 'n' and test[i + 2] == 'd':
            i += 6
            while test[i] != "'" and i < len(test):
                if test[i] == "\\":
                    i += 4
                tempstr = tempstr + test[i]
                i += 1
            tempdict['end'] = tempstr
            tempstr = ''
        if len(tempdict) == 3:
            edt.append(tempdict)
            tempdict = {}

        i += 1
        if test[i] == ']':
            break
    return edt


def affichage(liste):
  output = ''
  for dict in liste:
    output += "Cours de {}. \nDe **{}** à **{}**.\n".format(dict['title'],dict['start'][11:16],dict['end'][11:16])
  return output

#print(export())
