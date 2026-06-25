def main():
        import datetime

       # from a15_comparison_operator import main as comparison_main
      #  comparison_main()

        now = datetime.datetime.now()
        print(now)
        print(type(now))
        print(now.year)
        print(now.month)
        print(now.day)
        print(now.hour)
        print(now.minute)
        print(now.second)

        if 9 < now.hour < 12:
                print(f"지금은 {now.hour}시로 오전입니다.")
        elif now.hour < 9:
                print(f"지금은 {now.hour}로 새벽입니다.")
        else:
                print(f"지금은 {now.hour}시로 오후입니다.")

        print(now.month, type(now.month))

        if 4 <= now.month <= 5:
                print("지금은 봄입니다.")
        elif 6 <= now.month <= 8:
                print("지금은 여름입니다.")
        elif 9 <= now.month <= 11:
                print("지금은 가을입니다.")
        else:
                print("지금은 겨울입니다.")

        if now.month in [4, 5]:
            print("지금은 봄입니다.")
        elif now.month in [6, 7, 8]:
            print("지금은 여름입니다.")
        elif now.month in [9, 10, 11]:
            print("지금은 가을입니다.")
        else:
            print("지금은 겨울입니다.")

if __name__=="__main__":
        main()
