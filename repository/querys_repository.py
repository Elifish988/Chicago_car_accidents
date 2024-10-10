from collections import defaultdict
from datetime import timedelta, datetime

from database.conect import accidents


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


