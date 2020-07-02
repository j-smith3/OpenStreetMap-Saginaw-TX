import csv
import pprint
import re
import xml.etree.ElementTree as ET
import cerberus
import schema
from helper_functions import is_street_name, is_maxspeed, is_proper_noun
from update_functions import update_street, verify_speed, fix_name

# ================================================== #
#                    Variables                       #
# ================================================== #
OSM_PATH = "Saginaw.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
DOUBLE_COLON = re.compile(r'^([A-Za-z]|_)+:([A-Za-z]|_)+:([A-Za-z]|_)+')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


mapping = { "Blvd": "Boulevard",
            "BLVD": "Boulevard",
            "Blvd.": "Boulevard",
            "BLVD.": "Boulevard",
            "Fwy": "Freeway",
            "Ln": "Lane",
            "Rd": "Road"
            }

'''
this function will format and shape the data into a dictionary. The 'element' parameter 
is an element passed in from parsing the XML file. It returns a dictionary and lists
that are formatted and ready to write into a csv file
'''
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
   #Clean and shape node or way XML element to Python dict

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    node_tags = []
    way_tags = []

    if element.tag == 'node':

        #first loop through to get node's attributes and values into a dictionary
        for key, value in element.attrib.items():
            if key in NODE_FIELDS:
                node_attribs[key] = value
        #print (node_attribs)

        ''' 
            Next, loop through the child tags and parse out the
            key, value, and clean up the 'key' to create types. Then
            put everything into a dictionary to append to tags list.
        '''
        for i in element.iter('tag'):
            
            temp_dict = {}
            
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            elif DOUBLE_COLON.search(i.attrib['k']):
                temp_dict['id'] = element.attrib['id']
                temp_dict ['type'] = i.attrib['k'].split(':')[0]
                temp_dict ['key'] = i.attrib['k'].split(':')[1] + ':' + i.attrib['k'].split(':')[2]
                temp_dict ['value'] = i.attrib['v']
            elif LOWER_COLON.search(i.attrib['k']):
                temp_dict['id'] = element.attrib['id']
                temp_dict['type'] = i.attrib['k'].split(':')[0]                          
                temp_dict['key'] = i.attrib['k'].split(':')[1]               
                temp_dict['value'] = i.attrib['v']
            else:
                temp_dict['id'] = element.attrib['id']
                temp_dict['type'] = 'regular'                          
                temp_dict['key'] = i.attrib['k']               
                temp_dict['value'] = i.attrib['v']
            #print (temp_dict)
            node_tags.append(temp_dict)
        

        return {'node': node_attribs, 'node_tags': node_tags}

    elif element.tag == 'way':

        for key, value in element.attrib.items():
            if key in WAY_FIELDS:
                #print (key)
                #print (value)
                way_attribs[key] = value
        #print (way_attribs)

        ''' 
            Since the way tags follow the same rules as the node tags, these
            are processed the same way.
        '''
        for i in element.iter('tag'):
            temp = {}
            
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            elif DOUBLE_COLON.search(i.attrib['k']):
                temp['id'] = element.attrib['id']
                temp ['type'] = i.attrib['k'].split(':')[0]
                temp ['key'] = i.attrib['k'].split(':')[1] + ':' + i.attrib['k'].split(':')[2]
                temp ['value'] = i.attrib['v']
            elif LOWER_COLON.search(i.attrib['k']):
                temp['id'] = element.attrib['id']
                temp['type'] = i.attrib['k'].split(':')[0]                          
                temp['key'] = i.attrib['k'].split(':')[1]               
                temp['value'] = i.attrib['v']
            else:
                temp['id'] = element.attrib['id']
                temp['type'] = 'regular'                          
                temp['key'] = i.attrib['k']               
                temp['value'] = i.attrib['v']
            #print (temp)
            way_tags.append(temp)
        """
        enumerate() is used here to create a counter for each 'nd' child node.
        """

        for counter, i in enumerate(element.iter('nd')):
            nd = {}
            nd['id'] = element.attrib['id']
            nd['node_id'] = i.attrib['ref']
            nd['position'] = counter
            way_nodes.append(nd)
        #print (way_nodes)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': way_tags}
        
        
#validates that data is in correct format that the schema defined
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))
        
# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with open(NODES_PATH, 'w', encoding='utf-8') as nodes_file, \
         open(NODE_TAGS_PATH, 'w', encoding='utf-8') as nodes_tags_file, \
         open(WAYS_PATH, 'w', encoding='utf-8') as ways_file, \
         open(WAY_NODES_PATH, 'w', encoding='utf-8') as way_nodes_file, \
         open(WAY_TAGS_PATH, 'w', encoding='utf-8') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, fieldnames=NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, fieldnames=NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, fieldnames=WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, fieldnames=WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, fieldnames=WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()
        
        for event, element in ET.iterparse(file_in):
            if element.tag == 'node' or element.tag =='way':
                
                
                #this section cleans and updates data formats
                for tag in element.iter("tag"):
                    if is_street_name(tag): #update street names to a standard format
                        new_name = update_street(tag.attrib['v'], mapping)
                        tag.attrib['v'] = new_name
                    if is_maxspeed(tag): #update maxspeed attribute to a standard format
                        new_name = verify_speed(tag.attrib['v'])
                        tag.attrib['v'] = new_name
                    if is_proper_noun(tag): #update naming conventions to a standard format
                        new_name = fix_name(tag.attrib['v'])
                        tag.attrib['v'] = new_name            
                                                              
                
                el = shape_element(element)
                if el:
                    if validate is True:
                        validate_element(el, validator)

                    if element.tag == 'node':
                        nodes_writer.writerow(el['node'])
                        node_tags_writer.writerows(el['node_tags'])
                    elif element.tag == 'way':
                        ways_writer.writerow(el['way'])
                        way_nodes_writer.writerows(el['way_nodes'])
                        way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)