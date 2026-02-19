#import requests

#base_url = "https://ru.yougile.com/api-v2"
#body = {"title": "Создание проекта 33"}
#my_headers = {"Authorization": "Bearer A25-EVvVVQgDlv2GvtJYoh21zCAAcJealS-vJEurG4JR4aXbp5S4Mwfc4xtpxk6U", 
           "Content-Type": "application/json"}

#def test_create_pozitiv():
    resp = requests.post(f'{base_url}/projects', json=body, headers=my_headers)
    assert resp.status_code ==201
    print(resp)
    x = resp.json()
    print(x)