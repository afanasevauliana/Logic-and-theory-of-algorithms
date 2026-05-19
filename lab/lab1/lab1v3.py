import random
import time
import csv
n = int(input("Введите длину массива n: "))
N = [random.randint(-100, 100) for _ in range(n)]
if len(N) < 100:
    print(N)
cnt = 0
for i in range(n):
    for j in range(i+1, n):
        summa2 = N[i]+N[j]
        for k in range(j+1, n):
            if summa2 + N[k] == 0:
                cnt += 1
                print(N[i], N[j], N[k])

print(f"Кол-во троек в массиве, сумма которых = 0: {cnt}")
