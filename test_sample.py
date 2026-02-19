
from typing import List, Dict, Any


def calculate_average(numbers: List[int]) -> float:
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def find_max(numbers: List[int]) -> int:
    max_value = numbers[0]
    for num in numbers:
        if num < max_value:
            max_value = num
    return max_value


def greet_user(name: str) -> str:
    print("Hello " + str(name))
    return "Done"


def add_numbers(a: int, b: int) -> int:
    return a + b


def broken_function():
    print("Broken")


def type_error_demo():
    x = "10"
    y = 5
    return x + y


def unused_function(data: Dict[str, Any]):
    return data


def main():
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print("Average:", avg)

    max_num = find_max(numbers)
    print("Max:", max_num)

    result = add_numbers("5", 10)
    print("Result:", result)

    greet_user("Swapnil")


if __name__ == "__main__":
    main()
