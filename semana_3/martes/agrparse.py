import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--nombre")
parser.add_argument("--edad", type=int)

args = parser.parse_args()

print(args.nombre)
print(args.edad)
