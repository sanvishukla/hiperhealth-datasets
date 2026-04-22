import argparse
import sys
from pydantic import ValidationError
from .models import DatasetMetadata
from .core import get_datasets, add_dataset, _get_registry_files

def format_dataset(ds: DatasetMetadata) -> str:
    return (
        f"Name:        {ds.name}\n"
        f"Source:      {ds.source}\n"
        f"Skill:       {ds.target_skill}\n"
        f"Modality:    {ds.modality}\n"
        f"Access Link: {ds.access_link}\n"
        f"Licensing:   {ds.licensing}\n"
        f"Description: {ds.description}\n"
        f"Size:        {ds.size}\n"
    )

def main():
    parser = argparse.ArgumentParser(description="HiperHealth Dataset Registry CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # `list` command
    list_parser = subparsers.add_parser("list", help="List available datasets")
    list_parser.add_argument("--skill", type=str, help="Filter by target skill (e.g., skin, eye)")
    list_parser.add_argument("--license", type=str, help="Filter by licensing (e.g., MIT)")

    # `add` command
    subparsers.add_parser("add", help="Interactively add a new dataset")

    # `validate` command
    subparsers.add_parser("validate", help="Validate all datasets in the registry")

    # `update-readme` command
    subparsers.add_parser("update-readme", help="Update README.md with datasets table")

    args = parser.parse_args()

    if args.command == "list":
        datasets = get_datasets(skill=args.skill, license=args.license)
        if not datasets:
            print("No datasets found matching the criteria.")
        else:
            print(f"Found {len(datasets)} dataset(s):\n")
            for i, ds in enumerate(datasets, 1):
                print(f"--- Dataset {i} ---")
                print(format_dataset(ds))
                
    elif args.command == "add":
        print("Adding a new dataset. Please provide the following details:")
        
        def get_str(prompt_msg, required=False):
            while True:
                val = input(prompt_msg).strip()
                if not val:
                    if required:
                        print("This field is required.", file=sys.stderr)
                        continue
                    return ""
                return val

        def get_url(prompt_msg, required=False):
            from pydantic import BaseModel, HttpUrl
            class Dummy(BaseModel):
                url: HttpUrl
            while True:
                val = input(prompt_msg).strip()
                if not val:
                    if required:
                        print("This field is required.", file=sys.stderr)
                        continue
                    return None
                try:
                    Dummy(url=val)
                    return val
                except ValidationError as e:
                    print(f"Invalid URL: {e.errors()[0]['msg']}", file=sys.stderr)

        try:
            name = get_str("Dataset Name (e.g., ISIC 2020) [Required]: ", required=True)
            target_skill = get_str("Target Skill (e.g., skin) [Required]: ", required=True)
            source = get_str("Source (e.g., WHO) [Optional]: ", required=False)
            modality = get_str("Modality (e.g., dermoscopy images) [Optional]: ", required=False)
            access_link = get_url("Access Link [Required]: ", required=True)
            licensing = get_str("Licensing (e.g., CC BY 4.0) [Optional]: ", required=False)
            description = get_str("Description [Optional]: ", required=False)
            size = get_str("Size (e.g., 2GB, 3000 samples) [Optional]: ", required=False)
            
            ds_data = {
                "name": name,
                "target_skill": target_skill,
                "source": source,
                "modality": modality,
                "access_link": access_link,
                "licensing": licensing,
                "description": description,
                "size": size
            }
            dataset = DatasetMetadata(**ds_data)
            filepath = add_dataset(dataset)
            print(f"\nSuccessfully added dataset at {filepath}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(1)

    elif args.command == "validate":
        files = _get_registry_files()
        if not files:
            print("No datasets found to validate.")
            sys.exit(0)
            
        print(f"Validating {len(files)} files...\n")
        errors = 0
        import json
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    DatasetMetadata(**data)
                print(f"[OK] {filepath.name}")
            except Exception as e:
                print(f"[FAIL] {filepath.name}: {e}")
                errors += 1
                
        if errors == 0:
            print("\nAll datasets are valid!")
        else:
            print(f"\nFound {errors} validation error(s).")
            sys.exit(1)

    elif args.command == "update-readme":
        from .core import ROOT_DIR
        import re

        datasets = get_datasets()
        # Group by skill
        from collections import defaultdict
        grouped = defaultdict(list)
        for ds in datasets:
            grouped[ds.target_skill.lower()].append(ds)

        markdown_tables = []
        for skill in sorted(grouped.keys()):
            markdown_tables.append(f"### {skill.title()}")
            markdown_tables.append("")
            markdown_tables.append("| Name | Source | Modality | Size | License | Link |")
            markdown_tables.append("|---|---|---|---|---|---|")
            for ds in sorted(grouped[skill], key=lambda x: x.name):
                link_text = "[Link]" + f"({ds.access_link})"
                markdown_tables.append(
                    f"| {ds.name} | {ds.source} | {ds.modality} | {ds.size} | {ds.licensing} | {link_text} |"
                )
            markdown_tables.append("")

        new_content = "\n".join(markdown_tables)
        
        readme_path = ROOT_DIR / "README.md"
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace content between markers
        pattern = r"(<!-- DATASETS_START -->\n).*?(<!-- DATASETS_END -->)"
        replacement = rf"\1\n{new_content}\n\2"
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print("README.md updated successfully.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
