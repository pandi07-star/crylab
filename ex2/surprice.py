def permute(nums):
    result = []
    used = [False] * len(nums)

    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return

        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])

                backtrack(current)

                current.pop()
                used[i] = False

    backtrack([])
    return result


# Example 1
nums1 = [1, 2, 3]
print(permute(nums1))

# Example 2
nums2 = [0, 1]
print(permute(nums2))

# Example 3
nums3 = [1]
print(permute(nums3))
