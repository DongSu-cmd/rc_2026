import pickle
import random
from pathlib import Path

def main():
    pickle_path = Path(__file__).parent / "random_list.pickle"
    with pickle_path.open("rb") as f:
        li = pickle.load(f)
    print(li)

if __name__ == "__main__":
        main()
