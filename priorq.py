class PriorityQueue:
    def __init__(self):
        self.queue = []

    def p_add_vehicle(self, vehicle, priority):
        self.queue.append((priority, vehicle))
        self._bubble_up(len(self.queue) - 1)

    def _bubble_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.queue[index][0] < self.queue[parent][0]:
            self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]
            index = parent
            parent = (index - 1) // 2

    def p_remove_by_id(self, vehicle_id):
        for i in range(len(self.queue)):
            if self.queue[i][1].vehicle_id == vehicle_id:
                self.queue[i] = self.queue[-1]
                self.queue.pop()
                if i < len(self.queue):
                    self._bubble_down(i)
                    self._bubble_up(i)
                return

        raise ValueError(f"Vehicle with ID {vehicle_id} not found in PriorityQueue.")

    def is_empty(self):
        return len(self.queue) == 0
