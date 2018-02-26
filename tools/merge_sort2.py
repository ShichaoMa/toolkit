def merge(arr, left, mid, right, temp):
    i = left
    j = mid + 1
    while i <= mid and j <=right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1


    while i <= mid:
        temp.append(arr[i])
        i += 1

    while j <= right:
        temp.append(arr[j])
        j += 1

    arr[left: left+len(temp)] = temp
    temp.clear()


def sort(arr, left=0, right=None, temp=list()):
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2
        sort(arr, left, mid, temp)
        sort(arr, mid+1, right, temp)
        merge(arr, left, mid, right, temp)

a = [5,3,1,7,3,7,0,4,8]
sort(a)
print(a)