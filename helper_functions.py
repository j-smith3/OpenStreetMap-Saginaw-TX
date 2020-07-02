#function will test if tag has a 'k' attribute that indicates it is a street address
def is_street_name(elem): 
    return (elem.attrib['k'] == "addr:street")
    
    
    
    
    
#function will test if tag has a 'k' attribute that indicates it is a speed limit
def is_maxspeed(elem): 
    return (elem.attrib['k'] == "maxspeed")
    
    
    
    
'''
    function will test if tag has a 'k' attribute that indicates it is from either the denomination, leisure, tourism,
    or amenity fields. These fields have data that needs cleaned up
'''
def is_proper_noun(elem): 
    return (elem.attrib['k'] == "denomination" or elem.attrib['k'] == "leisure" or elem.attrib['k'] == "tourism" or \
           elem.attrib['k'] == "amenity")