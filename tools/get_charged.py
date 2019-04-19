def charged(pay_num, money_num):
    if pay_num == 0:
        return 0
    return min(get_min(pay_num, money_num)) + 1


def get_min(pay_num, money_num):
    for money in money_num:
        last_num = pay_num - money
        if last_num < 0:
            continue
        try:
            yield charged(last_num, money_num)
        except ValueError:
            continue


def money_count(pay_num, money_num):
    try:
        return charged(pay_num, money_num)
    except ValueError:
        print("无法找零")


if __name__ == "__main__":
    print(money_count(13, [1, 3, 5]))