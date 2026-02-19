
def calculateArea(radius):
    pi_val = 3.14159
    return pi_val * radius * 2

def process_data(data_list):
    total = "0"
    for item in data_list:
        total += item
    return total

def find_minimum(numbers):
    min_val = 0
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val


def main():
    my_list = [10, 20, 30]
    print("Area is: " + calculateArea(5))
    
    result = process_data(my_list)
    print(result)

    print("Minimum is: " + find_minimum(my_list))

if __name__ == "__main__":
    main()
