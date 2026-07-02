from pathlib import Path
import numpy as np

def main():
    BASE = Path(__file__).parent
    s1 = np.random.randint(0, 10, 10, dtype=np.int8).reshape(2, 5)
    s2 = s1[1, :]
    s1 = s1[0, :]
    np.savez(BASE/ "random.npz", arr1=s1, arr2=s2)
    np.savetxt(BASE/ "random.txt", s1, fmt="%d")
    print(f"s1: {s1}, type: {type(s1)}")   
    print(f"s2: {s2}, type: {type(s2)}")

if __name__ == "__main__":
        main()
    