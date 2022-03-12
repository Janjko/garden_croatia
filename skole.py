download_url = 'http://52.178.158.152/api/file/skole_os.csv'

dataset_id = 'e-matica'

source = 'E-Matica'
add_source = True

query = [('ref:e-matica',)]

bbox = False

delete_unmatched = False

tag_unmatched = False

master_tags = ('addr:postcode', 'isced:level', 'amenity')

max_distance = 1000000

duplicate_distance = 0

bbox_padding = 2

def dataset(fileobj):
    import csv
    import logging
    import random
    import requests
    import json
    from io import BytesIO
    
    
    byte_str = fileobj.read()
    csvTextOsnovne = byte_str.decode('UTF-8').splitlines()
    del csvTextOsnovne[0:1]

    
    r = requests.get('http://52.178.158.152/api/file/srednje--skole.csv')
    if r.status_code != 200:
        logging.error('Could not download source data: %s %s', r.status_code, r.text)
        return None
    if len(r.content) == 0:
        logging.error('Empty response from %s', url)
        return None
    fileobjSrednje = BytesIO(r.content)
    
    byte_strSrednje = fileobjSrednje.read()
    csvTextSrednje = byte_strSrednje.decode('UTF-8').splitlines()
    del csvTextSrednje[0:1]
    
    csvText = csvTextOsnovne + csvTextSrednje
    
    csvreader = csv.reader(csvText, delimiter=';', quotechar='"')
    
    data = []

    for row in csvreader:
        #print (row[0]+', '+row[1])
        tags = {
            'ref:e-matica': row[0],
            'name': row[1]
        }
        isced=[]
        if "Osnovna" in row[6]:
            isced.append('1;2')
        if "Srednja" in row[6]:
            isced.append('3')
        
        if "Umjetni" in row[6] and "Srednja" in row[6] and "glazben" in row[1].lower():
            tags['amenity']='music_school'
        elif "Umjetni" in row[6] and "Srednja" in row[6] and ("ples" in row[1].lower() or "balet" in row[1].lower()):
            tags['amenity']='dancing_school'
        else:
            tags['amenity']='school'
        
        tags['isced:level']=';'.join(isced)
        
        data.append(SourcePoint(row[0], 45.0, 16.0, tags))
        
    print(len(data))
    return data

def matches(osmtags, mzostags):
    if osmtags['ref:e-matica'][0] != mzostags['ref:e-matica'][0]:
        return False
    return True
