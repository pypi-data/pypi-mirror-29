import json
import sys
import os
import pathlib


def filterConfigFile(inFileName):
    if pathlib.Path(inFileName).suffix == '.txt':
        return True
    else:
        return False


def ParseConfigTextFile():
    fileLocation = sys.argv[1]

    if os.path.isdir(fileLocation):
        allFiles = sorted(list(filter(filterConfigFile, os.listdir(fileLocation))),
                          key=lambda filename: filename.split('.')[0])
    else:
        allFiles = [os.path.split(fileLocation)[-1]]
        fileLocation = os.path.dirname(fileLocation)

    for file in allFiles:
        with open(os.path.join(fileLocation, file), 'r') as f:
            jsonTexts = f.readlines()
            jsonText = ''
            for line in jsonTexts:
                jsonText += line
            dicts = json.loads(jsonText)

            outputString = 'Name: ' + dicts['name']
            if 'color' in file.split('.'):
                outputString += '.' + dicts['format'] + '\n'
                outputString += 'Type: Color Image \n'
                outputString += 'Expo: ' + str(dicts['expotime']) + ' ms\n'
                outputString += 'Gain: ' + str(dicts['gainval']) + '\n'

            elif 'mono' in file.split('.'):
                outputString += '\nType: HS Image\n'
                outputString += 'Expo: ' + str(dicts['expotime']) + ' ms\n'
                outputString += 'Band: ' + str(dicts['startband']) + ' - ' + str(dicts['endband']) + ' / ' + str(dicts['bandnum']) + '\n'
            outputString += 'Save: ' + dicts['location'] + '\n'
            outputString += 'Amp: ' + dicts['amp'] + '\n'
            outputString += 'Position: (' + str(dicts['xpos']) + ', ' + str(dicts['ypos']) + ', ' + str(
                dicts['zpos']) + ')' + '\n'
            print(outputString)
