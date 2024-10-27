import numpy as np
import matplotlib.pyplot as plt
import random

# Data pelanggan (koordinat) dan permintaan barang
customers = {
    'A': {'demand': 50, 'location': (2, 3)},
    'B': {'demand': 30, 'location': (5, 7)},
    'C': {'demand': 70, 'location': (3, 8)},
    'D': {'demand': 60, 'location': (6, 4)},
    'E': {'demand': 40, 'location': (1, 6)},
    'F': {'demand': 20, 'location': (7, 9)},
    'G': {'demand': 30, 'location': (4, 5)},
    'H': {'demand': 90, 'location': (8, 2)}
}

# Kapasitas truk dan depot
truck_capacity = 100
depot_location = (0, 0)
num_trucks = 3

# Fungsi untuk menghitung jarak Euclidean
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Fungsi untuk menghitung panjang rute
def route_length(route):
    total_distance = euclidean_distance(depot_location, route[0]['location'])
    for i in range(1, len(route)):
        total_distance += euclidean_distance(route[i-1]['location'], route[i]['location'])
    total_distance += euclidean_distance(route[-1]['location'], depot_location)
    return total_distance

# Membuat solusi awal acak
def initial_solution(customers, truck_capacity):
    customer_list = list(customers.values())
    random.shuffle(customer_list)
    solution = []
    current_route = []
    current_load = 0
    
    for customer in customer_list:
        if current_load + customer['demand'] > truck_capacity:
            solution.append(current_route)
            current_route = []
            current_load = 0
        current_route.append(customer)
        current_load += customer['demand']
    
    if current_route:
        solution.append(current_route)
    return solution

# Menghitung total jarak solusi
def solution_distance(solution):
    return sum(route_length(route) for route in solution)

# Mendapatkan tetangga dengan swap
def get_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            if solution[i] and solution[j]:
                new_solution = [route[:] for route in solution]
                new_solution[i][0], new_solution[j][0] = new_solution[j][0], new_solution[i][0]
                neighbors.append(new_solution)
    return neighbors

# Implementasi Tabu Search
def tabu_search(customers, truck_capacity, max_iterations=100, tabu_tenure=5):
    current_solution = initial_solution(customers, truck_capacity)
    best_solution = current_solution
    best_distance = solution_distance(best_solution)
    tabu_list = []

    for _ in range(max_iterations):
        neighbors = get_neighbors(current_solution)
        neighbors = [s for s in neighbors if s not in tabu_list]
        neighbors.sort(key=solution_distance)
        
        if not neighbors:
            break
        
        current_solution = neighbors[0]
        current_distance = solution_distance(current_solution)
        
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance
        
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
    
    return best_solution, best_distance

# Visualisasi solusi dengan matplotlib
def plot_routes(routes):
    plt.figure(figsize=(10, 8))
    colors = ['b', 'g', 'r']
    for idx, route in enumerate(routes):
        x = [depot_location[0]]
        y = [depot_location[1]]
        
        for customer in route:
            x.append(customer['location'][0])
            y.append(customer['location'][1])
        
        x.append(depot_location[0])
        y.append(depot_location[1])
        
        plt.plot(x, y, marker='o', color=colors[idx % len(colors)], label=f'Truck {idx + 1}')
    
    # Plot depot
    plt.plot(depot_location[0], depot_location[1], 'ks', markersize=10, label='Depot')
    
    # Plot customers
    for name, customer in customers.items():
        plt.plot(customer['location'][0], customer['location'][1], 'ro')
        plt.text(customer['location'][0], customer['location'][1], f" {name}({customer['demand']})", fontsize=12)
    
    plt.title(f'Optimal Routes (Total Distance: {best_distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid()
    plt.show()

# Menjalankan algoritma Tabu Search
best_routes, best_distance = tabu_search(customers, truck_capacity)

# Menampilkan hasil rute optimal
print("Best Route with Minimum Distance:")
for idx, route in enumerate(best_routes):
    print(f"Truck {idx + 1}: {[f'Customer ({c['location']})' for c in route]}")
print(f"Total Distance: {best_distance:.2f}")

# Plotting rute optimal
plot_routes(best_routes)
