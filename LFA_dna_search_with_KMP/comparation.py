def basic_search(dna_sequence, subsequence):
    dna_len = len(dna_sequence)
    sub_len = len(subsequence)
    positions = []
    comparisons = 0

    for i in range(dna_len - sub_len + 1):
        match = True
        for j in range(sub_len):
            comparisons += 1
            if dna_sequence[i + j] != subsequence[j]:
                match = False
                break
        if match:
            positions.append(i)
    
    return positions, comparisons
