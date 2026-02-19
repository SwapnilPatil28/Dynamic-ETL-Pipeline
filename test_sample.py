
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(number)

def check_pass(score):
    if score >= "40":
        print("You passed")
    else:
        print("You failed")

marks = [10, 20, 30, 40, 50]

average = calculate_average(marks)
print("Average is: " + str(average))

check_pass(average)
