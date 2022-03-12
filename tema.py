import time
import random
import sys


# verifica daca sirul este sortat crescator

def is_sorted(sir):
    for i in range(0, len(sir) - 1):
        if sir[i] > sir[i + 1]:
            return False
    return True


# Merge sort

def merge_sort(L):
    if len(L) > 1:
        mij = len(L) // 2
        ST = L[:mij]
        DR = L[mij:]
        merge_sort(ST)
        merge_sort(DR)

        i = j = k = 0
        while i < len(ST) and j < len(DR):
            if ST[i] < DR[j]:
                L[k] = ST[i]
                i += 1
            else:
                L[k] = DR[j]
                j += 1
            k += 1

        while i < len(ST):
            L[k] = ST[i]
            i += 1
            k += 1

        while j < len(DR):
            L[k] = DR[j]
            j += 1
            k += 1


# Count sort

def count_sort(L):
    mx = max(L)
    frecv = [0 for _ in range(mx + 1)]

    for val in L:
        frecv[val] += 1

    k = 0
    for i in range(mx + 1):
        c = frecv[i]
        while c > 0:
            L[k] = i
            c -= 1
            k += 1


# Shell sort

def shell_sort(L):
    # distantele lui Sedgewick: 4^k + 3*2^(k - 1) + 1
    distante = [1] + [4 ** x + 3 * 2 ** (x - 1) + 1 for x in range(1, 10)]
    distante.reverse()

    for dist in distante:
        for offset in range(dist):
            for i in range(offset, len(L), dist):
                aux = L[i]
                j = i
                while j >= dist and L[j - dist] > aux:
                    L[j] = L[j - dist]
                    j -= dist
                L[j] = aux


# Quick sort

def quick_sort(L, st, dr):
    if st < dr:
        pivot_poz = partition(L, st, dr)
        quick_sort(L, st, pivot_poz - 1)
        quick_sort(L, pivot_poz + 1, dr)


def partition(L, st, dr):
    rand_poz = random.randrange(st, dr)
    L[dr], L[rand_poz] = L[rand_poz], L[dr]

    i = st
    for j in range(st, dr):
        if L[j] < L[dr]:
            L[i], L[j] = L[j], L[i]
            i = i + 1
    L[dr], L[i] = L[i], L[dr]
    return i


# Radix sort

def radix_sort(L):
    mx = max(L)
    shift = 0

    while (mx >> shift) > 0:
        r_count_sort(L, shift)
        shift += 4


def r_count_sort(L, shift):
    aux = [0 for _ in range(len(L))]
    frecv = [0] * 16

    for elem in L:
        index = (elem >> shift) & 15
        frecv[index] += 1

    for i in range(1, 16):
        frecv[i] += frecv[i - 1]

    for i in range(len(L) - 1, -1, -1):
        index = (L[i] >> shift) & 15
        aux[frecv[index] - 1] = L[i]
        frecv[index] -= 1

    for i in range(len(L)):
        L[i] = aux[i]


# selecteaza functia de sortat

def select(functie):
    start = time.time()
    functie(L)
    stop = time.time()
    fout.write(
        f"{sortare}: {stop - start:.4f} secunde\t\t\tSortat corect: {'DA' if is_sorted(L) and len(L) == len(lista) else 'NU'}.\n")


# main

sys.setrecursionlimit(10 ** 6)
sortari = ['Merge sort', 'Shell sort', 'Quick sort', 'Radix sort', 'Count sort', 'Timsort python']

fin = open("input.txt")
fout = open("output.txt", 'w')

nr_teste = int(fin.readline())

for nr_test in range(nr_teste):
    fout.write(f"Testul #{nr_test + 1}:\n")

    N, MAX = [int(x) for x in fin.readline().strip().split()]
    fout.write(f"N = {N}, MAX = {MAX}\n")

    lista = [random.randint(0, MAX + 1) for _ in range(N)]
    for sortare in sortari:
        L = lista.copy()
        try:
            match sortare:
                case 'Merge sort':
                    select(merge_sort)
                case 'Shell sort':
                    select(shell_sort)
                case 'Quick sort':
                    start = time.time()
                    quick_sort(L, 0, len(L) - 1)
                    stop = time.time()
                    fout.write(
                        f"{sortare}: {stop - start:.4f} secunde\t\t\tSortat corect: {'DA' if is_sorted(L) and len(L) == len(lista) else 'NU'}.\n")
                case 'Radix sort':
                    select(radix_sort)
                case 'Count sort':
                    select(count_sort)
                case 'Timsort python':
                    start = time.time()
                    L.sort()
                    stop = time.time()
                    fout.write(
                        f"{sortare}: {stop - start:.4f} secunde\t\t\tSortat corect: {'DA' if is_sorted(L) and len(L) == len(lista) else 'NU'}.\n")
        except:
            print("eroare!")
    fout.write('\n')

fin.close()
fout.close()