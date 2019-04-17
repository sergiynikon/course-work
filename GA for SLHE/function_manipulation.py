def read_data_from_file(filename: str):
    file = open(filename, 'r')

    lines = file.readlines()

    A = [None] * len(lines)
    b = [None] * len(lines)
    for i in range(len(lines)):
        lines[i].replace('\n', '')
        A[i] = lines[i].split(' ')
        for j in range(len(A[i])):
            A[i][j] = int(A[i][j])

        b[i] = A[i].pop()
    return A, b

