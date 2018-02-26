def quick_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left >= right:
        return

    l = left
    r = right
    key = arr[left]
    while left < right:
        while left < right and arr[right] >= key:
            right -= 1
        arr[left] = arr[right]

        while left < right and arr[left] <= key:
            left += 1
        arr[right] = arr[left]

    arr[right] = key
    quick_sort(arr, l, right-1)
    quick_sort(arr, right+1, r)


if __name__ == "__main__":
    arr = [6,3,8,1,4,6,9,2]
    #quick(arr, 0, len(arr)-1)
    quick_sort(arr)
    print(arr)