# py3-URL-shortener

## create db

`python3 script/create_db.py`

## api list

```
1. check server work
[GET] /

Response:
    200:
        { "code": 200, "message": "ok." }

2. create short url
[POST] /

Body:
    {
        "origin": "https://www.google.com.tw?region=zh_tw#/firstpage",   # redirect url
	    "alias": "dcRi4m"                                                # (option)
    }

Response:
    200:
        { "code": 200, "message": "ok." }
    400:
        # origin is None
        { "code": 400, "message": "Validation Failed" }
    410:
        # alias repeat
        { "code": 410, "message": "Alias repeat" }

3. search date
[GET] /search

Query:
    {}

Response:
    # The top 3 visted 
    [
        {
            "alias" : "dcRi4m", 
            "origin": "https://www.google.com.tw?region=zh_tw#/firstpage", 
            "counts": 3
        }, {
            "alias" : "doii4p", 
            "origin": "https://www.google.com.tw?region=zh_tw#/firstpage", 
            "counts": 2
        }, {
            "alias" : "dc270a", 
            "origin": "https://www.google.com.tw?region=zh_tw#/firstpage", 
            "counts": 1
        }
    ]

Query:
    { "start": 20200418, "end": 20200505 }

Response:
    [
        {
            "Date": "2020-04-18",
            "Values": [
            {
                "alias": "dc270a",
                "origin": "https://www.google.com.tw?region=zh_tw#/firstpage",
                "counts": 1
            }
            ]
        },
        {
            "Date": "2020-05-05",
            "Values": [
            {
                "alias": "dcRi4m",
                "origin": "https://www.google.com.tw?region=zh_tw#/firstpage",
                "counts": 3
            }
            ]
        }
    ]
```