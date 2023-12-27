import json
import numpy as np


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def is_value_in_kernel(value, kernel):
    for cluster in kernel:
        if value in cluster:
            return True, cluster
    return False, []

def flatten_expert_rankings(expert_rankings):
    flatten_values = []
    indexes = []
    position = 0

    for cluster in expert_rankings:
        if isinstance(cluster, int):
            cluster = [cluster]
        for value in cluster:
            flatten_values.append(value)
            indexes.append(position)
        position += 1

    return flatten_values, indexes


def build_comparison_matrix(expert_rankings):
    flatten_values, indexes = flatten_expert_rankings(expert_rankings)

    matrix_size = len(flatten_values)
    comparison_matrix = np.zeros((matrix_size, matrix_size), dtype=int)

    for i in range(matrix_size):
        for j in range(matrix_size):
            if indexes[flatten_values.index(i + 1)] <= indexes[flatten_values.index(j + 1)]:
                comparison_matrix[i][j] = 1

    return comparison_matrix


def get_kernel_of_nonequal(matrix_1, matrix_2):
    matrix_1 = np.array(matrix_1)
    matrix_2 = np.array(matrix_2)

    kernel = np.multiply(matrix_1, matrix_2)
    kernel_T = np.multiply(matrix_1.T, matrix_2.T)

    kernel_res = np.logical_or(kernel, kernel_T).astype(np.int32)
    result = []

    for i in range(len(kernel_res)):
        for j in range(len(kernel_res[i])):
            if kernel_res[i][j] == 0:
                pair = sorted([i + 1, j + 1])
                if pair not in result:
                    result.append(pair)

    conc_result = []
    visited = [0 for _ in range(len(result))]

    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            set_1 = set(result[i])
            set_2 = set(result[j])

            if set_1.intersection(set_2):
                visited[i] = 1
                visited[j] = 1
                conc_result.append(list(set_1.union(set_2)))

        if result[i] not in conc_result and visited[i] == 0:
            conc_result.append(result[i])

    return conc_result


def get_expert_result(expert_1, expert_2, kernel):
    result = []

    for i in range(len(expert_1)):
        if isinstance(expert_1[i], int):
            expert_1[i] = [expert_1[i]]
        for j in range(len(expert_2)):
            if isinstance(expert_2[j], int):
                expert_2[j] = [expert_2[j]]

            expert_1_set = set(expert_1[i])
            expert_2_set = set(expert_2[j])
            for value in expert_1[i]:
                flag, cluster = is_value_in_kernel(value, kernel)
                if flag:
                    if cluster not in result:
                        result.append(cluster)
                        break

            inter = expert_1_set.intersection(expert_2_set)
            if inter and not flag:
                if len(inter) > 1:
                    result.append(list(inter))
                else:
                    result.append(inter.pop())

    print(result)


def main():
    A = read_json('A.json')
    B = read_json('B.json')
    C = read_json('C.json')

    matrix_A = build_comparison_matrix(A)
    matrix_B = build_comparison_matrix(B)
    matrix_C = build_comparison_matrix(C)

    kernel_AB = get_kernel_of_nonequal(matrix_A, matrix_B)
    kernel_BC = get_kernel_of_nonequal(matrix_B, matrix_C)

    get_expert_result(A, B, kernel_AB)
    get_expert_result(B, C, kernel_BC)


if __name__ == '__main__':
    main()
