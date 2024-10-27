import numpy as np
import matplotlib.pyplot as plt
import random
import math

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
def get_neighbor(solution):
    new_solution = [route[:] for route in solution]
    # Pilih dua rute secara acak dan tukar pelanggan antara mereka
    route1, route2 = random.sample(range(len(solution)), 2)
    if new_solution[route1] and new_solution[route2]:  # Pastikan rute tidak kosong
        customer1 = random.choice(new_solution[route1])
        customer2 = random.choice(new_solution[route2])
        idx1 = new_solution[route1].index(customer1)
        idx2 = new_solution[route2].index(customer2)
        new_solution[route1][idx1], new_solution[route2][idx2] = new_solution[route2][idx2], new_solution[route1][idx1]
    return new_solution

# Implementasi Simulated Annealing
def simulated_annealing(customers, truck_capacity, initial_temp=1000, cooling_rate=0.003, max_iterations=1000):
    current_solution = initial_solution(customers, truck_capacity)
    current_distance = solution_distance(current_solution)
    best_solution = current_solution
    best_distance = current_distance
    temperature = initial_temp

    for i in range(max_iterations):
        # Dapatkan solusi tetangga
        neighbor_solution = get_neighbor(current_solution)
        neighbor_distance = solution_distance(neighbor_solution)

        # Tentukan apakah solusi tetangga diterima
        if neighbor_distance < current_distance or random.uniform(0, 1) < math.exp((current_distance - neighbor_distance) / temperature):
            current_solution = neighbor_solution
            current_distance = neighbor_distance

        # Perbarui solusi terbaik jika ditemukan solusi lebih baik
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance

        # Kurangi temperatur
        temperature *= (1 - cooling_rate)
    
    return best_solution, best_distance

# Visualisasi solusi dengan matplotlib
def plot_routes(routes, best_distance):
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

# Menjalankan algoritma Simulated Annealing
best_routes, best_distance = simulated_annealing(customers, truck_capacity)

# Menampilkan hasil rute optimal
print("Best Route with Minimum Distance:")
for idx, route in enumerate(best_routes):
    print(f"Truck {idx + 1}: {[f'Customer ({c['location']})' for c in route]}")
print(f"Total Distance: {best_distance:.2f}")

# Plotting rute optimal
plot_routes(best_routes, best_distance)
