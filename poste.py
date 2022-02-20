download_url = 'https://www.posta.hr/mapahp.aspx?lng=_hr'

no_dataset_id = True

source = 'https://www.posta.hr'
add_source = False

query = [('amenity', 'post_office'),('addr:postcode',),('operator:wikidata', 'Q507289')]

bbox = (42.47999136,13.49,46.5037509222,19.3904757016)

delete_unmatched = True

overpass_timeout = 1200

tag_unmatched = False

master_tags = ('addr:postcode')

max_distance = 300

def dataset(fileobj):
    import re
    import logging
    import json
    
    data = []
    byte_str = fileobj.read().decode('utf-8')
    #print (byte_str)
    coordinatesRegex = re.compile(r'new\W+google\.maps\.LatLng\(\W?(\d\d\.\d+)\W?,\W?(\d\d\.\d+)\W?\)')
    coordArr = []
    coordinatesStr = coordinatesRegex.findall(byte_str)
    
    for pair in coordinatesStr:
        coordArr.append([float(pair[0]), float(pair[1])])
    
    #print (coordArr)
    
    n=0

    uredRegex = re.compile(u'^\W*?(content.*TANSKI URED.*)$',re.MULTILINE)
    kovcezicRegex = re.compile(u'^\W*?(content.*TANSKI KOV.*)$',re.MULTILINE)
    paketomatRegex = re.compile(u'^\W*?(content.*PAKETOMAT.*)$',re.MULTILINE)
    postcodeRegex = re.compile(r'\<div class="cloud"\>(?:\<img.*?\/\>)?\<h1\>.*?\<br \/\>\<br \/\>(\d{5}-?\d*)')
    idRegex = re.compile(r'content\[(\d*)\]')
    for ured in uredRegex.findall(byte_str):
        postcode = postcodeRegex.findall(ured)[0]
        id = idRegex.findall(ured)[0]
        tags = {
            'addr:postcode': postcode,
            'amenity': 'post_office',
        }
        data.append(SourcePoint(postcode, coordArr[n][0], coordArr[n][1], tags))
        n+=1
#    for kovcezic in kovcezicRegex.findall(byte_str):
#        n+=1
#        postcode = postcodeRegex.findall(kovcezic)[0]
#        id = idRegex.findall(kovcezic)[0]
#        tags = {
#            'addr:postcode': postcode,
#            'amenity': 'post_box',
#        }
#        data.append(SourcePoint(n, coordArr[n][0], coordArr[n][1], tags))
#    for paketomat in paketomatRegex.findall(byte_str):
#        n+=1
#        postcode = postcodeRegex.findall(paketomat)[0]
#        id = idRegex.findall(kovcezic)[0]
#        tags = {
#            'addr:postcode': postcode,
#            'amenity': 'vending_machine',
#            'vending': 'parcel_pickup',
#        }
#        data.append(SourcePoint(n, coordArr[n][0], coordArr[n][1], tags))


    print(len(data))
    return data

def find_ref(osmtags):
    return osmtags['addr:postcode']
