#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for i in range(length):
        if weights[i] < limit:
            next

        for j in range(length):
            if j != i:
                total = weights[i] + weights[j]
                if total == limit:
                    max_weight = max([weights[i], weights[j]])
                    min_weight = min([weights[i], weights[j]])
                    return (weights.index(max_weight), weights.index(min_weight))

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
