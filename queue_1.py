class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def lqenqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def lqdequeue(self):
        if self.front is None:
            return "Queue is empty"
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def lqis_empty(self):
        return self.front is None

    def lq_remove_by_id(self, vehicle_id):
        current = self.front
        prev = None

        while current:
            if current.data.vehicle_id == vehicle_id:
                if prev:
                    prev.next = current.next
                else:
                    self.front = current.next

                if current == self.rear:
                    self.rear = prev

                return

            prev = current
            current = current.next

        raise ValueError(f"Vehicle with ID {vehicle_id} not found in LinkedListQueue.")
