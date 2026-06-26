import os

def main():
    print(f"{os.name}")
    print(f"{os.getcwd()}")
    print(f"{os.listdir()}")
    folders = [name for name in os.listdir() if os.path.isdir(name)]
    print(folders)
    print(os.system("ls -al"))
    print(os.system("python3 a04_hello.py"))


if __name__ == "__main__":
        main()
