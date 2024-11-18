from statistics import mean

def read_file(filepath):
    with open(filepath) as file:
        lines = file.read().split('\n')
        digits_map = []

        for line in lines:
            digits_map.append(line.split(' ')) 
    
        return digits_map

def filter_data(): 
    digits_map = read_file('third_task.txt')
    filtered_lines = []

    for i in range(len(digits_map)):
        filtered_line = []      
        for j in range(len(digits_map[i])):
            if (digits_map[i][j] == 'N/A'):
                digits_map[i][j] = (int(digits_map[i][j-1]) + int(digits_map[i][j+1]))/2                          
            else:
                digits_map[i][j] = int(digits_map[i][j])                
            if (digits_map[i][j] < 0 and digits_map[i][j]%2 == 1):
                filtered_line.append(digits_map[i][j])
        filtered_lines.append(filtered_line) 
      
    return filtered_lines

def get_averages():
    filtered_data = filter_data()
    arithmetic_means = []
    
    for digits in filtered_data:
        arithmetic_means.append(mean(digits))

    with open('third_task_result.txt', 'w+') as file:
        for num in arithmetic_means:
            file.write(str(num) + '\n')
        
get_averages()