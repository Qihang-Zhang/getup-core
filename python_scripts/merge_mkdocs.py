import yaml

def merge_yaml_files(file1, file2, output_file):
    with open(file1, 'r') as f:
        data1 = yaml.safe_load(f)

    with open(file2, 'r') as f:
        data2 = yaml.safe_load(f)

    merged_data = {**data1, **data2}

    with open(output_file, 'w') as f:
        yaml.dump(merged_data, f)

merge_yaml_files('mkdocs_template.yml', 'personal_info.yml', 'mkdocs.yml')
