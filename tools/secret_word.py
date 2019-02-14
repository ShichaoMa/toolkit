
def parser(secret):
    """
    找到一个密码中， 后续的字符对应前面出现过的字符的下标
    :param secret: "abceeab"
    :return: {0： None, 1: None, 2: None, 3: None, 4: 3, 5: 1}
    """
    vals_mapping = dict()
    indices_mapping = dict()
    for index, i in enumerate(secret):
        if i in vals_mapping:
            indices_mapping[index] = vals_mapping[i]
        else:
            indices_mapping[index] = None
            vals_mapping[i] = index
    return indices_mapping


def run(long_str, secret):
    """
    判断超长的字符串中是否包含secret
    :param long_str:
    :param secret:
    :return:
    """
    sec_len = len(secret)
    sec_rs = parser(secret)
    for i in range(len(long_str) - sec_len):
        rs = parser(long_str[i: i+ sec_len])
        if rs == sec_rs:
            return "yes"
    return "no"


print(run("deabceeeab", "xyzddd"))

