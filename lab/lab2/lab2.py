import time
import csv
from sys import setrecursionlimit

setrecursionlimit(10000)  # увеличиваем лимит глубины рекурсии


# ============================================================
# 1. РЕКУРСИВНЫЙ АЛГОРИТМ (простой перебор, "в лоб")
# ============================================================
def count_recursive(step, x, y, N, targetX, targetY):
    """
    Рекурсивный подсчёт количества маршрутов.
    step - сколько шагов уже сделано
    x, y - текущие координаты
    N - всего шагов
    targetX, targetY - целевая точка
    """
    if step == N:
        return 1 if (x == targetX and y == targetY) else 0
    
    # 4 направления: Север, Юг, Восток, Запад
    return (count_recursive(step + 1, x, y + 1, N, targetX, targetY) +  # Север
            count_recursive(step + 1, x, y - 1, N, targetX, targetY) +  # Юг
            count_recursive(step + 1, x + 1, y, N, targetX, targetY) +  # Восток
            count_recursive(step + 1, x - 1, y, N, targetX, targetY))   # Запад


# ============================================================
# 2. ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ (итеративное, восходящее)
# ============================================================
def count_dp(N, targetX, targetY):
    """
    Динамическое программирование.
    Используем 2D-таблицу для текущего и следующего шага.
    """
    # Смещение координат, чтобы работать с неотрицательными индексами
    offset = N
    size = 2 * N + 1  # размер таблицы от -N до +N
    
    # Текущий шаг (k шагов)
    dp_curr = [[0] * size for _ in range(size)]
    dp_curr[offset][offset] = 1  # начальная точка (0,0)
    
    for step in range(N):
        # Следующий шаг (k+1 шагов)
        dp_next = [[0] * size for _ in range(size)]
        
        for x in range(size):
            for y in range(size):
                if dp_curr[x][y] == 0:
                    continue
                
                # Пробуем все 4 направления
                # Север (y+1)
                if y + 1 < size:
                    dp_next[x][y + 1] += dp_curr[x][y]
                # Юг (y-1)
                if y - 1 >= 0:
                    dp_next[x][y - 1] += dp_curr[x][y]
                # Восток (x+1)
                if x + 1 < size:
                    dp_next[x + 1][y] += dp_curr[x][y]
                # Запад (x-1)
                if x - 1 >= 0:
                    dp_next[x - 1][y] += dp_curr[x][y]
        
        dp_curr = dp_next
    
    # Возвращаем результат для целевой точки с учётом смещения
    return dp_curr[targetX + offset][targetY + offset]


# ============================================================
# 3. ФУНКЦИЯ ДЛЯ ЗАМЕРА ВРЕМЕНИ
# ============================================================
def measure_time(func, *args):
    """Измеряет время выполнения функции в миллисекундах"""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000


# ============================================================
# 4. ОСНОВНАЯ ПРОГРАММА
# ============================================================
def main():
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №2")
    print("Вариант 3: РОБОТ")
    print("Поиск количества программ из N команд, приводящих из (0,0) в (X,Y)")
    print("=" * 70)
    
    # Ввод параметров
    try:
        X = int(input("Введите X (цель, |X| ≤ 20): "))
        Y = int(input("Введите Y (цель, |Y| ≤ 20): "))
        max_N = int(input("Введите максимальное N (длина программы): "))
    except ValueError:
        print("Ошибка ввода! Использую значения по умолчанию: X=1, Y=1, max_N=15")
        X, Y, max_N = 1, 1, 15
    
    print(f"\nЦелевая точка: ({X}, {Y})")
    print(f"Максимальная длина программы: {max_N}")
    print("\n" + "=" * 70)
    
    # Проверка корректности
    if abs(X) > 20 or abs(Y) > 20:
        print("Предупреждение: |X| или |Y| > 20, но программа всё равно попытается выполниться.")
    
    # Результаты для таблицы
    results = []
    
    print("\n{:>4} | {:>20} | {:>20} | {:>12}".format(
        "N", "Рекурсия (мс)", "Динамическое ДП (мс)", "Результат"
    ))
    print("-" * 70)
    
    for N in range(1, max_N + 1):
        result_dp = 0
        time_dp = 0
        result_rec = None
        time_rec = None
        
        # Динамическое программирование (для всех N)
        try:
            result_dp, time_dp = measure_time(count_dp, N, X, Y)
        except Exception as e:
            result_dp = "Ошибка"
            time_dp = 0
        
        # Рекурсия (только для маленьких N, иначе слишком долго)
        # Ограничим N <= 12, чтобы программа не зависала
        if N <= 12:
            try:
                result_rec, time_rec = measure_time(count_recursive, 0, 0, 0, N, X, Y)
            except RecursionError:
                result_rec = "Глубокая рекурсия"
                time_rec = None
            except Exception as e:
                result_rec = f"Ошибка"
                time_rec = None
        else:
            result_rec = "N > 12"
            time_rec = None
        
        # Вывод в консоль
        rec_str = f"{time_rec:.4f}" if time_rec is not None else str(result_rec)
        dp_str = f"{time_dp:.4f}" if time_dp is not None else str(result_dp)
        
        print(f"{N:4} | {rec_str:>20} | {dp_str:>20} | {result_dp:>12}")
        
        # Сохраняем данные для CSV
        results.append({
            'N': N,
            'time_recursive_ms': time_rec if time_rec is not None else -1,
            'time_dp_ms': time_dp,
            'result': result_dp
        })
    
    # ============================================================
    # 5. СОХРАНЕНИЕ В CSV ФАЙЛ
    # ============================================================
    csv_filename = "robot_times.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['N', 'time_recursive_ms', 'time_dp_ms', 'result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    
    print("\n" + "=" * 70)
    print(f"Результаты сохранены в файл: {csv_filename}")
    print("\nПримечание: рекурсивный алгоритм запускается только для N ≤ 12,")
    print("так как при больших N время выполнения становится неприемлемо большим (O(4^N)).")
    print("Динамическое программирование работает эффективно для всех N (O(N^3)).")
    print("=" * 70)
    
    # ============================================================
    # 6. ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ДЛЯ БОЛЬШИХ N
    # ============================================================
    print("\nДополнительные замеры для больших N (только ДП):")
    print("-" * 50)
    for N in [20, 30, 40, 50]:
        _, time_dp = measure_time(count_dp, N, X, Y)
        print(f"N = {N:2}: время ДП = {time_dp:.4f} мс")
    
    print("\nГотово! Используйте данные из CSV для построения графиков.")


if __name__ == "__main__":
    main()