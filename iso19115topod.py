
# coding: utf-8

# Converts from ISO19115 to the Project Open Data Metadata format for NASA JPL PO.DAAC

# In[ ]:

from lxml import etree


# In[ ]:

def define_iso19115_entities():
    entities = {}
    entities['title'] = ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"
    entities['description'] = ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString"
    entities['keyword'] = ".//gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString"
    entities['modified'] = './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'
    entities['publisher'] = {}
    #TODO: Doublecheck this tag
    entities['publisher']['name'] = ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"
    entities['contactPoint'] = {}
    entities['contactPoint']['fn'] = ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"
    entities['contactPoint']['hasEmail'] = ".//gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"
    entities['identifier'] = ".//gmd:fileIdentifier"
       
    return entities


# In[ ]:

def convert(xmlstring):
    result = {}
    entities = define_iso19115_entities()
    root = etree.XML(xmlstring)
    for key, value in entities.items():
        if isinstance(value, str):
            nodes = root.findall(value, root.nsmap)
            result[key] = nodes[0].text
        elif isinstance(value, dict):
            entry = {}
            for key2, value2 in value.items():
                if isinstance(value2, str):
                    nodes = root.findall(value2, root.nsmap)
                    entry[key2] = nodes[0].text
                else:
                    pass
            result[key] = entry
        else:
            pass
    return result


# In[ ]:

def fixxml(brokenxml):
    fixedxml = '''<gmd	
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xsi:schemaLocation="http://www.isotc211.org/2005/gmi https://cdn.earthdata.nasa.gov/iso/schema/1.0/ISO19115-2_EOS.xsd" 
	xmlns:xlink="http://www.w3.org/1999/xlink" 
	xmlns:gco="http://www.isotc211.org/2005/gco" 
	xmlns:gmd="http://www.isotc211.org/2005/gmd" 
	xmlns:gmx="http://www.isotc211.org/2005/gmx" 
	xmlns:gml="http://www.opengis.net/gml/3.2" 
	xmlns:gss="http://www.isotc211.org/2005/gss" 
	xmlns:gts="http://www.isotc211.org/2005/gts" 
	xmlns:gsr="http://www.isotc211.org/2005/gsr" 
	xmlns:gmi="http://www.isotc211.org/2005/gmi" 
	xmlns:srv="http://www.isotc211.org/2005/srv">''' + brokenxml + "</gmd>"
    return fixedxml

