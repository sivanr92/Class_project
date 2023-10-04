import argparse
import random

def random_color():
    return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def assign_colors(data):
    unique_ecs = sorted(set(data.values()))
    color_mapping = {ec: random_color() for ec in unique_ecs}
    return color_mapping

def main(args):
    data = {}

    with open(args.input, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            data[parts[0]] = parts[1]

    color_mapping = assign_colors(data)

    with open(args.output, 'w') as f:
        f.write("DATASET_COLORSTRIP\nSEPARATOR SPACE\nDATASET_LABEL SSN\nCOLOR_BRANCHES 0\nDATA\n")
        for key, value in data.items():
            f.write(f"{key} {color_mapping[value]} {value}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert data to iTOL color strip format.")
    parser.add_argument('--input', required=True, help='Path to the input file.')
    parser.add_argument('--output', required=True, help='Path to the output file.')
    args = parser.parse_args()
    main(args)
