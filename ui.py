import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from minheap import MinHeap
from queue_1 import LinkedListQueue
from priorq import PriorityQueue


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, arrival_time):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.arrival_time = arrival_time

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __repr__(self):
        return f"Vehicle(ID: {self.vehicle_id}, Type: {self.vehicle_type}, Arrival: {self.arrival_time})"


class VehicleManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Vehicle Management System 🚗")
        self.root.configure(bg="#f0f4f8")
        self.root.geometry("600x700")
        self.min_heap = MinHeap()
        self.priority_queue = PriorityQueue()
        self.linked_list_queue = LinkedListQueue()

        # Define the font
        self.default_font = ("Roboto", 12)

        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        frame = tk.Frame(self.root, bg="#e6f7ff", padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="🚗 Vehicle ID:", font=self.default_font, bg="#e6f7ff", fg="#004080").grid(row=0, column=0, sticky=tk.W)
        self.vehicle_id_entry = tk.Entry(frame, font=self.default_font)
        self.vehicle_id_entry.grid(row=0, column=1)

        tk.Label(frame, text="🚘 Vehicle Type:", font=self.default_font, bg="#e6f7ff", fg="#004080").grid(row=1, column=0, sticky=tk.W)
        self.vehicle_type_entry = tk.Entry(frame, font=self.default_font)
        self.vehicle_type_entry.grid(row=1, column=1)

        tk.Label(frame, text="⏰ Arrival Time (HH:MM):", font=self.default_font, bg="#e6f7ff", fg="#004080").grid(row=2, column=0, sticky=tk.W)
        self.arrival_time_entry = tk.Entry(frame, font=self.default_font)
        self.arrival_time_entry.grid(row=2, column=1)

        tk.Label(frame, text="🔋 Battery Level:", font=self.default_font, bg="#e6f7ff", fg="#004080").grid(row=3, column=0, sticky=tk.W)
        self.battery_level_entry = tk.Entry(frame, font=self.default_font)
        self.battery_level_entry.grid(row=3, column=1)

        tk.Button(frame, text="Add Vehicle", font=self.default_font, bg="#80e0a8", command=self.add_vehicle).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Display LOW BATTERY VEHICLES QUEUE(MIN-HEAP)", font=self.default_font, bg="#ffeb3d", command=self.display_min_heap).pack(fill=tk.X, pady=5)
        tk.Button(self.root, text="Display VIP/EMERGENCY VEHICLES QUEUE(PriorityQueue)", font=self.default_font, bg="#ffeb3d", command=self.display_priority_queue).pack(fill=tk.X, pady=5)
        tk.Button(self.root, text="Display REGULAR VEHICLES QUEUE(LinkedListQueue)", font=self.default_font, bg="#ffeb3d", command=self.display_linked_list_queue).pack(fill=tk.X, pady=5)

        tk.Label(self.root, text="🚫 Vehicle ID to Remove:", font=self.default_font, bg="#f0f4f8", fg="#b71c1c").pack(pady=5)
        self.remove_id_entry = tk.Entry(self.root, font=self.default_font)
        self.remove_id_entry.pack()

        tk.Button(self.root, text="Remove Vehicle", font=self.default_font, bg="#ff5722", command=self.remove_vehicle).pack(pady=10)

        self.output_text = tk.Text(self.root, height=15, width=60, font=("Courier", 12), bg="#e8f7fa", fg="#004d40")
        self.output_text.pack(padx=10, pady=10)

    def add_vehicle(self):
        vehicle_id = self.vehicle_id_entry.get().strip()
        vehicle_type = self.vehicle_type_entry.get().strip().lower()
        arrival_time = self.arrival_time_entry.get().strip()
        battery_level = self.battery_level_entry.get().strip()

        try:
            arrival_time = datetime.strptime(arrival_time, "%H:%M")
            battery_level = int(battery_level)
            vehicle = Vehicle(vehicle_id, vehicle_type, arrival_time)

            if vehicle_type in ["vip", "emergency"]:
                priority = 1 if vehicle_type == "emergency" else 2
                self.priority_queue.p_add_vehicle(vehicle, priority)
                messagebox.showinfo("Success", f"🚀 Vehicle {vehicle_id} added to PriorityQueue.")

            elif vehicle_type == "regular" and battery_level > 40:
                self.linked_list_queue.lqenqueue(vehicle)
                messagebox.showinfo("Success", f"✅ Vehicle {vehicle_id} added to LinkedListQueue.")

            elif battery_level <= 40:
                self.min_heap.insert(vehicle)
                messagebox.showinfo("Success", f"✅ Vehicle {vehicle_id} added to MinHeap.")

            else:
                messagebox.showerror("Error", "⚠️ Invalid vehicle type or conditions.")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Invalid Input: {e}")

    def display_min_heap(self):
        self.output_text.delete("1.0", tk.END)
        if self.min_heap.is_empty():
            self.output_text.insert(tk.END, "🚫 MinHeap is empty.\n")
        else:
            for vehicle in self.min_heap.heap:
                self.output_text.insert(tk.END, f"{vehicle}\n")

    def display_priority_queue(self):
        self.output_text.delete("1.0", tk.END)
        if self.priority_queue.is_empty():
            self.output_text.insert(tk.END, "🚫 PriorityQueue is empty.\n")
        else:
            for priority, vehicle in self.priority_queue.queue:
                self.output_text.insert(tk.END, f"Priority {priority}: {vehicle}\n")

    def display_linked_list_queue(self):
        self.output_text.delete("1.0", tk.END)
        current = self.linked_list_queue.front
        if not current:
            self.output_text.insert(tk.END, "🚫 LinkedListQueue is empty.\n")
        else:
            while current:
                self.output_text.insert(tk.END, f"{current.data}\n")
                current = current.next

    def remove_vehicle(self):
        vehicle_id = self.remove_id_entry.get().strip()

        try:
            self.min_heap.remove_by_id(vehicle_id)
            messagebox.showinfo("Info", f"✅ Vehicle {vehicle_id} removed from MinHeap.")
            return
        except ValueError:
            pass

        try:
            self.priority_queue.p_remove_by_id(vehicle_id)
            messagebox.showinfo("Info", f"✅ Vehicle {vehicle_id} removed from PriorityQueue.")
            return
        except ValueError:
            pass

        try:
            self.linked_list_queue.lq_remove_by_id(vehicle_id)
            messagebox.showinfo("Info", f"✅ Vehicle {vehicle_id} removed from LinkedListQueue.")
            return
        except ValueError:
            pass

        messagebox.showerror("Error", f"❌ Vehicle {vehicle_id} not found in any queue.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    app = VehicleManagementApp(root)
    root.mainloop()


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
