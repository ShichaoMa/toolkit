def retry_for(times):
    def wrapper(func):

        def inner(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except TimeoutError as e:
                    import time
                    if count < times:
                        time.sleep(1)
                        count += 1
                    else:
                        break
            raise e
        return inner
    return wrapper


@retry_for(2)
def fun():
    print("start")
    raise TimeoutError()


# fun()


def lower_bound(arr, target, start=0, end=None):
    if end is None:
        end = len(arr) - 1
    if start >= end:
        return -1

    mid = (end + start) // 2
    if target == arr[mid]:
        return mid
    if target < arr[mid]:
        index = lower_bound(arr, target, start, mid)
        if index == -1:
            return mid
        else:
            return index
    else:
        index = lower_bound(arr, target, mid + 1, end)
        if index == -1:
            return end
        else:
            return index


def split(num):
    nums = []
    while num:
        nums.insert(0, num % 10)
        num //= 10
    return nums


def gather(nums):
    num = 0
    for i in nums:
        num = (num * 10 + i)
    return num


def adjust(num):
    max_index = None
    nums = split(num)
    for i in range(len(nums)):
        for j in range(len(nums) - 1, i, -1):
            if nums[i] < nums[j]:
                max_index = j
        if max_index is not None:
            nums[i], nums[max_index] = nums[max_index], nums[i]
            return gather(nums)
    else:
        return num



print(adjust(2736))


def adjust_2(num):
    nums = split(num)
    start = 0
    end = len(nums) - 2
    min_index = None
    max_index = None
    while start < end:
        if min_index is None and nums[start+1] < nums[start]:
            pass
        elif min_index is None:
            min_index = start
            max_index = start + 1
        elif nums[start+1] > nums[start]:
            max_index = start + 1

        start += 1

    if min_index is None:
        raise RuntimeError()
    else:
        for i in range(min_index+1):
            if nums[max_index] > nums[i]:
                nums[max_index], nums[i] = nums[i], nums[max_index]
                return gather(nums)






print(adjust_2(2736))

#
# def regex(pat, string):
#     if "*"

class Solution:

    @staticmethod
    def _get_max_bit(num):
        """
        如: 1234 -> 1000,
            89321 -> 10000
        :param num:
        :return:
        """
        bit = 1
        num //= 10
        while num:
            bit *= 10
            num //= 10
        return bit

    def NumberOf1Between1AndN_Solution(self, num):
        """
        递归法，将输入的数字以最大位取整的值将此数分为两部分，如：
        43123按10000分隔成0-9999和10000-43123两部分分别取值。
        :param num:
        :return:
        """
        if num <= 0:
            return 0
        if num < 10:
            return 1

        max_bit_num = self._get_max_bit(num)
        count = 0
        # num = 9999时的1的个数
        per = self.NumberOf1Between1AndN_Solution(max_bit_num - 1)
        # 由于43123 > 9999, 所以先加上
        count += per
        # 接下来求第二部分的数
        last = (num - max_bit_num)
        # 若num 是这种形式1xxxx...，即说明首位是1的数和last是一样多的 ，
        # 同时还要加上一个1000...,对于除去1后并部分中的1，递归求之。
        if num < max_bit_num * 2:
            count += (last + 1 + self.NumberOf1Between1AndN_Solution(last))
        # 否则，1开头的是满的，也就是说有max_bit_num个，加上，同时per是少一位的999...
        # 找出余下的有几个per，由于未达到满per的，递归求之。
        else:
            times = (last // max_bit_num)
            count += (max_bit_num + times * per +
                      self.NumberOf1Between1AndN_Solution(
                last - times * max_bit_num))
        return count


print(Solution().NumberOf1Between1AndN_Solution(21345))