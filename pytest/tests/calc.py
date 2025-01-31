import pytest
import pickle
from argparse import Namespace

def calc(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    raise ValueError("Invalid operator")

def read_pickle_data(args: Namespace) -> None:
	with open(file=args.some_random_filepath, mode="rb") as f:
        obj = pickle.load(f)
	with open(file=args.another_random_filepath, mode="rb") as f:
        obj_1 = pickle.load(f)
	return
