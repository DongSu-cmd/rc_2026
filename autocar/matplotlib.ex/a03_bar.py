import matplotlib.pyplot as plt    
import numpy as np

def main():
    x = np.arange(100, 110)
    data = np.random.random(10)*100+30
    plt.bar(x, data)
    fig = plt.figure(figsize=(5, 5))
    ax1 = fig.add_subplot(1,1,1)
    ax1 = fig.add_subplot(1,1,2)
    ax1.bar(x, data, align="edge", edgecolor="black", color="orange", alpha=0.5, width=0.1)
    fig2 = plt.figure(figsize=(5, 5))
    ax1 = fig2.add_subplot(2,1,1)
    ax2 = fig2.add_subplot(2,1,2)
    data = np.random.random(50).reshape(5,10)
    ax1 = plt.bar(np.arange(10), data[0], color="gray" )
    ax1 = plt.bar(np.arange(10), data[1], color="yellow" )
    ax1 = plt.bar(np.arange(10), data[2], color="black" )
    ax2 = plt.bar(np.arange(0, 50, 5), data[0], color="lightgray")
    ax2 = plt.bar(np.arange(0, 50, 5)+1, data[1], color="gray")
    ax2 = plt.bar(np.arange(0, 50, 5)+2, data[2], color="black")
    fig3 = plt.figure(figsize=(5,5))
    ax1 = fig3.add_subplot(2,1,1)
    ax2 = fig3.add_subplot(2,1,2)
    plt.show()

if __name__ == "__main__":
    main()  