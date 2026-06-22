def main():
    # 사용자로부터 상품명, 가격, 할인율 입력 받기
    product_name = input("상품명을 입력하세요: ")
    
    try:
        product_price = float(input("상품 가격을 입력하세요: "))
        discount_rate = float(input("할인율을 입력하세요 (예: 20 for 20%): "))
    except ValueError:
        print("가격과 할인율은 숫자로 입력해야 합니다.")
        return

    # 할인 금액과 최종 가격 계산
    discount_amount = product_price * discount_rate / 100
    final_price = product_price - discount_amount

    # 결과 출력
    print(f"\n상품명: {product_name}")
    print(f"원래 가격: {product_price:.2f}원")
    print(f"할인율: {discount_rate:.2f}%")
    print(f"할인 금액: {discount_amount:.2f}원")
    print(f"최종 가격: {final_price:.2f}원")

if __name__ == "__main__":
    main()