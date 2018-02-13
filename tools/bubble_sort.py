def bubble_sort(arr):
    for i in range(len(arr)-1):
        for j in range(1, len(arr)-i):
            if arr[j-1] > arr[j]:
                arr[j-1], arr[j] = arr[j], arr[j-1]


arr = [5,3,1,7,3,7,0,4,8]
bubble_sort(arr)
print(arr)