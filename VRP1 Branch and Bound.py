import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations

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

# Fungsi Branch and Bound untuk mencari rute optimal
def branch_and_bound(customers, truck_capacity):
    best_routes = []
    min_distance = float('inf')
    best_solution = None

    # Mencoba semua kombinasi rute (brute-force untuk masalah kecil)
    customer_list = list(customers.values())
    for perm in permutations(customer_list):
        route = []
        current_load = 0
        temp_route = []
        
        # Membagi rute sesuai kapasitas truk
        for customer in perm:
            if current_load + customer['demand'] > truck_capacity:
                route.append(temp_route)
                current_load = 0
                temp_route = []
            temp_route.append(customer)
            current_load += customer['demand']
        if temp_route:
            route.append(temp_route)

        # Menghitung jarak total
        total_distance = sum(route_length(r) for r in route)
        
        # Memperbarui solusi terbaik jika ditemukan rute yang lebih pendek
        if total_distance < min_distance:
            min_distance = total_distance
            best_solution = route
    
    return best_solution, min_distance

# Menjalankan algoritma Branch and Bound
best_routes, min_distance = branch_and_bound(customers, truck_capacity)

# Visualisasi hasil dengan matplotlib
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
    
    plt.title(f'Optimal Routes (Total Distance: {min_distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid()
    plt.show()

# Menampilkan hasil rute optimal
print("Best Route with Minimum Distance:")
for idx, route in enumerate(best_routes):
    print(f"Truck {idx + 1}: {[f'Customer ({c['location']})' for c in route]}")
print(f"Total Distance: {min_distance:.2f}")

# Plotting rute optimal
plot_routes(best_routes)
