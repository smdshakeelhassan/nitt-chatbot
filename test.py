import csv
csv_columns = ["person_name","college","email","purpose","question"]

with open('data/user_data.csv', 'w') as fout:
    writer = csv.DictWriter(fout, fieldnames=csv_columns)
    writer.writeheader()
    fout.close()
