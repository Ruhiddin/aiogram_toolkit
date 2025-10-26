import json
import subprocess
from collections import defaultdict
from pathlib import Path

def run_ctags(root_dir: str, output_file: str, exclude_dirs=None):
    exclude_dirs = exclude_dirs or []
    exclude_args = []
    for d in exclude_dirs:
        exclude_args += ["--exclude=" + d]

    cmd = [
        "ctags",
        *exclude_args,
        "-R",
        "--languages=Python",
        "--fields=+KSn",
        "--output-format=json",
        root_dir
    ]
    print(f"Running ctags: {' '.join(cmd)}")
    with open(output_file, "w", encoding="utf-8") as f_out:
        subprocess.run(cmd, stdout=f_out, check=True)


def parse_ctags_ndjson(file_path: str):
    structure = lambda: {  # noqa: E731
        "functions": [],
        "classes": defaultdict(lambda: {"methods": [], "variables": []}),
        "variables": [],
    }

    tree = defaultdict(structure)

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                tag = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            if tag.get("_type") != "tag":
                continue

            kind = tag.get("kind")
            name = tag.get("name")
            path = tag.get("path")
            if not (kind and name and path):
                continue

            raw_scope = tag.get("scope")
            scope = raw_scope.get("name") if isinstance(raw_scope, dict) else raw_scope
            scope_kind = tag.get("scopeKind")

            node = tree[path]

            if kind == "function":
                if scope_kind == "class" and scope:
                    node["classes"][scope]["methods"].append(name)
                else:
                    node["functions"].append(name)

            elif kind == "variable":
                if scope_kind == "class" and scope:
                    node["classes"][scope]["variables"].append(name)
                else:
                    node["variables"].append(name)

            elif kind == "class":
                node["classes"][name]  # just initialize it

    return tree

def build_nested_tree(flat_tree):
    nested = {}

    for file_path, content in flat_tree.items():
        parts = Path(file_path).parts
        current = nested
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = content

    return nested

def print_tree(d, level=0):
    indent = "    " * level
    keys = sorted(d.keys())
    for i, key in enumerate(keys):
        is_last = i == len(keys) - 1
        branch = "└──" if is_last else "├──"
        value = d[key]

        print(f"{indent}{branch} {key}")

        if isinstance(value, dict):
            if "functions" in value:  # file node
                if value["functions"]:
                    for fn in value["functions"]:
                        print(f"{indent}    ├── def {fn}()")
                if value["variables"]:
                    for var in value["variables"]:
                        print(f"{indent}    ├── var {var}")
                if value["classes"]:
                    for cls, members in sorted(value["classes"].items()):
                        print(f"{indent}    ├── class {cls}")
                        for method in members["methods"]:
                            print(f"{indent}    │   ├── def {method}()")
                        for var in members["variables"]:
                            print(f"{indent}    │   ├── var {var}")
            else:  # folder node
                print_tree(value, level + 1)

if __name__ == "__main__":
    ROOT_DIR = "."  # or specify your folder
    TAGS_JSON = "tags.json"
    EXCLUDE_DIRS = [".venv_atk", ".git"]

    # Step 1: Run ctags to generate tags.json
    run_ctags(ROOT_DIR, TAGS_JSON, exclude_dirs=EXCLUDE_DIRS)

    # Step 2: Parse the output file
    parsed = parse_ctags_ndjson(TAGS_JSON)

    # Step 3: Build nested tree
    nested = build_nested_tree(parsed)

    # Step 4: Print the tree
    print_tree(nested)


def get_file_tree(root_dir: str='.', tags_json_file: str='tags.json', exclude_dirs: list=['venv', '.git']):
    ROOT_DIR = root_dir # or specify your folder
    TAGS_JSON = tags_json_file
    EXCLUDE_DIRS = exclude_dirs

    # Step 1: Run ctags to generate tags.json
    run_ctags(ROOT_DIR, TAGS_JSON, exclude_dirs=EXCLUDE_DIRS)

    # Step 2: Parse the output file
    parsed = parse_ctags_ndjson(TAGS_JSON)

    # Step 3: Build nested tree
    nested = build_nested_tree(parsed)

    # Step 4: Print the tree
    print_tree(nested)
