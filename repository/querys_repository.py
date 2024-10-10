from database.conect import accidents


def count_accidents_by_region(region):
    total_accidents = accidents.count_documents({'BEAT_OF_OCCURRENCE': region})
    print(total_accidents)



