import os
import urllib.request
from urllib.error import URLError, HTTPError
import pandas as pd
from time import sleep

os.chdir('C:/Users/cjoynt/Desktop/FishAnalysis')

WaterBody = pd.read_csv('WaterBody.csv', sep = '|', encoding = 'latin1', header = 0)

partURL = 'https://www.kimonolabs.com/api/6885gym6?apikey=LDXiLSTZg8PKmGDEAKenFyDmo5ThsLRB&lakeCode='

dataFile = open('fishsurvey.txt', 'w')
errorFile = open('errors.txt', 'w')
successFile = open('success.txt', 'w')

errorCount = 0
successCount = 0

for index, row in WaterBody.iterrows():
    lakeCode = WaterBody.irow(index)['wbURLParam']
    fullURL = (partURL + lakeCode)

    try:
        response = urllib.request.urlopen(fullURL)
        if (response.getcode() == 200):
            data = pd.read_json(fullURL)	
        else:
            errorCount += 1
            errorFile.write('Error number:' + str(errorCount) + ' at lake code:' + lakeCode + ' for reason: Response Error' + '\n')
            sleep(5)            
            continue
			
    except urllib.error.URLError as ue:
        errorCount += 1
        errorFile.write('Error number:' + str(errorCount) + ' at lake code:' + lakeCode + ' for reason: URL Error' + '\n')
        sleep(5)
        continue
		
    except urllib.error.HTTPError as he:
        errorCount += 1
        errorFile.write('Error number:' + str(errorCount) + ' at lake code:' + lakeCode + ' for reason: HTTP Error' + '\n')
        sleep(5)
        continue
    
    if len(data.index) == 2:
        for i in data['results']['collection1']:
            dataFile.write(lakeCode + '|' + i['fishType'] + '|' + i['countCaught'] + '|' + i['avgLen'] + '|' + i['avgWt'] + '|' + data['results']['collection2'][0]['surveyDt'] + '\n')
		
        successCount += 1
        successFile.write('Success number:' + str(successCount) + ' Appended lake code:' + lakeCode + '\n')		
        sleep(5)
    else:
        errorCount += 1
        errorFile.write('Error number:' + str(errorCount) + ' at lake code:' + lakeCode + ' for reason: No collection 2' + '\n')
        continue

dataFile.close()
errorFile.close()
successFile.close()
		
successRate = successCount/718
errorRate = errorCount/718

print ('Retrieval of fish survey data has completed')
print ('A total of ' + str(successCount) + ' lake codes were successfully retrieved.')
print ('A total of ' + str(errorCount) + ' errors were encountered.')
print ('Success rate: ' + str(successRate))
print ('Error rate: ' + str(errorRate))