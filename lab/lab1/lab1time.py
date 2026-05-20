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

def average_time(len_arr):
    times = []
    for b in range(5):
        N = [random.randint(-100, 100) for p in range(len_arr)]
        start_time = time.time()
        cnt3, arr3 = f3(N, len_arr)
        end_time = time.time()
        times.append(end_time-start_time)
    times.sort()
    trim_count = int(len(times) * 0.2)
    if trim_count > 0:
        times = times[:-trim_count]
    return sum(times) / len(times)

def main():
    n = int(input("Введите длину массива n: "))
    N = [random.randint(-100, 100) for p in range(n)]
    start_time = time.time()
    cnt3, arr3 = f3(N, n)
    end_time = time.time()
    if len(N) < 50:
        print(f"Массив: {N}")
        print(f"Тройки: {arr3}")
    else:
        print(f"Массив: [{N[0]}, {N[1]}, {N[2]}, ..., {N[-3]}, {N[-2]}, {N[-1]}] (всего {len(N)} элементов)")
    print(f"Кол-во троек в массиве, сумма которых = 0: {cnt3}")
    print(f"Время выполнения алгоритма: {end_time - start_time}")
    

    print("\nИсследование временной сложности алгоритма:")
    results = []
    for c in range(20, 301, 20):
        elapsed_time = average_time(c)
        results.append([c, elapsed_time])
    
    print(f"{'Размер N':<12} {'Время выполнения (сек)'}")
    print("-" * 35)
    for row in results:
        print(f"{row[0]:<12} {row[1]:<20.6f}")
    
    csv_filename = "lab1_variant3_results.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Size", "Time"])
        writer.writerows(results)
    print(f"Результаты сохранены в файл: {csv_filename}")

    return 0

if __name__ == "__main__":
    main()