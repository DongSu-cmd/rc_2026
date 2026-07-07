import matplotlib.pyplot as plt
import numpy as np

def main():
    data1 = np.random.random(10)
    data2 = np.random.random(30).reshape(10, 3)

    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(data1)
    ax1.set_title("STAR")
    ax1.set_xlabel("scale")
    ax1.set_ylabel("distance")

    ax2 = fig.add_subplot(2,1,2) #가로, 세로, 인덱스
    ax2.plot(data2, label=["Samsung", "SKhyinx", "LG"])
    ax2.legend(loc="upper right")

    fig.show() 
    input("Enter")
    #plt.show()

if __name__=="__main__":
    main()