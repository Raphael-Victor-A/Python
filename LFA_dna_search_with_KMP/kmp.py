def compute_lps_array(subsequence):
    length = 0
    lps = [0] * len(subsequence)
    i = 1

    while i < len(subsequence):
        if subsequence[i] == subsequence[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(dna_sequence, subsequence):
    dna_len = len(dna_sequence)
    sub_len = len(subsequence)
    lps = compute_lps_array(subsequence)
    positions = []
    comparisons = 0

    i = 0
    j = 0
    while i < dna_len:
        comparisons += 1
        if subsequence[j] == dna_sequence[i]:
            i += 1
            j += 1

        if j == sub_len:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < dna_len and subsequence[j] != dna_sequence[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions, comparisons
