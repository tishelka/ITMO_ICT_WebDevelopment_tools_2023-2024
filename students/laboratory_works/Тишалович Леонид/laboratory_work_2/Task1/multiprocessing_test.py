import multiprocessing
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


def worker_function(results, start, end):
    """
    Функция рабочего процесса для вычисления суммы и добавления результата в список.

    Параметры:
    results (list): Список для сохранения результата.
    start (int): Начало диапазона.
    end (int): Конец диапазона.
    """
    result = calculate_sum(start, end)
    results.append(result)


def main():
    """
    Основная функция для вычисления суммы чисел с использованием multiprocessing.

    Создает процессы для вычисления сумм в диапазонах и выполняет их параллельно,
    затем собирает результаты и выводит общую сумму.
    """
    processes = []  # Список процессов
    start = 1  # Начало общего диапазона
    end = 1000000  # Конец общего диапазона
    step = 100000  # Шаг для разделения диапазона на поддиапазоны
    with multiprocessing.Manager() as manager:
        results = manager.list()  # Список для результатов

        for i in range(start, end, step):
            # Создаем процессы для вычисления суммы в поддиапазонах
            process = multiprocessing.Process(target=worker_function, args=(results, i, i + step))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()  # Ждем завершения всех процессов

        print("Результат Multiprocessing:", sum(results))  # Выводим общую сумму


if __name__ == "__main__":
    start_time = time.time()  # Время начала выполнения
    main()  # Запускаем основную функцию
    print("Время выполнения:", time.time() - start_time)  # Время выполнения программы
