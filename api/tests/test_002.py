import requests
from mock import patch
from api.Gold.GoldClass import  Gold
import pytest


@pytest.mark.mock_test
class TestGold:
    def test_gold(self):
        import pdb
        #pdb.set_trace()
        fake_json=[{'key':'value'}]
        with patch('api.Gold.GoldClass.requests.exceptions') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = fake_json

            obj = Gold()
            response = obj.get()

        assert response.status_code == 200
        assert response.json() == fake_json



