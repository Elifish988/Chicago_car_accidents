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


