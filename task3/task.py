import csv
import argparse
import math


def read_matrix_from_csv(file_path):
    matrix = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            matrix.append(row)

    return matrix


def compute_probability_matrix(matrix):
    probability_matrix = []
    n = len(matrix)
    for row in matrix:
        temp_probs = []
        for value in row:
            temp_probs.append(float(value) / (n - 1))

        probability_matrix.append(temp_probs)

    return probability_matrix


def compute_entropy_for_row(probability_matrix):
    entropies = []

    for row in probability_matrix:
        h = 0.0
        for value in row:
            if value != 0.0:
                h += -1 * value * math.log2(value)

        entropies.append(h)

    return entropies


def calculate_entropy(matrix):
    prob_matrix = compute_probability_matrix(matrix)
    entropies = compute_entropy_for_row(prob_matrix)

    entropy = sum(entropies)

    return entropy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path to the CSV file containing the matrix')
    args = parser.parse_args()

    input_matrix = read_matrix_from_csv(args.filepath)
    result = calculate_entropy(input_matrix)
    print(result)
