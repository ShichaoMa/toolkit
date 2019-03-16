class Solution:
    def reOrderArray(self, arr):
        # write code here
        if not arr:
            return arr
        for i in range(0, len(arr)):
            if arr[i] % 2 == 0:
                for j in range(i+1, len(arr)):
                    if arr[j] % 2:
                        for k in range(i, j):
                            arr[k], arr[k+1] = arr[k+1], arr[k]
                    else:
                        break

        return arr


if __name__ == "__main__":
    Solution().reOrderArray([1, 2, 3, 4, 5, 6, 7])