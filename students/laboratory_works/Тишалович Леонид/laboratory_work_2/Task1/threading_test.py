import threading
import time


def calculate_sum(start: int, end: int) -> int:
    """
    Вычислить сумму целых чисел в диапазоне [начало, конец).

    Параметры:
    start (int): Начало диапазона (включительно).
    end (int): Конец диапазона (исключая).

    Возвращает:
    int: Сумма целых чисел в указанном диапазоне.
    """
    return sum(range(start, end))


def main():
    """
    Основная функция для вычисления суммы чисел с использованием threading.

    Создает потоки для вычисления сумм в диапазонах и выполняет их параллельно,
    затем собирает результаты и выводит общую сумму.
    """
    threads = []  # Список потоков
    start = 1  # Начало общего диапазона
    end = 1000000  # Конец общего диапазона
    step = 100000  # Шаг для разделения диапазона на поддиапазоны
    results = []

    for i in range(start, end, step):
        # Создаем потоки для вычисления суммы в поддиапазонах
        thread = threading.Thread(target=lambda q, arg1, arg2: q.append(calculate_sum(arg1, arg2)), args=(results, i, i + step))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Ждем завершения всех потоков

    print("Результат Threading:", sum(results))  # Выводим общую сумму


if __name__ == "__main__":
    start_time = time.time()  # Время начала выполнения
    main()  # Запускаем основную функцию
    print("Время выполнения:", time.time() - start_time)  # Время выполнения программы
