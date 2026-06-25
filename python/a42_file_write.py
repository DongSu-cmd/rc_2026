from pathlib import path

def main():
    #print(path(__file__).parent)
    f = open(path(__file__).parent / "text.txt", "a")       #a모드 권장 
                            #(path(__file__).parent.parent / "data" / "text.txt", "a") <-원하는 위치로 text.txt가 이동
                            #with쓰면 더 안전
                            
    f.write("안녕\n")
    f.close()
    #with open(uri, "r", encoding='utf-8'parent) as f:
        #data = f.read()
        #print(data)
    #with open(uri, "a", encoding='utf-8'parent) as f:         f.seek(0)로 대제
        #while data := f.readline()
            #print(data)
        #f.seek(0) <=0바이트 시작


if __name__ == "__main__":
        main()
