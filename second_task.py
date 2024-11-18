from statistics import mean

def read_file(filepath):
    with open(filepath) as file:
        lines = file.read().split('\n')       
        digits_map = []

        for line in lines:
            digits_map.append(list(map(int, line.split(' '))))

        return digits_map

def get_result():
    digits_map = read_file('second_task.txt')
    sums = []
    
    for line in digits_map:
        sum = 0
        for digit in line:        
            if (digit*digit < 100000):
                sum += abs(digit)
        sums.append(sum)

    arithmetic_mean = mean(sums)

    with open('second_task_result.txt', 'w+') as file:
        for i in sums:
            file.write(str(i) + '\n')
        file.write('------\n')
        file.write(str(arithmetic_mean))

get_result()