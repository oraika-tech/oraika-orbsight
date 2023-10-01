import ast
import fnmatch
import os
import sys

import yaml

dirty_import_count = 0


def load_rules(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    rules = data['rules']
    flattened_rules = []
    for rule in rules:
        from_values = rule['from'] if isinstance(rule['from'], list) else [rule['from']]
        to_values = rule['to'] if isinstance(rule['to'], list) else [rule['to']]

        for from_val in from_values:
            for to_val in to_values:
                flattened_rules.append({**rule, 'from': from_val, 'to': to_val})

    return data['root-package'], flattened_rules


def check_import_rules(import_from, import_to, rules):
    for rule in rules:
        if fnmatch.fnmatch(import_from, rule['from']) and fnmatch.fnmatch(import_to, rule['to']):
            if rule['type'] == 'forbidden':
                print(f"{rule['type'].capitalize()}: {import_from} -> {import_to} :: {rule['title']}")
                global dirty_import_count
                dirty_import_count += 1
                return False
            else:
                return True


def file_to_module(file_path):
    return file_path.replace('/', '.').replace('.py', '')


def validate_file(file_path, rules):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                check_import_rules(file_to_module(file_path), n.name, rules)
        elif isinstance(node, ast.ImportFrom):
            for n in node.names:
                check_import_rules(file_to_module(file_path), f"{node.module}.{n.name}", rules)


def traverse_and_validate(root_package, rules):
    for root, _, files in os.walk(root_package):
        for file in files:
            if file.endswith(".py"):
                validate_file(os.path.join(root, file), rules)


def print_success(msg: str):
    print(f"\033[92m{msg}\033[0m")


def print_failure(msg: str):
    print(f"\033[91m{msg}\033[0m")


def main():
    root_package, rules = load_rules("rules-import.yml")
    traverse_and_validate(root_package, rules)
    if dirty_import_count:
        print_failure(f"Found {dirty_import_count} dirty imports")
        sys.exit(1)
    else:
        print_success("All imports are clean")


if __name__ == "__main__":
    main()
