import itertools
import numpy as np
import more_itertools as mit
import numpy as np
import time


def datasum(p):
    row_sum = p.sum(axis=1) == 1                            #Rowsum and column sum =1
    column_sum = p.sum(axis=0) == 1
    # print(row_sum)
    return row_sum.all() and column_sum.all()


def partialsum(p):
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


def blocks(a): #F  # Finding positions of -1s and linking them to their blocks
    ''''
    returns the blocks and the no. of free 1's
    '''
    positive = 0
    negative = 0
    order = len(a)
    for i in a:
        positive += i.count(1)
        negative += i.count(-1)
    n = set() #set
    b = 0
    arr = {} #dictionary
    z = 0
    for i in range(1, order - 1):
        for j in range(1, order - 1):
            flag = -1
            k = set()
            if a[i][j] == -1:
                p = j
                for m in range(i - 1, -1, -1):
                    if a[m][p] == 1:
                        k.add((m, p))
                        break
                for m in range(i + 1, order):
                    if a[m][p] == 1:
                        k.add((m, p))
                        break
                for m in range(p - 1, -1, -1):
                    if a[i][m] == 1:
                        k.add((i, m))
                        break
                for m in range(p + 1, order):
                    if a[i][m] == 1:
                        k.add((i, m))
                        break
                # if len(n) + 4 == len(n.union(k)):
                    # b += 1
                for r in arr.keys():
                    for q in k:
                        if q in arr[r]['p']:
                            flag = r
                if flag != -1:  # if block has the same linked 1s, then joining them as connected blocks
                    arr[flag] = {'p': arr[flag]['p'].union(k), 'n': arr[flag]['n'] + [(i, j)]}
                else:  # new block if 1s found are unique
                    arr[z] = {'p': k, 'n': [(i, j)]}
                    z += 1
                n = n.union(k)
    print("No of blocks: ", z + positive - len(n))
    print("No of free 1's: ", positive - len(n))
    
     
    return arr, positive - len(n)


def check(p, a, comb, n):  #F # For checking if all permutations of a given matrix or block have row and column sum=1
    r = 1
    t = 2
    for i in p:
        f = 0
        matrix = [a[j] for j in i]
        data = np.matrix(matrix)
        if n == 2:
            data = np.transpose(data)
        tp = np.transpose(data)
        if negativecheck(data):
            if partialsum(data) and partialsum(tp):
                # if (tp == data).all():
                #     t = 1
                for j in comb:
                    if (data == j).all():
                        f = 1
                if f == 0:
                    r += 1
                    comb.append(data)

        tp_a = np.transpose(comb[0]) #comb 0 is the initial matrix (block)
        for i in comb:
            if(i==tp_a).all():
                t = 1
    return r, t, comb


def matform(order, pos, rmin, cmin): #F  # Forming individual blocks
    matrix = [[0 for i in range(0, order)] for i in range(0, order)]
    for j in pos['p']:
        matrix[j[0] - rmin][j[1] - cmin] = 1   
    for j in pos['n']:
        matrix[j[0] - rmin][j[1] - cmin] = -1
    ecol = []
    erow = []
    for i in range(0, order):
        f = 0
        for j in matrix[i]:
            if j != 0:
                f = 1
                break
        if f == 0:
            erow.append(i)
    matrix = np.transpose(np.matrix(matrix)).tolist()  # Finding and removing blank rows and columns while maintaing order
    for i in range(0, order):
        f = 0
        for j in matrix[i]:
            if j == 1 or j == -1:
                f = 1
                break
        if f == 0:
            ecol.append(i)
    matrix = np.transpose(np.matrix(matrix)).tolist()
    while (len(erow) == len(ecol) and len(erow) != 0):
        matrix.pop(erow[-1])
        matrix = np.transpose(np.matrix(matrix)).tolist()
        matrix.pop(ecol[-1])
        matrix = np.transpose(np.matrix(matrix)).tolist()
        erow.pop()
        ecol.pop()
    return matrix


def isomorph(k):  #F # Forming order of individual blocks and sending it to matform along with positions of 1s and -1s
    matcomb = []
    for i in k.keys():
        rmin = 1000
        cmin = 1000
        rmax = -1
        cmax = -1
        for j in k[i]['p']:
            rmin = min(rmin, j[0])
            rmax = max(rmax, j[0])
            cmin = min(cmin, j[1])
            cmax = max(cmax, j[1])
        order = max(rmax - rmin, cmax - cmin) + 1
        matcomb.append(matform(order, k[i], rmin, cmin))
    return matcomb


def asmcomb(a): #F  # Generating all possible row and column permutations  #F
    
    order = len(a)
    p = list(itertools.permutations([i for i in range(0, order)], order))
    # print ("P: ")
    # print(p)
    # print()
    comb = [np.matrix(a)]
    r, t, comb = check(p, a, comb, 1)
    a = np.transpose(np.matrix(a)).tolist()
    c, t, comb = check(p, a, comb, 2)
    # print("COMB")
    # print(comb)
    return r, c, t, comb


def binomial(n, c):  #F
    return fact(n) // (fact(c) * fact(n - c))  # binomial calculation


def fact(a):  #F
    if a == 0 or a == 1:
        return 1
    return a * fact(a - 1)  # factorial


if __name__ == "__main__":
    
    print("Enter order of matrix")
    a=[]
    order= int(input())
    for i in range(0,order):
        print(f"Enter Row {i+1} with a single space between each element")
        q=input().split()
        for j in range(0,len(q)):
            q[j]=int(q[j])
        a.append(q)
    print()
    
    if datasum(np.matrix(a)):
        k, free = blocks(a)
        iso = 0
        matcomb = isomorph(k) #contains all blocks in matrix form
        # print(matcomb)
        combarr = []   #
        for i in range(0, len(matcomb)):
            r, c, t, comb = asmcomb(matcomb[i])
            combarr.append([r, c, t, comb, len(matcomb[i]), False])
        isogroup = []
        for i in range(0, len(matcomb)):
            if not combarr[i][5]:
                for j in range(i + 1, len(matcomb)):
                    if combarr[i][4] == combarr[j][4] and (
                            combarr[i][0] * combarr[i][1] == combarr[j][0] * combarr[j][1]) and \
                            combarr[i][2] == combarr[j][2]:
                        for k in combarr[i][3]:            #traverse the comb of i
                            if (k == matcomb[j]).all():     #check if j is in comb of i 
                                if combarr[i][5] == False:
                                    combarr[i][5] = True
                                    iso += 1
                                combarr[j][5] = True
                                iso += 1
                                f = 1
                                break
                isogroup.append(iso)

        print("ISOMORPHIC BLOCKS: ", iso)
        rct = 1
        for i in range(0, len(combarr)):
            rct *= combarr[i][0] * combarr[i][1] * combarr[i][2]
            print(
                f"Block {i + 1}: Order={combarr[i][4]} Row={combarr[i][0]} Column={combarr[i][1]} Transpose={combarr[i][2]} Isomorphic={combarr[i][5]}")
        answer = 1
        for i in range(0, free):
            answer *= order ** 2
            order -= 1
        answer = answer // fact(free)
        for i in range(0, len(combarr)):
            answer *= binomial(order, combarr[i][4]) ** 2
            order = order - combarr[i][4]
        for i in isogroup:
            answer //= fact(i)
        answer *= rct
        print("ANSWER:", answer)

    else:
        print("Matrix not ASM") 


