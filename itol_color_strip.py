import argparse
import random

def generate_random_colors(num):
    return ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(num)]

def parse_files(node_subgroup_file, node_protein_file, output_file, id_file):
    node_subgroup = {}
    subfams = set()
    with open(node_subgroup_file, 'r') as f:
        next(f)
        for line in f:
            node, subgroup = line.strip().split()
            node_subgroup[node] = "sub" + subgroup
            subfams.add(subgroup)

    colors = generate_random_colors(len(subfams))
    
    node_to_protein = {}
    id_to_label = {}
    with open(node_protein_file, 'r') as f:
        next(f)
        for line in f:
            node_id, label = line.strip().split()
            protein = label.split('|')[0]
            protein_id = protein.split('(')[0]
            id_to_label[node_id] = protein_id
            

    for node, subgroup in node_subgroup.items():
        if node in id_to_label:
            node_to_protein[id_to_label[node]] = subgroup

    subfam_to_color = dict(zip(sorted(subfams), colors))
    
    ids = set()
    with open(id_file, 'r') as f:
        for line in f:
            ids.add(line.strip().split('|')[0])
    


    with open(output_file, 'w') as f:
        f.write("DATASET_COLORSTRIP\nSEPARATOR SPACE\nDATASET_LABEL SSN\nCOLOR_BRANCHES 1\nDATA\n\n")
        
        for protein_id, subgroup in node_to_protein.items():
            if protein_id in ids:
                color = subfam_to_color[subgroup.replace('sub', '')]
                f.write(f"{protein_id}|GH31 {color} {subgroup}\n")

    print(f"Generated {output_file} successfully!")

# 命令行参数处理
parser = argparse.ArgumentParser(description="Generate iTOL color files based on node-subgroup and node-protein relationships.")
parser.add_argument("node_subgroup_file", help="Path to the node-subgroup file")
parser.add_argument("node_protein_file", help="Path to the node-protein file")
parser.add_argument("output_file", help="Path to the output file")
parser.add_argument("--id_file", required=True, help="File containing the list of IDs")

args = parser.parse_args()

parse_files(args.node_subgroup_file, args.node_protein_file, args.output_file, args.id_file)
