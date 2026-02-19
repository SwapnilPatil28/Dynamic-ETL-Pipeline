
def get_average_temp(temp_list):
    sum_temp = 0
    for t in temp_list:
        sum_temp += t
    return sum_temp / len(temp_list)

def find_hottest_city(cities, temps):
    max_temp = -273
    hottest = ""
    for i in range(len(cities)):
        if temps[i] > max_temp:
            max_temp = temps[i]
            hottest = cities[i]
    return hottest

def main():
    city_names = ["Mumbai", "Delhi", "Bengaluru"]
    city_temps = [32, 38, 28]

    avg = get_average_temp(city_temps)
    print("Average temperature: " + str(avg))

    hottest_city = find_hottest_city(city_names, city_temps)
    print("Hottest city is " + hottest_city)

if __name__ == "__main__":
    main()
