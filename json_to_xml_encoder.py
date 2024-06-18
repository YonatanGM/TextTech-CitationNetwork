import ijson
import time
import xml.etree.ElementTree as ET
from lxml import etree
import os

start = time.process_time()

def create_xml_element(name, text=None, attributes=None):
    element = ET.Element(name, attrib=attributes or {})
    if text is not None:
        element.text = str(text)
    return element

def reconstruct_abstract(indexed_abstract):
    if not indexed_abstract:
        return ''
    
    # Extract terms and positions
    positions = indexed_abstract.get('InvertedIndex', {})
    max_position = max(pos for positions in positions.values() for pos in positions)
    
    # Create a list with None entries for the positions
    abstract_list = [None] * (max_position + 1)
    
    for term, indices in positions.items():
        for index in indices:
            abstract_list[index] = term
    
    # Join the terms to form the abstract text
    return ' '.join(term for term in abstract_list if term)

# Load the XML Schema from the file
with open('./dblp_paper_schema.xsd', 'rb') as schema_file:
    xml_schema_doc = etree.parse(schema_file)
xml_schema = etree.XMLSchema(xml_schema_doc)
xml_parser = etree.XMLParser(schema=xml_schema)

with open('./dblp.v12.50.json', "rb") as f:
    for i, element in enumerate(ijson.items(f, "item")):
        paper_id = element.get('id')
        root = ET.Element('paper', id=str(paper_id))

        root.append(create_xml_element('title', element.get('title')))
        root.append(create_xml_element('year', element.get('year')))

        authors = ET.Element('authors')
        for author in element.get('authors', []):
            author_attributes = {'org': author.get('org', '')}
            if author.get('id') is not None:
                author_attributes['id'] = str(author.get('id'))
            author_element = create_xml_element('author', author.get('name'), attributes=author_attributes)
            authors.append(author_element)
        root.append(authors)

        # Optional elements
        if element.get('n_citation') is not None:
            root.append(create_xml_element('n_citation', element.get('n_citation')))
        root.append(create_xml_element('doc_type', element.get('doc_type')))

        # References (required but can be empty)
        references = ET.Element('references')
        for ref in element.get('references', []):
            references.append(create_xml_element('reference', ref))
        root.append(references)

        # Venue
        venue_data = element.get('venue', {})
        venue_attributes = {
            'id': str(venue_data.get('id', '')),
            'type': venue_data.get('type', '')
        }
        venue_element = create_xml_element('venue', venue_data.get('raw', ''), attributes=venue_attributes)
        root.append(venue_element)

        # DOI
        if element.get('doi') is not None:
            root.append(create_xml_element('doi', element.get('doi')))

        # Keywords
        keywords = ET.Element('keywords')
        for keyword in element.get('fos', []):
            keyword_attributes = {'weight': str(keyword.get('w', ''))}
            keyword_element = create_xml_element('keyword', keyword.get('name'), attributes=keyword_attributes)
            keywords.append(keyword_element)
        root.append(keywords)

        # Publisher
        if element.get('publisher') is not None:
            root.append(create_xml_element('publisher', element.get('publisher')))

        # Abstract
        indexed_abstract = element.get('indexed_abstract', {})
        abstract_text = reconstruct_abstract(indexed_abstract)
        if abstract_text:
            root.append(create_xml_element('abstract', abstract_text))

        # Write to XML file
        folder_path = "./xml"
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        xml_file_path = f"{folder_path}/paper_{paper_id}.xml"
        tree = ET.ElementTree(root)
        tree.write(xml_file_path)

        # Validate the XML file against the schema
        try:
            with open(xml_file_path, 'rb') as xml_file:
                etree.parse(xml_file, xml_parser)
            print(f"XML file {xml_file_path} is valid.")
        except etree.XMLSyntaxError as e:
            print(f"XML file {xml_file_path} is invalid: {e}")

# Print execution time
end = time.process_time()
print(f"Execution time: {end - start} seconds")
