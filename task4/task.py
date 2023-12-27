import math


def generate_values_matrix():
    sums_set = set()
    products_set = set()

    for i in range(1, 7):
        for j in range(1, 7):
            sums_set.add(i + j)
            products_set.add(i * j)

    sums_values = sorted(list(sums_set))
    products_values = sorted(list(products_set))

    matrix = [[0 for _ in range(len(products_values))] for _ in range(len(sums_values))]

    for i in range(1, 7):
        for j in range(1, 7):
            sum_ij = i + j
            prod_ij = i * j
            matrix[sums_values.index(sum_ij)][products_values.index(prod_ij)] += 1

    return matrix


def calculate_probability_matrix(matrix):
    total_outcomes = 36
    for row in matrix:
        for j in range(len(row)):
            row[j] /= total_outcomes

    return matrix


def compute_single_entropy(matrix, by='row'):
    entropy = 0.0

    if by == 'row':
        for i in range(len(matrix)):
            h = 0.0
            for value in matrix[i]:
                if value != 0.0:
                    h += value

            h = -1 * h * math.log2(h)
            entropy += h

    elif by == 'column':
        for i in range(len(matrix[0])):
            h = 0.0
            for j in range(len(matrix)):
                if matrix[j][i] != 0.0:
                    h += matrix[j][i]

            h = -1 * h * math.log2(h)
            entropy += h

    return entropy


def compute_joint_entropy(matrix):
    entropy = 0.0
    for i in range(len(matrix)):
        h = 0.0
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0.0:
                h += -1 * matrix[i][j] * math.log2(matrix[i][j])
        entropy += h

    return entropy


def compute_conditional_entropy(matrix, probability_matrix):
    conditional_prob_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            conditional_prob_matrix[i][j] = matrix[i][j] / sum(matrix[i])

    entropy = 0.0
    for i in range(len(conditional_prob_matrix)):
        h_si = 0.0
        for j in range(len(conditional_prob_matrix[i])):
            if conditional_prob_matrix[i][j] != 0.0:
                h_si += -1 * conditional_prob_matrix[i][j] * math.log2(conditional_prob_matrix[i][j])
        h = h_si * sum(probability_matrix[i])
        entropy += h

    return entropy


def perform_information_theory_analysis():
    matrix = generate_values_matrix()

    probability_matrix = calculate_probability_matrix(matrix)

    entropy_A = compute_single_entropy(probability_matrix, by='row')
    entropy_B = compute_single_entropy(probability_matrix, by='column')

    entropy_AB = compute_joint_entropy(probability_matrix)

    entropy_B_A = compute_conditional_entropy(matrix, probability_matrix)

    information_A_B = entropy_B - entropy_B_A

    return entropy_A, entropy_B, entropy_AB, entropy_B_A, information_A_B


if __name__ == '__main__':
    result = perform_information_theory_analysis()
    print(result)
