import numpy as np


def main():
    x = np.random.randint(10, size=10).reshape(2, 5)
    print(x)

    s1 = np.sum(x)
    print(s1, type(s1))
    s1 = np.mean(x)
    print(s1, type(s1)) 
    s1 = np.min(x)
    print(s1, type(s1))     
    s1 = np.max(x)
    print(s1, type(s1))

    x = [np.random.randint(0, 10) for _ in range(10)] 
    print(sum(x))
    print(min(x))
    print(max(x))

    s1 = np.var(x)
    print(f"s1: {s1}, type: {type(s1)}") 
    s1 = np.std(x)
    print(f"s1: {s1}, type: {type(s1)}")
    s1 = np.cumsum(x)
    print(f"s1: {s1}, type: {type(s1)}"             )
    s1 = np.unique(x)
    print(f"s1: {s1}, type: {type(s1)}") 
    s1 = np.sort(x)
    print(f"s1: {s1}, type: {type(s1)}")
    #s1 = np.flatten(s1)
    x = np.array(x)
    s1 = np.union1d(s1, x)
    print(f"s1: {s1}, type: {type(s1)}")
    s1 =  np.setdiff1d(s1, x)
    print(f"s1: {s1}, type: {type(s1)}")

if __name__ == "__main__":
        main()
