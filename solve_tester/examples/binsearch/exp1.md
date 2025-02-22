The binary search algorithm is an efficient method for finding a target value in a sorted array. The provided C++ code implements this algorithm, and here's an explanation of how and why it works:

### Key Concepts of Binary Search

1. **Sorted Array Requirement**: Binary search requires that the input array is sorted. This is crucial because the algorithm relies on the order of elements to eliminate half of the search space with each iteration.

2. **Divide and Conquer**: The algorithm uses a divide-and-conquer approach. It repeatedly divides the search interval in half, which allows it to quickly narrow down the possible locations of the target value.

### Code Explanation

Here’s a breakdown of the code and how it implements binary search:

```cpp
int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0; // Start index of the search range
    int right = arr.size() - 1; // End index of the search range

    while (left <= right) { // Continue searching while the range is valid
        int mid = left + (right - left) / 2; // Calculate the middle index

        if (arr[mid] == target) {
            return mid; // Target found, return its index
        } else if (arr[mid] < target) {
            left = mid + 1; // Target is in the right half
        } else {
            right = mid - 1; // Target is in the left half
        }
    }

    return -1; // Target not found
}
```

### Step-by-Step Explanation

1. **Initialization**:
   - The variables `left` and `right` are initialized to represent the current search range within the array. `left` starts at the beginning (index 0), and `right` starts at the end (index `arr.size() - 1`).

2. **While Loop**:
   - The loop continues as long as `left` is less than or equal to `right`. This condition ensures that there are still elements to search.

3. **Finding the Middle Index**:
   - The middle index `mid` is calculated using the formula `left + (right - left) / 2`. This formula helps prevent overflow that could occur if `left` and `right` are large integers.

4. **Comparison**:
   - The value at the middle index (`arr[mid]`) is compared to the target:
     - If `arr[mid]` equals the target, the function returns `mid`, indicating that the target has been found.
     - If `arr[mid]` is less than the target, it means the target must be in the right half of the array. Therefore, `left` is updated to `mid + 1`.
     - If `arr[mid]` is greater than the target, it means the target must be in the left half of the array. Therefore, `right` is updated to `mid - 1`.

5. **Termination**:
   - If the loop exits without finding the target (i.e., `left` exceeds `right`), the function returns `-1`, indicating that the target is not present in the array.

### Efficiency

- **Time Complexity**: The time complexity of binary search is O(log n), where n is the number of elements in the array. This is because the search space is halved with each iteration.
  
- **Space Complexity**: The space complexity is O(1) for the iterative version, as it uses a constant amount of space for the variables.

### Conclusion

The code works effectively because it leverages the properties of sorted arrays and the divide-and-conquer strategy to efficiently locate the target value. By systematically narrowing down the search range, it minimizes the number of comparisons needed to find the target or determine its absence. This makes binary search a powerful algorithm for searching in sorted data structures.
