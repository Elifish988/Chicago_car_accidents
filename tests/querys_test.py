import pytest
from pymongo import MongoClient
from repository.querys_repository import count_accidents_by_region, count_accidents_by_region_and_period, \
    count_accidents_by_cause_and_region, get_accident_statistics

@pytest.fixture(scope="function")
def create_database():

    client = MongoClient('mongodb://localhost:27017/')
    db = client['chicago_car_accidents']


    injuries = db['injuries']
    accidents = db['accidents']

    injuries.drop()
    accidents.drop()


    injury_data = [
        {'INJURIES_TOTAL': 3, 'INJURIES_FATAL': 1, 'INJURIES_NON_FATAL': 2},
        {'INJURIES_TOTAL': 5, 'INJURIES_FATAL': 0, 'INJURIES_NON_FATAL': 5},
        {'INJURIES_TOTAL': 2, 'INJURIES_FATAL': 1, 'INJURIES_NON_FATAL': 1}
    ]


    injury_ids = [injuries.insert_one(injury).inserted_id for injury in injury_data]


    accident_data = [
        {'CRASH_RECORD_ID': '1', 'PRIM_CONTRIBUTORY_CAUSE': 'Speeding', 'BEAT_OF_OCCURRENCE': '225',
         'CRASH_DATE': '2024-01-01', 'injury': injury_ids[0]},
        {'CRASH_RECORD_ID': '2', 'PRIM_CONTRIBUTORY_CAUSE': 'Under the influence of alcohol',
         'BEAT_OF_OCCURRENCE': '225', 'CRASH_DATE': '2024-01-02', 'injury': injury_ids[1]},
        {'CRASH_RECORD_ID': '3', 'PRIM_CONTRIBUTORY_CAUSE': 'Failure to reduce speed', 'BEAT_OF_OCCURRENCE': '226',
         'CRASH_DATE': '2024-01-03', 'injury': injury_ids[2]}
    ]


    accidents.insert_many(accident_data)
    return accidents, injuries


@pytest.fixture(scope="function")
def init_test_data(create_database):
    return create_database




def test_count_accidents_by_region(init_test_data):
    accidents, injuries = init_test_data
    count = count_accidents_by_region(accidents,'225')
    assert count == 2

def test_count_accidents_by_region_and_period(init_test_data):
    accidents, injuries = init_test_data
    count = count_accidents_by_region_and_period( accidents,'225', 'day', '01/01/2024')
    assert count == 1

def test_count_accidents_by_cause_and_region(init_test_data):
    accidents, injuries = init_test_data
    cause_count = count_accidents_by_cause_and_region(accidents,'225')
    assert cause_count['Speeding'] == 1
    assert cause_count['Under the influence of alcohol'] == 1

def test_get_accident_statistics(init_test_data):
    accidents, injuries = init_test_data
    stats = get_accident_statistics(accidents, injuries,'225')
    assert stats['total_injuries'] == 8  # 3 + 5
    assert stats['total_fatal_injuries'] == 1  # Only one fatal injury
    assert stats['total_non_fatal_injuries'] == 7  # 2 + 5
