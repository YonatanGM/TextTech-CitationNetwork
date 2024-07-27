# TextTech-CitationNetwork

## Original Dataset
Original dataset from Kaggle: [Citation Network Dataset](https://www.kaggle.com/datasets/mathurinache/citation-network-dataset) (dblp.v12.json \ 4,894,081 papers \ 12.52 GB)

## Data Preparation

### extract_papers.py
- This script incrementally reads the large JSON from Kaggle (dblp.v12.json) to build a map of 1,000,000 papers, extracts an initial set of 100 papers from the map, then expands the set by following references up to 5 levels deep, and saves the extracted subset to dblp.v12.12642.json
- Output: 12642 papers
- Goal was to make the dataset smaller and get a somewhat connected graph.

### json_to_xml_encoder.py
- Reads the dblp.v12.12642.json, creates XML representations for each paper, reconstructs abstracts, validates these XMLs against the dblp_paper_schema.xsd schema, and saves the valid XML files in ./xml directory
- Output: 7694 valid papers

### dblp_paper_schema.xsd
- Specifies the structure and datatypes for the XML representation of the papers. Restrictions include n_citation being an integer >= 1, doi and abstract must have a minimum length, references must contain at least one reference, etc.

### xml_to_csv_neo4j.py
- Reads the valid XML files from ./xml and extracts nodes (papers, authors, venues, fields of study) and relationships (authored, published in, has FOS, cites). Writes this data to CSV files under ./csv (nodes_paper.csv, nodes_author.csv, nodes_venue.csv, nodes_fos.csv, relationships_authored.csv, relationships_published_in.csv, relationships_has_fos.csv, relationships_cites.csv). These files are then loaded into Neo4j AuraDB instance using Cypher LOAD CSV commands.

## Neo4j DB Access
The AuraDB instance is running and you can explore the data and test cypher queries on it.
To access the instance, use the credentials below:
- First go here: [Neo4j Connection](https://workspace-preview.neo4j.io/connection/connect)
- Connection URL: `6095dc87.databases.neo4j.io:7687`
- Database User: `neo4j`
- Password: `APGMB_0ZIYaw8PFXq_Cy3utL7AoEClikHFR-xMaxk2E`

### Example Queries

#### Citation Network
```cypher
WHERE p.title = $titleOrDoi OR p.doi = $titleOrDoi
CALL apoc.path.subgraphAll(p, {
    maxLevel: $depth,
    relationshipFilter: "CITES>"
})
YIELD nodes, relationships
RETURN nodes, relationships
```

#### Influential Authors
```cypher
MATCH (a:Author)-[:AUTHORED]->(p:Paper)-[:HAS_FOS]->(f:FieldOfStudy)
WHERE f.name = $fieldName
RETURN a.name AS Author, COUNT(p) AS Papers
ORDER BY Papers DESC
LIMIT 10
```

## Website
The website is finished and you can access it here: [TextTech Citation Network](https://texttech-citationnetwork.web.app)
We used Firebase hosting and Firebase functions.

### Frontend
- `Firebase/public/index.html` — Defines the website structure, including input fields, result display sections, and graph visualization with D3.js.
- `Firebase/public/xml/` — The folder of valid XML files hosted here.
- `public/paper.xsl` — When a node is from a queried subgraph clicked, the corresponding XML file is fetched and transformed using this stylesheet to display detailed paper information on the website.

### Backend
- `Firebase/functions/index.js` — Contains the Firebase functions for handling user requests, connecting to the Neo4j AuraDB instance, and executing Cypher queries. The functions include `queryCitationNetwork`, `queryVenueImpact`, and `queryInfluentialAuthors`.
