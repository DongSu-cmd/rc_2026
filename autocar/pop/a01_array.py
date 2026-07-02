import numpy as np

def main():
    arr = np.array([1, 2, 3], dtype=np.int8)
    print(type(arr), arr)
    print(arr.shape, arr.ndim, arr.dtype, arr.size)
    
    
    
if __name__=="__main__":
    main()