import os
import csv
import xml.etree.ElementTree as ET

# Directory containing the XML files
xml_dir = './xml'

# Create 'csv' directory if it doesn't exist
csv_dir = 'csv'
os.makedirs(csv_dir, exist_ok=True)

# Initialize lists for nodes and relationships
nodes_paper = []
nodes_author = []
nodes_venue = []
nodes_fos = []
relationships_authored = []
relationships_published_in = []
relationships_has_fos = []
relationships_cites = []

# Parse each XML file
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        tree = ET.parse(os.path.join(xml_dir, xml_file))
        root = tree.getroot()

        # Extract paper attributes
        paper_id = root.attrib.get('id', '')
        title = root.findtext('title', '')
        year = root.findtext('year', '')
        n_citation = root.findtext('n_citation', '')
        doc_type = root.findtext('doc_type', '')
        doi = root.findtext('doi', '')
        publisher = root.findtext('publisher', '')
        abstract = root.findtext('abstract', '')

        # Add paper node
        nodes_paper.append({
            "id": paper_id,
            "title": title,
            "year": year,
            "n_citation": n_citation,
            "doc_type": doc_type,
            "publisher": publisher,
            "doi": doi
        })

        # Extract and add venue node and relationship
        venue = root.find('venue')
        if venue is not None:
            venue_id = venue.attrib.get('id', '')
            venue_name = venue.text
            venue_type = venue.attrib.get('type', '')

            nodes_venue.append({
                "id": venue_id,
                "name": venue_name,
                "type": venue_type
            })

            relationships_published_in.append({
                "start_node_id": paper_id,
                "end_node_id": venue_id,
                "relationship_type": "PUBLISHED_IN"
            })

        # Extract and add author nodes and relationships
        authors = root.find('authors')
        if authors is not None:
            for author in authors.findall('author'):
                author_id = author.attrib.get('id', '')
                author_name = author.text
                author_org = author.attrib.get('org', '')

                nodes_author.append({
                    "id": author_id,
                    "name": author_name,
                    "org": author_org
                })

                relationships_authored.append({
                    "start_node_id": author_id,
                    "end_node_id": paper_id,
                    "relationship_type": "AUTHORED"
                })

        # Extract and add Field of Study (FOS) nodes and relationships
        keywords = root.find('keywords')
        if keywords is not None:
            for keyword in keywords.findall('keyword'):
                fos_name = keyword.text
                fos_weight = keyword.attrib.get('weight', '')

                nodes_fos.append({
                    "name": fos_name
                })

                relationships_has_fos.append({
                    "start_node_id": paper_id,
                    "end_node_id": fos_name,
                    "relationship_type": "HAS_FOS",
                    "weight": fos_weight
                })

        # Extract and add citation relationships
        references = root.find('references')
        if references is not None:
            for reference in references.findall('reference'):
                ref_id = reference.text

                relationships_cites.append({
                    "start_node_id": paper_id,
                    "end_node_id": ref_id,
                    "relationship_type": "CITES"
                })

# Remove duplicates from nodes
nodes_author = [dict(t) for t in {tuple(d.items()) for d in nodes_author}]
nodes_venue = [dict(t) for t in {tuple(d.items()) for d in nodes_venue}]
nodes_fos = [dict(t) for t in {tuple(d.items()) for d in nodes_fos}]

# Write nodes to CSV
with open(os.path.join(csv_dir, 'nodes_paper.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "title", "year", "n_citation", "doc_type", "publisher", "doi"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(nodes_paper)

with open(os.path.join(csv_dir, 'nodes_author.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "org"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(nodes_author)

with open(os.path.join(csv_dir, 'nodes_venue.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "type"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(nodes_venue)

with open(os.path.join(csv_dir, 'nodes_fos.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["name"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(nodes_fos)

# Write relationships to CSV
with open(os.path.join(csv_dir, 'relationships_authored.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["start_node_id", "end_node_id", "relationship_type"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(relationships_authored)

with open(os.path.join(csv_dir, 'relationships_published_in.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["start_node_id", "end_node_id", "relationship_type"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(relationships_published_in)

with open(os.path.join(csv_dir, 'relationships_has_fos.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["start_node_id", "end_node_id", "relationship_type", "weight"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(relationships_has_fos)
z
with open(os.path.join(csv_dir, 'relationships_cites.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["start_node_id", "end_node_id", "relationship_type"], lineterminator='\n')
    writer.writeheader()
    writer.writerows(relationships_cites)

print("CSV files have been generated successfully in the 'csv' directory.")
