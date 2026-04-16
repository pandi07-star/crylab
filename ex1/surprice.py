def similarPairs(words):
    freq = {}
    
    for word in words:
        base = ord(word[0])
        pattern = []
        
        for ch in word:
            diff = (ord(ch) - base + 26) % 26
            pattern.append(str(diff))
        
        key = ",".join(pattern)
        freq[key] = freq.get(key, 0) + 1
    
    ans = 0
    for f in freq.values():
        ans += f * (f - 1) // 2
    
    return ans


# Example 1
words1 = ["fusion", "layout"]
print(similarPairs(words1))

# Example 2
words2 = ["ab", "aa", "za", "aa"]
print(similarPairs(words2))
