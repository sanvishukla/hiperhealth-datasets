import os
import re
import sys
from pydantic import ValidationError
from .models import DatasetMetadata
from .core import add_dataset

def parse_issue_body(body: str) -> DatasetMetadata:
    """
    Parse a GitHub issue body containing markdown headers into a dataset object.
    The headers correspond to the issue template fields.
    """
    fields = {
        "Name": "name",
        "Source": "source",
        "Target Skill": "target_skill",
        "Modality": "modality",
        "Access Link": "access_link",
        "Licensing": "licensing",
        "Description": "description",
        "Size": "size"
    }
    
    extracted_data = {}
    
    # We will look for headings ### Heading and grab the text until the next heading.
    for display_name, field_name in fields.items():
        # Match "### Heading\n\nContent"
        pattern = rf"###\s+{re.escape(display_name)}\s*\n+(.*?)(?=\n###|\Z)"
        match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # If the user leaves the default `_No response_` from github, handle it
            if value == "_No response_":
                value = ""
            if field_name == "access_link" and value == "":
                value = None
            extracted_data[field_name] = value

    try:
        dataset = DatasetMetadata(**extracted_data)
        return dataset
    except ValidationError as e:
        print("Failed to validate dataset from issue:", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m hiperhealth_datasets.github_parser <issue_body_file>")
        sys.exit(1)
        
    issue_file = sys.argv[1]
    with open(issue_file, "r", encoding="utf-8") as f:
        body = f.read()
        
    dataset = parse_issue_body(body)
    filepath = add_dataset(dataset)
    print(f"Dataset successfully parsed and saved to {filepath}")

if __name__ == "__main__":
    main()
