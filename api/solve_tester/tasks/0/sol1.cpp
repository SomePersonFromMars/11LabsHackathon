#include <iostream>
#include <vector>

int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2; // To prevent overflow

        if (arr[mid] == target) {
            return mid; // Target found
        } else if (arr[mid] < target) {
            left = mid + 1; // Search in the right half
        } else {
            right = mid - 1; // Search in the left half
        }
    }

    return -1; // Target not found
}

int main() {
    int n;
    std::cerr << "Enter the number of elements in the array: ";
    std::cin >> n;

    std::vector<int> arr(n);
    std::cerr << "Enter the sorted elements of the array: ";
    for (int i = 0; i < n; ++i) {
        std::cin >> arr[i];
    }

    int target;
    std::cerr << "Enter the target value to search for: ";
    std::cin >> target;

    int result = binarySearch(arr, target);
    if (result != -1) {
        std::cerr << "Target found at index: ";
        std::cout << result << std::endl;
    } else {
        std::cerr << "Target not found. ";
        std::cout << -1 << std::endl;
    }

    return 0;
}
