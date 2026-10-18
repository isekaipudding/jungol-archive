# 링크 : https://jungol.co.kr/problem/12318
import sys
import time

# 에디토리얼 : https://infossm.github.io/blog/2025/01/31/problem-solving-22222/
# 참고 소스 코드 : https://lamp2357.tistory.com/31

try:
    sys.set_int_max_str_digits(1000000)
except Exception:
    pass


def divide_with_rounding(numerator:int, denominator:int) -> int:
    if denominator == 0:
        raise ZeroDivisionError
    if numerator >= 0:
        return (numerator + denominator // 2) // denominator
    return -(((-numerator) + denominator // 2) // denominator)


def multiply_and_divide_with_rounding(first_value:int, second_value:int, denominator:int) -> int:
    return divide_with_rounding(first_value * second_value, denominator)


def binary_search_rounded_square_root(target_squared:int, lower_bound:int, upper_bound:int) -> int:
    left_pointer:int = lower_bound
    right_pointer:int = upper_bound
    floor_root:int = lower_bound

    while left_pointer <= right_pointer:
        middle_candidate:int = (left_pointer + right_pointer) // 2
        candidate_squared:int = middle_candidate * middle_candidate
        if candidate_squared <= target_squared:
            floor_root = middle_candidate
            left_pointer = middle_candidate + 1
        else:
            right_pointer = middle_candidate - 1

    lower_square:int = floor_root * floor_root
    upper_square:int = (floor_root + 1) * (floor_root + 1)
    if target_squared - lower_square > upper_square - target_squared:
        return floor_root + 1
    return floor_root


def build_binomial_tables(maximum_degree:int) -> tuple:
    binomial_table:list = [[0] * (maximum_degree + 1) for _ in range(maximum_degree + 1)]
    binomial_by_column:list = [[0] * (maximum_degree + 1) for _ in range(maximum_degree + 1)]

    for row_index in range(maximum_degree + 1):
        binomial_table[row_index][0] = 1
        binomial_by_column[0][row_index] = 1
        for column_index in range(1, row_index + 1):
            combination_value:int = (
                binomial_table[row_index - 1][column_index - 1]
                + binomial_table[row_index - 1][column_index]
            )
            binomial_table[row_index][column_index] = combination_value
            binomial_by_column[column_index][row_index] = combination_value

    return binomial_table, binomial_by_column


def build_power_of_two_minus_one(maximum_degree:int) -> list:
    power_of_two_minus_one:list = [0] * (maximum_degree + 1)
    current_power:int = 1
    for total_degree in range(1, maximum_degree + 1):
        current_power <<= 1
        power_of_two_minus_one[total_degree] = current_power - 1
    return power_of_two_minus_one


def build_expected_moment_table(
    maximum_degree:int,
    fixed_point_scale:int,
    binomial_table:list,
    binomial_by_column:list,
    power_of_two_minus_one:list
) -> list:
    half_degree:int = maximum_degree // 2
    expected_moment_table:list = [[0] * (maximum_degree + 1) for _ in range(half_degree + 1)]
    expected_moment_table[0][0] = fixed_point_scale

    # row_transition_by_column[q][i] = sum_{j == i (mod 6), j <= q} C(q, j) * E[D^i (D*)^j]
    # 연속 메모리 참조 및 내적 고속화를 위해 인덱스를 [second_exponent][row_index] 순으로 배치
    row_transition_by_column:list = [[0] * (half_degree + 1) for _ in range(maximum_degree + 1)]
    for target_degree in range(maximum_degree + 1):
        row_transition_by_column[target_degree][0] = fixed_point_scale

    multiply_integers = int.__mul__

    for total_degree in range(2, maximum_degree + 1, 2):
        end_first_exponent:int = total_degree // 2
        remainder_degree:int = total_degree % 6

        start_first_exponent:int = 0
        while start_first_exponent <= end_first_exponent:
            if (2 * start_first_exponent) % 6 == remainder_degree:
                break
            start_first_exponent += 1

        if start_first_exponent > end_first_exponent:
            continue

        denominator_factor:int = 3 * power_of_two_minus_one[total_degree]

        for first_exponent in range(start_first_exponent, end_first_exponent + 1, 3):
            second_exponent:int = total_degree - first_exponent
            binomial_row_first:list = binomial_table[first_exponent]
            binomial_row_second:list = binomial_table[second_exponent]
            transition_column:list = row_transition_by_column[second_exponent]

            # C 레벨 벡터 내적으로 first_partial_sum 고속 계산
            first_partial_sum:int = sum(
                map(
                    multiply_integers,
                    binomial_row_first[:first_exponent],
                    transition_column[:first_exponent]
                )
            )

            second_partial_sum:int = 0
            remainder_first:int = first_exponent % 6
            for column_index in range(remainder_first, second_exponent, 6):
                moment_value:int = (
                    expected_moment_table[first_exponent][column_index]
                    if first_exponent <= column_index
                    else expected_moment_table[column_index][first_exponent]
                )
                if moment_value:
                    second_partial_sum += binomial_row_second[column_index] * moment_value

            total_moment_sum:int = first_partial_sum + second_partial_sum
            current_moment:int = divide_with_rounding(2 * total_moment_sum, denominator_factor)
            expected_moment_table[first_exponent][second_exponent] = current_moment

            if current_moment == 0:
                continue

            binomial_column_second:list = binomial_by_column[second_exponent]
            upper_target_limit:int = maximum_degree - first_exponent
            for target_degree in range(second_exponent, upper_target_limit + 1):
                row_transition_by_column[target_degree][first_exponent] += (
                    binomial_column_second[target_degree] * current_moment
                )

            if first_exponent != second_exponent and second_exponent < half_degree:
                binomial_column_first:list = binomial_by_column[first_exponent]
                symmetric_upper_limit:int = maximum_degree - second_exponent
                for target_degree in range(second_exponent + 1, symmetric_upper_limit + 1):
                    row_transition_by_column[target_degree][second_exponent] += (
                        binomial_column_first[target_degree] * current_moment
                    )

    nonzero_moment_items:list = []
    for first_exponent in range(half_degree + 1):
        max_second_exponent:int = maximum_degree - first_exponent
        for second_exponent in range(first_exponent, max_second_exponent + 1):
            moment_value = expected_moment_table[first_exponent][second_exponent]
            if moment_value != 0:
                weighted_moment:int = moment_value if first_exponent == second_exponent else moment_value * 2
                nonzero_moment_items.append((first_exponent, second_exponent, weighted_moment))

    return nonzero_moment_items


def build_square_root_taylor_coefficients(maximum_degree:int, fixed_point_scale:int) -> list:
    taylor_coefficients:list = [0] * (maximum_degree + 1)
    taylor_coefficients[0] = fixed_point_scale
    for degree_index in range(1, maximum_degree + 1):
        previous_coefficient:int = taylor_coefficients[degree_index - 1]
        numerator:int = previous_coefficient * (3 - 2 * degree_index)
        denominator:int = 2 * degree_index
        taylor_coefficients[degree_index] = divide_with_rounding(numerator, denominator)
    return taylor_coefficients


def multiply_scaled_complex(
    first_real:int,
    first_imaginary:int,
    second_real:int,
    second_imaginary:int,
    fixed_point_scale:int
) -> tuple:
    next_real:int = (
        multiply_and_divide_with_rounding(first_real, second_real, fixed_point_scale)
        - multiply_and_divide_with_rounding(first_imaginary, second_imaginary, fixed_point_scale)
    )
    next_imaginary:int = (
        multiply_and_divide_with_rounding(first_real, second_imaginary, fixed_point_scale)
        + multiply_and_divide_with_rounding(first_imaginary, second_real, fixed_point_scale)
    )
    return next_real, next_imaginary


def compute_jiae_constant(maximum_degree:int, output_digits:int, scale_exponent:int) -> str:
    fixed_point_scale:int = 10 ** scale_exponent
    fixed_point_scale_squared:int = fixed_point_scale * fixed_point_scale

    binomial_table, binomial_by_column = build_binomial_tables(maximum_degree)
    power_of_two_minus_one:list = build_power_of_two_minus_one(maximum_degree)
    nonzero_moment_items:list = build_expected_moment_table(
        maximum_degree,
        fixed_point_scale,
        binomial_table,
        binomial_by_column,
        power_of_two_minus_one
    )
    taylor_coefficients:list = build_square_root_taylor_coefficients(maximum_degree, fixed_point_scale)

    # 1.732 < sqrt(3) < 1.733 수학적 보장 구간에서만 이진 탐색 수행
    scaled_sqrt_three:int = binary_search_rounded_square_root(
        3 * fixed_point_scale_squared,
        1732 * (fixed_point_scale // 1000),
        1733 * (fixed_point_scale // 1000)
    )
    half_scale:int = fixed_point_scale // 2
    quarter_scale:int = fixed_point_scale // 4

    unit_rotation_real:int = half_scale
    unit_rotation_imaginary:int = divide_with_rounding(scaled_sqrt_three, 2)

    sixth_root_powers:list = [(fixed_point_scale, 0)]
    current_real:int = fixed_point_scale
    current_imaginary:int = 0
    for _ in range(2):
        current_real, current_imaginary = multiply_scaled_complex(
            current_real,
            current_imaginary,
            unit_rotation_real,
            unit_rotation_imaginary,
            fixed_point_scale
        )
        sixth_root_powers.append((current_real, current_imaginary))

    # 4개 케이스의 |U_eval| 탐색 구간을 수학적 상·하한으로 고정 (유리수 케이스는 즉시 확정)
    branch_cases:list = [
        (0, 0, 1, 3, half_scale, half_scale),
        (sixth_root_powers[0][0], sixth_root_powers[0][1], 1, 9, 3 * quarter_scale, 3 * quarter_scale),
        (
            sixth_root_powers[1][0],
            sixth_root_powers[1][1],
            2,
            9,
            661 * (fixed_point_scale // 1000),
            662 * (fixed_point_scale // 1000)
        ),
        (
            sixth_root_powers[2][0],
            sixth_root_powers[2][1],
            2,
            9,
            433 * (fixed_point_scale // 1000),
            434 * (fixed_point_scale // 1000)
        ),
    ]

    accumulated_expectation:int = 0

    for (
        branch_real,
        branch_imaginary,
        probability_numerator,
        probability_denominator,
        magnitude_lower_bound,
        magnitude_upper_bound
    ) in branch_cases:
        evaluated_real:int = half_scale + multiply_and_divide_with_rounding(branch_real, quarter_scale, fixed_point_scale)
        evaluated_imaginary:int = multiply_and_divide_with_rounding(branch_imaginary, quarter_scale, fixed_point_scale)

        magnitude_squared:int = evaluated_real * evaluated_real + evaluated_imaginary * evaluated_imaginary
        if magnitude_lower_bound == magnitude_upper_bound:
            evaluated_magnitude:int = magnitude_lower_bound
        else:
            evaluated_magnitude = binary_search_rounded_square_root(
                magnitude_squared,
                magnitude_lower_bound,
                magnitude_upper_bound
            )

        transformed_real:int = divide_with_rounding(quarter_scale * evaluated_real * fixed_point_scale, magnitude_squared)
        transformed_imaginary:int = -divide_with_rounding(quarter_scale * evaluated_imaginary * fixed_point_scale, magnitude_squared)

        real_series_terms:list = [0] * (maximum_degree + 1)
        imaginary_series_terms:list = [0] * (maximum_degree + 1)
        power_real:int = fixed_point_scale
        power_imaginary:int = 0

        for degree_index in range(maximum_degree + 1):
            coefficient_value:int = taylor_coefficients[degree_index]
            real_series_terms[degree_index] = multiply_and_divide_with_rounding(power_real, coefficient_value, fixed_point_scale)
            imaginary_series_terms[degree_index] = multiply_and_divide_with_rounding(power_imaginary, coefficient_value, fixed_point_scale)
            power_real, power_imaginary = multiply_scaled_complex(
                power_real,
                power_imaginary,
                transformed_real,
                transformed_imaginary,
                fixed_point_scale
            )

        raw_series_sum:int = 0
        if transformed_imaginary == 0:
            for first_exponent, second_exponent, weighted_moment in nonzero_moment_items:
                raw_series_sum += (
                    real_series_terms[first_exponent]
                    * real_series_terms[second_exponent]
                    * weighted_moment
                )
        else:
            for first_exponent, second_exponent, weighted_moment in nonzero_moment_items:
                dot_product:int = (
                    real_series_terms[first_exponent] * real_series_terms[second_exponent]
                    + imaginary_series_terms[first_exponent] * imaginary_series_terms[second_exponent]
                )
                raw_series_sum += dot_product * weighted_moment

        series_sum:int = divide_with_rounding(raw_series_sum, fixed_point_scale_squared)
        weighted_branch_value:int = multiply_and_divide_with_rounding(evaluated_magnitude, series_sum, fixed_point_scale)
        accumulated_expectation += divide_with_rounding(weighted_branch_value * probability_numerator, probability_denominator)

    # 수학적으로 보장된 0.417829 < 지애 상수 < 0.471404 구간 내의 최종 기댓값 산출
    scaled_jiae_constant:int = divide_with_rounding(accumulated_expectation * 72, 85)

    shift_exponent:int = scale_exponent - output_digits
    truncation_divisor:int = 10 ** shift_exponent
    rounding_digit:int = (scaled_jiae_constant // (truncation_divisor // 10)) % 10
    rounded_integer_part:int = scaled_jiae_constant // truncation_divisor
    if rounding_digit >= 5:
        rounded_integer_part += 1

    return f"0.{rounded_integer_part:0{output_digits}d}"


maximum_degree:int = 870
output_digits:int = 222
scale_exponent:int = 240

total = 0.0
LIMIT = 10
for _ in range(LIMIT):
    start = time.time()
    final_output:str = compute_jiae_constant(maximum_degree, output_digits, scale_exponent)
    sys.stdout.write(final_output + "\n")
    # 타이머 종료 및 출력
    end = time.time()
    print(f"Elapsed time: {end - start:.3f} sec", file=sys.stderr)
    total += end - start

print(f"Average Elapsed time: {total / LIMIT:.3f} sec", file=sys.stderr)

# VS Code에서 직접 실행해본 결과 135초 -> 25초로 단축되었습니다.
# 추가적인 최적화 작업을 통해 25초 -> 15초로 단축되었습니다.
# 드디어 Python으로 22.222초 안에 통과됩니다!!!