data = []
times = []
with open('csvs/r_asrc_20_fake_whole_cell.csv', 'r') as csv_file:
    for line in csv_file:
        (time, result) = line.split(',')
        data.append(result.strip())
        times.append(time)

interesting_data = data[:31]
boring_data = data[0]

data1 = list(interesting_data)
data1.extend([boring_data]*(100-len(interesting_data)))

data2 = [boring_data]*10
data2.extend(list(interesting_data))
data2.extend([boring_data]*(90-len(interesting_data)))

data3 = [boring_data]*20
data3.extend(list(interesting_data))
data3.extend([boring_data]*(70-len(interesting_data)))

new_data = zip(times, data1, data2, data3)
with open('csvs/r_asrc_20_fake_whole_cell.csv', 'w') as csv_file:
    for row in new_data:
        csv_file.write(','.join(row) + '\n')
