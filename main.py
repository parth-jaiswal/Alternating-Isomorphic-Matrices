import more_itertools as mit
import numpy as np
import time


def datasum(p):
    row_sum = p.sum(axis=1) == 1                            #Rowsum and column sum =1
    column_sum = p.sum(axis=0) == 1
    return row_sum.all() and column_sum.all()


def adjacentsum(p):
    p=np.array(p)
    for i in p:                                             # condition for asm
        sum = 0
        for j in i:
            sum += j
            if sum not in[0,1]:
                return False
    return True


def negativecheck(p):
    first_r = p[0]                                          # 1st and last rows and columns should not have -1
    first_c = p[:, 0]
    last_c = p[:, len(p) - 1]
    last_r = p[len(p) - 1]
    if -1 in first_r or -1 in first_c or -1 in last_r or -1 in last_c:
        return False
    return True


def comp_array(a, m):                                       # checking for transpose
    for j in m:
        if (a == j).all():
            return False
    return True


if __name__ == "__main__":
    order = int(input("Please Enter Order of Matrix:"))
    negative = int(input("Please Enter number of -1's:"))

    if negative > (order ** 2 - order) // 2:
        print(0)
    else:
        l = [-1] * negative + [0] * (order ** 2 - order - 2 * negative) + [1] * (order + negative)
        c = 0
        matrix_comb = list(mit.distinct_permutations(l))  # generation all permutations
        comb = []
        print("Possible matrices:", len(matrix_comb))
        print("Running all combinations now:")
        time1 = time.time()
        for i in matrix_comb:
            data = np.array(i)
            data = np.reshape(data, (order, order))     #reshaping permutations into matrices
            if negativecheck(data):
                if datasum(data) and adjacentsum(data) and adjacentsum(np.transpose(data)):   #calling functions to check for asm
                    c += 1
                    comb.append(data) # storing all asms in an array
        # l = 0
        # for j, i in enumerate(comb):
        #     data_t = np.transpose(i)
        #     if comp_array(data_t, comb[j:]):
        #         #if comp_array(np.rot90(data, k=1, axes=(0, 1)), comb[j:]) and comp_array(
        #           #      np.rot90(data, k=2, axes=(0, 1)), comb[j:]) and comp_array(np.rot90(data, k=3, axes=(0, 1)),
        #            #                                                                comb[j:]):
        #         l += 1
        #             # print(i, end="\n\n")
        print("Time taken: ", time.time() - time1)
        print("Total ASMs: ", c)
        # print("Total ASMs without lrs: ", l)
