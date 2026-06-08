# LRU (Least Recently Used)

**LRU** — это структура данных, используемая для кэширования элементов в соответствии с правилом: **самый давно не используемый элемент удаляется первым** при добавлении нового. Принцип работы LRU-кэша:

1. **Получение элемента** — сдвиг его в цепочке на позицию самого последнего (самого свежего) элемента.
2. **Добавление элемента** — если не достигнут максимальный размер кэша, элемент добавляется в цепочку на позицию последнего. Если лимит достигнут, удаляется самый первый (старый) элемент в цепочке, а новый добавляется на место последнего.

Для реализации LRU на практике используются две структуры данных:

- [Связанный список](./linked_list.md#связанный-список)
- [Хэш-таблица](./hash_table.md#хэш-таблица)

Связанный список требуется для отслеживания порядка использования элементов. Его свойство, обеспечивающее **O(1)** для удаления узла из любой позиции и вставки в конец (при наличии оптимизаций с указателями на голову и хвост), идеально подходит для перемещения элементов при доступе к ним. Основной проблемой связанного списка является получение элемента по ключу за **O(n)** — приходится обходить все узлы, чтобы найти требуемый элемент.

Чтобы устранить проблему временной сложности поиска узла, используют хэш-таблицу. Временная сложность добавления/получения/удаления элемента из хэш-таблицы равна **O(1)**. В качестве ключа используется имя узла, а в качестве значения — ссылка на сам узел. Любая операция с узлом связанного списка — это по сути перенацеливание указателей соседних элементов, занимающее **O(1)** времени.

Таким образом, связанный список служит для поддержания актуального порядка использования элементов, а хэш-таблица является индексом для мгновенного доступа к узлу и манипуляций с ним. Из рассуждений выше вытекает одно главное правило для LRU-кэша — **ключ должен быть хэшируемым объектом**!

---

## Ключевые особенности

LRU-кэш сочетает преимущества двух структур данных:

- **Хэш-таблица** обеспечивает мгновенный поиск элемента по ключу за **O(1)**.
- **Двусвязный список** обеспечивает быстрое перемещение элементов (удаление из любой позиции и вставка в конец) за **O(1)**.

Без хэш-таблицы поиск элемента в списке занимал бы **O(n)**. Без связанного списка отслеживание порядка использования и удаление старого элемента также занимало бы **O(n)**.

---

## Реализация в CPython

В **Python** для реализации логики LRU можно пойти как минимум тремя путями:

- Использование модуля `functools`, а именно декоратора `lru_cache`.
- Использование модуля `collections`, а именно структуры `OrderedDict`.
- Реализация связанного списка и самого LRU-кэша вручную:

<details>

```python
import typing as t


class Node:
    """Узел двусвязного списка для LRU-кэша."""

    def __init__(
        self,
        key: t.Hashable = "",
        value: t.Any = "",
        next_node: t.Self | None = None,
        prev_node: t.Self | None = None,
    ) -> None:
        self.key = key
        self.value = value
        self.next = next_node
        self.prev = prev_node

    def __str__(self) -> str:
        return f"key: {self.key}, value: {self.value}"


class DoubleLinkedList:
    """Двусвязный список с фиктивными узлами головы и хвоста."""

    def __init__(self) -> None:
        self._head = Node()
        self._tail = Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def insert_head(self, node: Node) -> None:
        """Вставка узла сразу после головы списка."""
        first_next_node = self._head.next
        node.prev = self._head
        node.next = first_next_node

        if first_next_node:
            first_next_node.prev = node
        self._head.next = node

    def append_tail(self, node: Node) -> None:
        """Добавление узла перед хвостом списка (самый свежий элемент)."""
        first_prev_node = self._tail.prev
        node.next = self._tail
        node.prev = first_prev_node

        if first_prev_node:
            first_prev_node.next = node
        self._tail.prev = node

    def remove_node(self, node: Node) -> None:
        """Удаление узла из списка."""
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.next = node.prev = None

    def pop(self) -> Node | None:
        """Извлечение последнего элемента (перед хвостом)."""
        if self._tail.prev is self._head:
            return None

        result = self._tail.prev
        if result:
            self.remove_node(result)

        return result

    def popleft(self) -> Node | None:
        """Извлечение первого элемента (после головы) — самый старый элемент."""
        if self._head.next is self._tail:
            return None

        result = self._head.next
        if result:
            self.remove_node(result)

        return result


class LRUCache:
    """LRU-кэш на основе двусвязного списка и хэш-таблицы."""

    def __init__(self, max_items: int = 3) -> None:
        self._cache: dict[t.Hashable, Node] = {}
        self._linked_list = DoubleLinkedList()
        self._capacity = max_items

    def get(self, key: t.Hashable) -> t.Any | None:
        """Получение значения по ключу. При успешном поиске элемент помечается как свежий."""
        exists_node = self._cache.get(key)
        if not exists_node:
            return None

        self._linked_list.remove_node(exists_node)
        self._linked_list.append_tail(exists_node)

        return exists_node.value

    def set(self, key: t.Hashable, value: t.Any) -> None:
        """Установка или обновление значения по ключу."""
        if key in self._cache:
            existed_node = self._cache[key]
            existed_node.value = value
            self._linked_list.remove_node(existed_node)
            self._linked_list.append_tail(existed_node)
        else:
            if len(self._cache) >= self._capacity:
                dropped_node = self._linked_list.popleft()
                if dropped_node:
                    self._cache.pop(dropped_node.key)

            new_node = Node(key, value)
            self._cache[new_node.key] = new_node
            self._linked_list.append_tail(new_node)
```

</details>

---

## Сложность операций

*Формат: `Время | Пространство`*

| Операция | Временная сложность | Пространственная сложность | Примечание |
| --- | --- | --- | --- |
| **Получение элемента (`get`)** | `O(1)` | `O(1)` | Поиск в хэш-таблице `O(1)`, перемещение узла в списке `O(1)`. |
| **Добавление элемента (`set`)** | `O(1)` | `O(1)` | Вставка в хэш-таблицу `O(1)`, добавление узла в хвост списка `O(1)`. |
| **Обновление существующего элемента** | `O(1)` | `O(1)` | Поиск в хэш-таблице `O(1)`, обновление значения и перемещение узла `O(1)`. |
| **Удаление старого элемента (eviction)** | `O(1)` | `O(1)` | Удаление из головы списка `O(1)`, удаление из хэш-таблицы `O(1)`. |
| **Проверка наличия ключа** | `O(1)` | `O(1)` | Проверка в хэш-таблице `O(1)`. |
| **Получение размера кэша** | `O(1)` | `O(1)` | Длина хэш-таблицы всегда актуальна. |

---

## LRU-кэш vs OrderedDict vs functools.lru_cache

Выбор реализации зависит от задачи:

- Если требуется **готовое решение для декорирования функций**, то правильный выбор — `functools.lru_cache`.
- Если требуется **ручное управление порядком элементов** и гибкая логика, то лучшим вариантом будет `collections.OrderedDict`.
- Если требуется **понимание внутренней работы** или кастомная логика кэширования, то стоит реализовать LRU-кэш вручную на основе двусвязного списка и хэш-таблицы.
