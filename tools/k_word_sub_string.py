def run(string, k):
    """
    给定字符串S和整数K.
    计算长度为K且包含K个不同字符的子串数

    :param string: s
    :param k:
    :return:
    """
    所有的子串数 = 0
    子串尾部对应S的索引 = -1
    子串头部对应S的索引 = 0
    for 游标 in range(len(string)):
        存在于子串中的字符索引 = string[子串头部对应S的索引: 子串尾部对应S的索引+1].find(
            string[游标])
        if 存在于子串中的字符索引 != -1:
            子串头部对应S的索引 = 子串头部对应S的索引 + 存在于子串中的字符索引 + 1
        else:
            子串尾部对应S的索引 = 游标
        if 子串尾部对应S的索引 - 子串头部对应S的索引 + 1 == k:
            所有的子串数 += 1
            子串头部对应S的索引 += 1

    return 所有的子串数


print(run("abdaeesdaegabas", 3))
