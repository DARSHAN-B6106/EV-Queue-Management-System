class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, arrival_time):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.arrival_time = arrival_time

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __repr__(self):
        return f"Vehicle(ID: {self.vehicle_id}, Type: {self.vehicle_type}, Arrival: {self.arrival_time})"


class MinHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        parent = self._parent(index)
        if index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def insert(self, vehicle):
        self.heap.append(vehicle)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def is_empty(self):
        return len(self.heap) == 0

    def remove_by_id(self, vehicle_id):
        for i in range(len(self.heap)):
            if self.heap[i].vehicle_id == vehicle_id:
                self.heap[i] = self.heap[-1]
                self.heap.pop()
                self._heapify_down(i)
                self._heapify_up(i)
                return
        raise ValueError(f"Vehicle with ID {vehicle_id} not found in MinHeap.")
