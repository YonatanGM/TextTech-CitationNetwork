import ijson
import json
import os

def build_paper_map_incremental(file_path, max_papers=100000):
    paper_map = {}
    with open(file_path, 'rb') as f:
        for i, paper in enumerate(ijson.items(f, "item")):
            if i >= max_papers:
                break
            paper_id = paper['id']
            paper_map[paper_id] = paper
    len(paper_map)
    return paper_map

def extract_papers_and_references(paper_map, initial_paper_count=50, max_depth=3):
    papers = []
    paper_ids = set()
    references = set()
    
    # Extract the initial set of papers and their references
    paper_count = 0
    for paper_id, paper in paper_map.items():
        if paper_count < initial_paper_count:
            papers.append(paper)
            paper_ids.add(paper_id)
            references.update(paper.get('references', []))
            paper_count += 1
        else:
            break

    # Iteratively expand the set of papers based on references
    for _ in range(max_depth):
        new_references = references - paper_ids
        if not new_references:
            break

        for ref_id in list(new_references):
            if ref_id in paper_map:
                paper = paper_map[ref_id]
                papers.append(paper)
                paper_ids.add(ref_id)
                references.update(paper.get('references', []))

    return papers

def make_serializable(obj):
    """
    Function to convert non-serializable objects to a serializable format.
    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return str(obj)

# Path to the large JSON file
json_file_path = './dblp.v12.json'

# Build paper map incrementally
paper_map = build_paper_map_incremental(json_file_path, max_papers=1000000)  # Limit to 100,000 papers for demonstration

# Extract papers and references
subset = extract_papers_and_references(paper_map, initial_paper_count=100, max_depth=5)

# Output the subset to a new JSON file
with open('dblp_subset.json', 'w') as outfile:
    json.dump(subset, outfile, indent=2, default=make_serializable)

print(f"Extracted {len(subset)} papers with their references.")
