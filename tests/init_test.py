import pytest


@pytest.fixture(scope="function")
def accidents_collection(init_test_data):
   return init_test_data['cars']


def test_init(accidents_collection):
    assert accidents_collection.find() != 0



