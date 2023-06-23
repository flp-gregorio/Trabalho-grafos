import numpy as np

def calculate_min_beacons_coverage(grid, cell_size, beacon_range):
    rows, cols = grid.shape
    num_cells_covered = np.zeros((rows, cols), dtype=bool)

    def is_cell_covered(row, col):
        return num_cells_covered[row, col]

    def mark_cells_covered(row, col):
        num_cells_covered[row, col] = True
        if row > 0:
            num_cells_covered[row - 1, col] = True
        if row < rows - 1:
            num_cells_covered[row + 1, col] = True
        if col > 0:
            num_cells_covered[row, col - 1] = True
        if col < cols - 1:
            num_cells_covered[row, col + 1] = True

    beacons = []

    while not np.all(num_cells_covered):
        uncovered_cells = np.where(~num_cells_covered)
        cell_coverage_counts = np.zeros_like(uncovered_cells[0])

        for i in range(len(uncovered_cells[0])):
            row, col = uncovered_cells[0][i], uncovered_cells[1][i]
            for beacon in beacons:
                beacon_row, beacon_col = beacon
                distance = np.sqrt((row - beacon_row) ** 2 + (col - beacon_col) ** 2) * cell_size
                if distance <= beacon_range:
                    cell_coverage_counts[i] += 1

        max_count_idx = np.argmax(cell_coverage_counts)
        row, col = uncovered_cells[0][max_count_idx], uncovered_cells[1][max_count_idx]
        beacons.append(((col + 0.5) * cell_size, (row + 0.5) * cell_size))
        mark_cells_covered(row, col)

    return beacons

# Exemplo de uso
grid = np.zeros([100, 100])

cell_size = 1.0  # Tamanho de cada célula em metros
beacon_range = 8.0  # Alcance de cada beacon em metros

beacons = calculate_min_beacons_coverage(grid, cell_size, beacon_range)
num_beacons = len(beacons)

print("Número mínimo de beacons necessários:", num_beacons)
print("Coordenadas dos beacons:")
for beacon in beacons:
    print(beacon)
