import json
from src.contacts.app import lambda_handler

test_token = "IQoJb3JpZ2luX2VjEKL//////////wEaCWV1LXdlc3QtMSJIMEYCIQCWAdQVbk2Xe9XlzJV+wQrJ9EXRmT0b2UUXbpDa8RrNxwIhAOgQQ3fWy8z+n7r7oWtUedoFYpyEE0DYEqDHpyemsDF6KpgDCLv//////////wEQABoMMjExMTI1NTYxMDA1IgxYD+kJSr87SmNTMbEq7AK+DWhh0StDEvBOGkWog0NF1subOu08iv6t2igrhci3iE400CecIbmGESCQw7xGJvms2xL3bDXhIT4Hb6zeo/MYI4/YY4PJVbILjmLdXcizuGyovZroSRrMgqrLVvvio3dA5D6D5tTskmGToZZHziHyRS2mv6vlCKW4Gd5Lk4fIkN1LgZ4dx+OJdZMQ4/LeJns4zuOKCcH6TUciiKpih6NXBeaDLqHUqWn8G6/4tvKyGx10KaIo0eTvW34MdgkVgqYysfYkNdKvCkN+rISBH3bSjJgugaDOLgs+57Oyh+U2dvZbbGfGzArR3WmtptqZyWK4jNhaWBN1yYTNMJMMfDTxA6UAL72xrjW8j9+patZwftOEGiM44UVFQNpbX/jipha+OWuCAs9b4jzoJAZpuqFXS8DAb/o3MPV9A3uI6xBnm+IeilczMY8ReK1BiJBm0uOZTleKH5Vh5zotUI8k1WQ8o0/lr7+tcNBfh/TvMPi627YGOqUBxcdwX4nau7V7qgYCkpvYZxgy5L1368tXaJEF3VHVhiN09PEt4J98D6zh0rTS+hRtwyr4txLOtZnKFWQHHTbUgfVhQiJ6jrxk+iSvpX4RM1FeLcS92snEdlJiPheUYE+2y+q263plvrqNW3prkNoNc8FVuaXmUjLZVjrZGc3eMxhjh6je2Ut0/DI/E+1J/k/AUyH1N9LukRGCbL5Xk5c6q+5njc/q"

event = {
    "routeKey": "POST /contacts/lead/create",
    "headers": {
        "Authorization": f"Bearer {test_token}"
    }, 
    "body": json.dumps({
        "firstName": "Don",
        "lastName": "Lucho",
        "phone": "1234567890",
        "nif": "AB123456C",
        "email": "Don.Lucho@Test.com",
    })
}
response = lambda_handler(event, None)
print(response)
