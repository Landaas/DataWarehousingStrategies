import datetime
import random
from ranges import ranges

old_date = datetime.date(2010, 1, 1)
arr = [[1, ranges[0]], [1, ranges[1]], [1, ranges[2]], [1, ranges[3]], [1, ranges[4]], [15, 600]]
entries = 100

def random_stuff(n):
    array = []

    for _ in range(n):
        delta = datetime.date.today() - old_date
        random_days = random.randint(0, delta.days)
        date =  old_date + datetime.timedelta(days=random_days)
        array.append([random.randint(num[0], num[1]) for num in arr] + [date])
    
    return array

with open("dataset.csv", "w") as f:
    f.writelines('\n'.join([str(','.join([str(i) for i in arr])) for arr in random_stuff(entries)]))