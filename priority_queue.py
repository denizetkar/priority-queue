from collections import defaultdict


class PriorityQueue:
    def __init__(
        self,
        arr=None,
        has_higher_priority=lambda x, y: x[0] < y[0],
        id_of=lambda x: x[1],
    ):
        if arr is None:
            arr = []
        self._heap = arr
        self.has_higher_priority = has_higher_priority
        self.id_of = id_of
        self._elem_idxs = defaultdict(set)
        for i, elem in enumerate(self):
            self._add_elem_idx(elem=elem, idx=i)

        self._heapify()

    def _get_elem_idxs(self, elem=None, elem_id=None):
        if elem is not None:
            elem_id = self.id_of(elem)
        return self._elem_idxs[elem_id]

    def _add_elem_idx(self, idx, elem=None, elem_id=None):
        if elem is not None:
            elem_id = self.id_of(elem)
        self._elem_idxs[elem_id].add(idx)

    def _remove_elem_idx(self, idx, elem=None, elem_id=None):
        if elem is not None:
            elem_id = self.id_of(elem)
        self._elem_idxs[elem_id].remove(idx)
        if len(self._elem_idxs[elem_id]) == 0:
            self._elem_idxs.pop(elem_id, None)

    def __len__(self):
        return len(self._heap)

    def __getitem__(self, i):
        return self._heap[i]

    @staticmethod
    def left_child_idx(i):
        return 2 * i + 1

    @staticmethod
    def right_child_idx(i):
        return 2 * i + 2

    @staticmethod
    def parent_idx(i):
        return (i - 1) // 2

    def _swap_elems(self, i, j):
        elem1, elem2 = self[i], self[j]
        self._heap[i], self._heap[j] = elem2, elem1
        self._remove_elem_idx(elem=elem1, idx=i)
        self._add_elem_idx(elem=elem1, idx=j)
        self._remove_elem_idx(elem=elem2, idx=j)
        self._add_elem_idx(elem=elem2, idx=i)

    def _bubble_up(self, i):
        while True:
            if i == 0:
                return
            parent_idx = self.parent_idx(i)
            if not self.has_higher_priority(self[i], self[parent_idx]):
                return
            self._swap_elems(parent_idx, i)
            i = parent_idx

    def _bubble_down(self, i):
        left_child_idx = self.left_child_idx(i)
        right_child_idx = self.right_child_idx(i)
        if left_child_idx >= len(self):
            return
        prio_idx = left_child_idx
        if right_child_idx < len(self):
            if self.has_higher_priority(self[right_child_idx], self[prio_idx]):
                prio_idx = right_child_idx

        if self.has_higher_priority(self[prio_idx], self[i]):
            self._swap_elems(i, prio_idx)
            self._bubble_down(prio_idx)

    def _heapify(self):
        if len(self) == 0:
            return
        max_idx = self.parent_idx(len(self) - 1)
        for idx in range(max_idx, -1, -1):
            self._bubble_down(idx)

    def _append(self, elem):
        self._add_elem_idx(elem=elem, idx=len(self))
        self._heap.append(elem)

    def put(self, elem):
        self._append(elem)
        self._bubble_up(len(self) - 1)

    def _remove_last(self):
        last_idx = len(self) - 1
        elem = self._heap.pop(last_idx)
        self._remove_elem_idx(elem=elem, idx=last_idx)
        return elem

    def pop(self):
        if len(self) == 0:
            return None
        self._swap_elems(0, len(self) - 1)
        elem = self._remove_last()
        self._bubble_down(0)
        return elem

    def update_elem(self, elem_id, new_elem):
        elem_idxs = self._get_elem_idxs(elem_id=elem_id)
        if len(elem_idxs) == 0:
            return
        idx = next(iter(elem_idxs))

        elem = self._heap[idx]
        self._heap[idx] = new_elem
        self._remove_elem_idx(elem_id=elem_id, idx=idx)
        self._add_elem_idx(elem=new_elem, idx=idx)
        if self.has_higher_priority(new_elem, elem):
            self._bubble_up(idx)
        elif self.has_higher_priority(elem, new_elem):
            self._bubble_down(idx)

    def __repr__(self) -> str:
        return repr(self._heap)
