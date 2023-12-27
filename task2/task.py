import csv
import argparse


def read_graph_from_csv(file_path):
    graph_dict = {}
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] not in graph_dict:
                graph_dict[row[0]] = row[1:]
            else:
                graph_dict[row[0]].extend(row[1])

    return graph_dict


def get_all_keys(graph):
    all_keys = []
    for key in graph:
        if key not in all_keys:
            all_keys.append(key)
        for elem in graph[key]:
            if elem not in all_keys:
                all_keys.append(elem)

    return all_keys, len(all_keys)


def compute_matrix(graph, length):
    matrix = [[0 for _ in range(length)] for _ in range(length)]

    for key in graph:
        for value in graph[key]:
            matrix[int(key) - 1][int(value) - 1] = 1
            matrix[int(value) - 1][int(key) - 1] = -1

    return matrix


def write_csv(matrix, file_name='result.csv'):
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in matrix:
            csv_writer.writerow(row)


def process_graph(filename):
    graph_data = read_graph_from_csv(filename)
    keys, length = get_all_keys(graph_data)
    adjacency_matrix = compute_matrix(graph_data, length)

    result_matrix = [[0 for _ in range(5)] for _ in range(length)]

    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                result_matrix[i][0] += 1
                for index, value in enumerate(adjacency_matrix[j]):
                    if value == 1:
                        result_matrix[i][2] += 1
            if adjacency_matrix[i][j] == -1:
                result_matrix[i][1] += 1
                for index, value in enumerate(adjacency_matrix[j]):
                    if value == -1:
                        result_matrix[i][3] += 1
                    if value == 1 and index != i:
                        result_matrix[i][4] += 1

    write_csv(result_matrix)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('filepath')
    arguments = argument_parser.parse_args()
    process_graph(arguments.filepath)
