import re
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
speed_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Airport", "Circle", "Cove", "Creek", "East", "Highway", 
            "Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Worth",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", 
            "Freeway", "Jaycrest", "Lake", "North", "Pass", "Path", "West", 
           "Plaza", "Point", "Rose", "Run", "South", "Terrace", "Trace", "Way"]


'''
this function will update street name endings to format all data to a standard type of street address
the name parameter is the value of the 'v' attribute which correlates to a street name, and the 
mapping parameter is a dictionary with key:value pairs for incorrect street endings and their corrections.
The function will return a correctly formatted name.
'''
def update_street(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        try:
            if int(street_type):
                return name.title()
        except: 
            if street_type not in expected:
                name = re.sub(street_type, mapping[street_type], name)
                return name.title()
            else:
                return name.title()
'''
    street_type will be the last word of the street string returned from the regular expression evaluation
    mapping[street_type] will replace this returned string from above, but with the value located at the 
    specified key in the mapping dictionary.... 'St.' ---> 'Street'
    name is the string we are looking at from our file 
    example re.sub('St.', 'Street', 'West Elm St.') ---> West Elm Street
'''    



'''
this function will verify the maxspeed attribute (name) is the standard mph,
it will return a correctly formatted string, that includes the mph unit
'''
def verify_speed(name):

    m = speed_type_re.search(name)
    if m:
        speed_type = m.group()
        try:
            if int(speed_type):
                speed_type = speed_type + ' mph'
                return speed_type
        except: 
            return name           

'''
This function takes in the name from the 'v' attribute field and formats it to a standard with Capital letters
and correct spacing. 
It returns this formatted name
'''
def fix_name (name):
    if '_' in name:
        return name.replace('_',' ').title()
    else: 
        return name.title()