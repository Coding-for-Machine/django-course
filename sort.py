def morge_sort(arr):
    if len(arr)<=2:
        return arr
    mid = len(arr)//2
    left = morge_sort(arr[mid:])
    right = morge_sort(arr[:mid])
    result = []
    i=j=0
    while i<len(left) and j<len(right):
        if arr[i]<arr[j]:
            result.append(arr[i])
            i+=1
        else:
            result.append(arr[j])
            j+=1
    result.append(arr[i:])
    result.append(arr[j:])
    return result

arr = [5, 1, 8, 6, 29, 789, 2, 9, 7, 78, 91]
re = morge_sort(arr)
print(re)