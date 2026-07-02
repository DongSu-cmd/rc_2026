from pathlib import Path
import numpy as np

def main():
     BASE = Path(__file__).parent
     data = np.load(BASE/ "random.npz")
     s1 = data['arr1']
     s2 = data['arr2']
     print(data['arr1'], type(data['arr1']))
     print(data['arr2'], type(data['arr2']))

if __name__ == "__main__":
        main()