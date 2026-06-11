"""
Алгоритм: сортировка последовательности кучей.
Временная сложность: O(n log n).
Пространственная сложность: O(1).

Описание: алгоритм преобразует список в максимальную кучу, затем
последовательно извлекает максимальный элемент, помещая его в конец
отсортированной части.
"""

from typing import TypeVar

T = TypeVar("T", bound=int | float)


def _sift_down_max(heap: list[T], start_index: int, end_index: int) -> None:
    """Восстанавливает свойство максимальной кучи для поддерева.

    Элемент на позиции `start_index` «просеивается» вниз по куче до тех пор,
    пока он не окажется на месте, где оба его потомка (если они есть)
    меньше или равны ему.

    Аргументы:
        heap: список, представляющий бинарную кучу.
        start_index: индекс корня поддерева, которое нужно исправить.
        end_index: граница кучи (элементы за этой границей не участвуют).
    """
    root = start_index
    while (child_index := 2 * root + 1) < end_index:
        next_child_index = child_index + 1

        if (
            next_child_index < end_index
            and heap[child_index] < heap[next_child_index]
        ):
            child_index = next_child_index

        if heap[root] >= heap[child_index]:
            break

        heap[root], heap[child_index] = heap[child_index], heap[root]
        root = child_index


def sort_heap(input_sequence: list[T]) -> None:
    """Сортирует последовательность на месте методом сортировки кучей.

    Алгоритм состоит из двух фаз:
    1. Построение максимальной кучи из всего списка.
    2. Последовательное извлечение максимального элемента (корня кучи)
       и помещение его в конец отсортированной части списка.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
            Список изменяется на месте.

    Возвращает:
        None. Результат сортировки сохраняется во входном списке.

    Примеры:
        >>> numbers = [4, 10, 3, 5, 1]
        >>> sort_heap(numbers)
        >>> numbers
        [1, 3, 4, 5, 10]
    """
    end_index = len(input_sequence)

    # Фаза 1: построение максимальной кучи
    for index in reversed(range(end_index // 2)):
        _sift_down_max(input_sequence, index, end_index)

    # Фаза 2: извлечение элементов из кучи
    for index in reversed(range(1, end_index)):
        input_sequence[0], input_sequence[index] = (
            input_sequence[index],
            input_sequence[0],
        )
        _sift_down_max(input_sequence, 0, index)
