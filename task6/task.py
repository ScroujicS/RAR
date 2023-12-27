import numpy as np
import json


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def compute_kendall_tau(experts_rankings):
    num_experts = len(experts_rankings)
    num_items = len(experts_rankings[0])

    rank_matrix = [[0 for _ in range(num_experts)] for _ in range(num_items)]
    rank_matrix_eta = [[num_items - j for _ in range(num_experts)] for j in range(num_items)]

    all_elements = sorted(experts_rankings[0])

    for i in range(num_experts):
        for j in range(num_items):
            rank_matrix[j][i] = num_items - experts_rankings[i].index(all_elements[j])

    rank_matrix = np.array(rank_matrix)
    rank_matrix_eta = np.array(rank_matrix_eta)

    disp_rank_matrix_eta = ((rank_matrix_eta.sum(axis=-1) - rank_matrix_eta.sum(axis=-1).mean()) ** 2).sum() / (
                num_items - 1)
    disp_rank_matrix = ((rank_matrix.sum(axis=-1) - rank_matrix.sum(axis=-1).mean()) ** 2).sum() / (num_items - 1)

    kendall_tau = disp_rank_matrix / disp_rank_matrix_eta

    print(disp_rank_matrix)
    print(disp_rank_matrix_eta)

    return kendall_tau


def main():
    A = read_json('A.json')
    B = read_json('B.json')
    C = read_json('C.json')

    experts_rankings = [A, B, C]

    kendall_tau_result = compute_kendall_tau(experts_rankings)
    print(kendall_tau_result)


if __name__ == "__main__":
    main()
