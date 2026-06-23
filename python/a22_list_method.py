class mylist:
        def __init__(self):
                self.myvariable1="sin"
                self.myvariable2="su"
                self.mylist=list()


        def append(self,els):
                self.mylist.append(els)


def main():
        list_a = [1,2,3]
        list_b = [4,5,6]
        print(list_a+list_b)
        print(list_a)
        list_a.extend(list_b)
        print(list_a)

        list_b.append(7)
        list_b.append(8)
        print(list_b)
        list_b.insert(1, 4.5)
        print(list_b)

        mylist_a = mylist()
        mylist_a.append("sin dong su")
        print(list_a.myvariable1, list_a.myvariable2, mylist_a.mylist)

if __name__=="__main__":
        main()