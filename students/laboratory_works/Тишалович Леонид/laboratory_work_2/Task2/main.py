import time
import asyncio
import multiprocessing_test
import threading_test
import asyncio_test


def run_multiprocessing_test():
    """
    Запуск теста с использованием multiprocessing.
    """
    print("Запуск теста с использованием multiprocessing...")
    start_time = time.time()
    multiprocessing_test.main()
    print("Время выполнения multiprocessing:", time.time() - start_time)


def run_threading_test():
    """
    Запуск теста с использованием threading.
    """
    print("Запуск теста с использованием threading...")
    start_time = time.time()
    threading_test.main()
    print("Время выполнения threading:", time.time() - start_time)


def run_asyncio_test():
    """
    Запуск теста с использованием asyncio.
    """
    print("Запуск теста с использованием asyncio...")
    start_time = time.time()
    asyncio.run(asyncio_test.main())
    print("Время выполнения asyncio:", time.time() - start_time)


if __name__ == "__main__":
    print("Начало выполнения всех тестов")

    run_multiprocessing_test()
    run_threading_test()
    run_asyncio_test()

    print("Конец выполнения всех тестов")
