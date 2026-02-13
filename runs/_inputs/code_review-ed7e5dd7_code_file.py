Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Implement a sorting algorithm to sort a given array.

### Input:
[3, 1, 4, 5, 9, 0]

### Response:
def bubble_sort(arr):
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
 
# Driver code to test above
arr = [3, 1, 4, 5, 9, 0]
 
bubble_sort(arr)
 
print ("Sorted array is:")
for i in range(len(arr)):
    print ("%d" %arr[i]),