from collections import defaultdict
from datetime import timedelta, datetime

from flask import jsonify

from database.conect import accidents, injuries


def count_accidents_by_region(region):
    total_accidents = accidents.count_documents({'BEAT_OF_OCCURRENCE': region})
    return total_accidents


def count_accidents_by_region_and_period(region, period, start_date):
    start_date = datetime.strptime(start_date, '%d/%m/%Y')

    if period == 'day':
        end_date = start_date + timedelta(days=1)
    elif period == 'week':
        end_date = start_date + timedelta(weeks=1)
    elif period == 'month':
        end_date = start_date + timedelta(days=30)
    else:
        return {"error": "Invalid period. Must be 'day', 'week', or 'month'."}

    total_accidents = accidents.count_documents({
        'BEAT_OF_OCCURRENCE': region,
        'CRASH_DATE': {'$gte': start_date, '$lt': end_date}
    })

    return total_accidents


def count_accidents_by_cause_and_region(region):
#יצירת דיקשנרי מיוחד שמייצר ערכים דיפולטיבים
    cause_count = defaultdict(int)
#מחפש תאונות על פי האיזור
    accidents_data = accidents.find({'BEAT_OF_OCCURRENCE': region})

    for accident in accidents_data:
        cause = accident.get('PRIM_CONTRIBUTORY_CAUSE')
        cause_count[cause] += 1

    return dict(cause_count)


def get_accident_statistics(region):
    total_injuries = 0
    total_fatal_injuries = 0
    total_non_fatal_injuries = 0
    fatal_events = []
    non_fatal_events = []

    accident_records = accidents.find({'BEAT_OF_OCCURRENCE': region})

    for record in accident_records:
        injury_id = record['injury']
        injury = injuries.find_one({'_id': injury_id})

        if injury:
            total_injuries += injury['INJURIES_TOTAL']
            total_fatal_injuries += injury['INJURIES_FATAL']
            total_non_fatal_injuries += injury['INJURIES_NON_FATAL']

            # המרת ObjectId למחרוזת תוספת בעקבות באג
            record['_id'] = str(record['_id'])
            record['injury'] = str(injury_id)

            # הוספת האירוע לרשימות
            if injury['INJURIES_FATAL'] > 0:
                fatal_events.append(record)
            else:
                non_fatal_events.append(record)

    return {
        'total_injuries': total_injuries,
        'total_fatal_injuries': total_fatal_injuries,
        'total_non_fatal_injuries': total_non_fatal_injuries,
        'fatal_events': fatal_events,
        'non_fatal_events': non_fatal_events
    }


