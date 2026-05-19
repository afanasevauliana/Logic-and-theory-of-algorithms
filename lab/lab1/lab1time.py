import random
import time
import csv

def f3(arr, n):
    cnt = 0
    tr = []
    for i in range(n):
        for j in range(i+1, n):
            summa2 = arr[i]+arr[j]
            for k in range(j+1, n):
                if summa2 + arr[k] == 0:
                    cnt += 1
                    tr.append((arr[i], arr[j], arr[k]))
    return cnt, tr

def main():
    n = int(input("Введите длину массива n: "))
    N = [random.randint(-100, 100) for _ in range(n)]
    cnt3, arr3 = f3(N, n)
    if len(N) < 50:
        print(f"Массив: {N}")
        print(f"Тройки: {arr3}")
    else:
        print(f"Массив: [{N[0]}, {N[1]}, {N[2]}, ..., {N[-3]}, {N[-2]}, {N[-1]}] (всего {len(N)} элементов)")
    print(f"Кол-во троек в массиве, сумма которых = 0: {cnt3}")
    #for i in range(100, 200, 10):

    return 0

if __name__ == "__main__":
    main()