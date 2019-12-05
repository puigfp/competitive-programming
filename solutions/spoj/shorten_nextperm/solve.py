def next_perm(l):
    """
    Updates l in place to its next permutation (in lexicographic order).
    Returns True if l was updated, and False is there is no next permutation.
    Algorithm taken from:
    https://www.nayuki.io/page/next-lexicographical-permutation-algorithm
    """
    i = len(l) - 1
    while i > 0 and l[i-1] >= l[i]:
        i -= 1

    if i == 0:
        return False

    j = len(l) - 1
    while l[j] <= l[i - 1]:
        j -= 1

    l[i-1], l[j] = l[j], l[i-1]
    l[i:] = reversed(l[i:])

    return True

if __name__ == "__main__":
    N = int(input())
    for _ in range(N):
        input()
        word = input()
        word = list(word)
        if next_perm(word):
            print("".join(word))
        else:
            print("ERROR")
