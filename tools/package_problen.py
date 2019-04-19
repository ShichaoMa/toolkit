def package_problem(max_weight, values, weights, count):
    if count == 0:
        return 0
    if weights[count-1] > max_weight:
       return 0
    va1 = package_problem(max_weight-weights[count-1], values, weights, count-1) + values[count-1]
    va2 = package_problem(max_weight, values, weights, count-1)
    return max(va1, va2)

#
# def package_problem2(max_weight, values, weights, count):
#


print(package_problem(10, [6, 3, 5, 4, 6], [2, 2, 6, 5, 4], 5))