import numpy as np

def main():
    x = np.arange(40).reshape(8, 5) 
    y = np.arange(39,-1,-1).reshape(8, 5)
    z = np.linspace(30, 100, 40).reshape(8, 5)
    print(x) 
    print(y) 
    print(z)

    s1 = x + y
    s2 = x - z
    s3 = x * y
    s4 = x / z
    print(s1)
    print(s2)
    print(s3)
    print(s4)

    x = x + 5
    x = x + np.array([1, 2, 3, 4, 5])

    s5 = np.matmul(x, y.T)
    print(s5)
    s6 = np.dot(x, y.T)
    print(s6)

    A = np.array([[1, 2], [3, 4]])
    inv_A = np.linalg.inv(A)
    print(A, inv_A)
    print(A @ inv_A)

    #연립방정식 풀기
    A = np.array([[1, 2], [3, 4]])
    b = np.array([5, 6])
    x = np.linalg.solve(A, b)
    a_inv = np.linalg.inv(A)
    result = a_inv @ b
    x, y = result
    print(f"x: {x}, y: {y}")


if __name__=="__main__":
    main()