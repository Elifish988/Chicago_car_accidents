import csv

from flask import jsonify

from database.conect import accidents, injuries
from repository.parse_date_servis import parse_date


def read_csv(csv_path):
   with open(csv_path, 'r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           yield row


def init_accidents():
    accidents.drop()
    injuries.drop()


    try:
        for row in read_csv(r'C:\Users\Eli Fishman\Data\Python\Chicago_car_accidents\data\Traffic_Crashes_-_Crashes - 20k rows.csv'):
            injuries_total = int(row['INJURIES_TOTAL']) if row['INJURIES_TOTAL'].isdigit() else 0
            injuries_fatal = int(row['INJURIES_FATAL']) if row['INJURIES_FATAL'].isdigit() else 0
            injury = {
                'INJURIES_TOTAL': injuries_total,
                'INJURIES_FATAL': injuries_fatal,
                'INJURIES_NON_FATAL': injuries_total - injuries_fatal
            }

            injuries_id = injuries.insert_one(injury).inserted_id

            accident = {
                'CRASH_RECORD_ID': row['CRASH_RECORD_ID'],
                'PRIM_CONTRIBUTORY_CAUSE': row['PRIM_CONTRIBUTORY_CAUSE'],
                'BEAT_OF_OCCURRENCE': row['BEAT_OF_OCCURRENCE'],
                'CRASH_DATE':  parse_date(row['CRASH_DATE']),
                'injury': injuries_id

            }

            accidents.insert_one(accident)
    except Exception as e:
        return f"An error occurred: {e}"

    return "Processing completed successfully"
