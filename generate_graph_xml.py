import json
import xml.etree.ElementTree as ET
from lxml import etree

# Function to create an XML element with optional text and attributes
def create_xml_element(name, text=None, attributes=None):
    element = ET.Element(name, attrib=attributes or {})
    if text is not None:
        element.text = str(text)
    return element

# Function to build the GraphML XML structure with nodes and edges, including metadata
def build_graph_xml(papers, output_file):
    # Create the root element for GraphML
    graphml = ET.Element("graphml", 
                         xmlns="http://graphml.graphdrawing.org/xmlns", 
                         attrib={
                             "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                             "xsi:schemaLocation": "http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"
                         })
    
    # Define keys for the metadata fields
    keys = [
        {"id": "title", "for": "node", "attr_name": "title", "attr_type": "string"},
        {"id": "authors", "for": "node", "attr_name": "authors", "attr_type": "string"},
        {"id": "year", "for": "node", "attr_name": "year", "attr_type": "int"},
        {"id": "doc_type", "for": "node", "attr_name": "doc_type", "attr_type": "string"},
        {"id": "doi", "for": "node", "attr_name": "doi", "attr_type": "string"},
    ]
    for key in keys:
        ET.SubElement(graphml, "key", id=key["id"], attrib={"for": key["for"], "attr.name": key["attr_name"], "attr.type": key["attr_type"]})
    
    # Create the main graph element
    graph = ET.SubElement(graphml, "graph", id="G", edgedefault="directed")

    # Track nodes and edges
    node_ids = set()
    edges = []

    # Iterate over each paper to create nodes and edges
    for paper in papers:
        paper_id = str(paper['id'])
        
        # Create a node for each paper if it doesn't already exist
        if paper_id not in node_ids:
            node = ET.SubElement(graph, "node", id=paper_id)
            
            # Add metadata to the node
            title = paper.get('title', '')
            if title:
                title_data = create_xml_element('data', text=title, attributes={'key': 'title'})
                node.append(title_data)

            authors = ', '.join([author['name'] for author in paper.get('authors', [])])
            if authors:
                authors_data = create_xml_element('data', text=authors, attributes={'key': 'authors'})
                node.append(authors_data)

            year = paper.get('year')
            if year is not None:
                year_data = create_xml_element('data', text=str(year), attributes={'key': 'year'})
                node.append(year_data)

            doc_type = paper.get('doc_type', '')
            if doc_type:
                doc_type_data = create_xml_element('data', text=doc_type, attributes={'key': 'doc_type'})
                node.append(doc_type_data)

            doi = paper.get('doi', '')
            if doi:
                doi_data = create_xml_element('data', text=doi, attributes={'key': 'doi'})
                node.append(doi_data)

            node_ids.add(paper_id)

        # Create edges for references
        for ref_id in paper.get('references', []):
            ref_id = str(ref_id)
            if ref_id not in node_ids:
                node = ET.SubElement(graph, "node", id=ref_id)
                node_ids.add(ref_id)
            edges.append((paper_id, ref_id))

    # Add edges to the graph
    for i, (source, target) in enumerate(edges):
        ET.SubElement(graph, "edge", id=f"e{i}", source=source, target=target)

    # Write the entire XML structure to a file
    tree = ET.ElementTree(graphml)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Function to validate the GraphML XML against the schema
def validate_graphml(xml_path, schema_path):
    # Load the XML schema
    with open(schema_path, 'rb') as schema_file:
        schema_root = etree.XML(schema_file.read())
    schema = etree.XMLSchema(schema_root)

    # Parse and validate the XML file
    with open(xml_path, 'rb') as xml_file:
        xml_root = etree.parse(xml_file)
    
    is_valid = schema.validate(xml_root)
    
    # Output validation result
    if is_valid:
        print("The GraphML file is valid.")
    else:
        print("The GraphML file is invalid.")
        print(schema.error_log)

# Load the subset of papers from a JSON file
with open('./dblp.v12.12642.json', 'r') as f:
    papers = json.load(f)

# Generate the GraphML file
output_file = "./citation_graph.xml"
build_graph_xml(papers, output_file)

# Validate the generated GraphML file against the schema
schema_path = 'graphml.xsd'
validate_graphml(output_file, schema_path)
