import json
from src.contacts.app import lambda_handler

test_token = "IQoJb3JpZ2luX2VjEKv//////////wEaCWV1LXdlc3QtMSJHMEUCIQDj436y45RQJXbIuGDZjIv9tPEWopmVY7eYPxnWg7YTVAIgUeEuf4ddunEX2O3WEkEl46gF2kEh3MsnQD7Ug9SRqLQqmAMIxP//////////ARAAGgwyMTExMjU1NjEwMDUiDJby9co7/OJ5YuCjYSrsAjMq36fO640eAZzyYebyXUfFAvlvhfXwJAN1OuaYQlYMVWXzgYEZjcy1qNnecxhiSzcaRdHbNpliF9LaR2NaFYGgGwy4zovsdeQr0VS1grW6kQgU3jcapCMRW2Z1lTT8FgGUrENHRtHCqe5w81mOJHNX2tk9bCkswQvmvUTbweUiGiNMr2+5POybkTCIn8bb49lRCo18ABzWoQBd7/O8WDVm/sQM+VQXNZn0gb6qprI5qa6NmrkfD8EM39R/mBS9Y1IOPio+jKb04JTqjSvKL44Z+mBu6heVmCav7+RAxNi7QBalJ42k1a+2zyOS3LkgnVv4SU8JI4XMpL7xC6S8Zn4KWu9n69kUzddkbNXaI09fLv3ROxyExuWqey5zeFxNb8peSVmJwRrY0liiP8XhTDBLAQ3piauyYQPg0x7GrdPYEIknwZr+5VS3rjAV7s1aiUq71HCRYUsfQxC1FpdMfgMrLloCH4XaLFII0+4wxqrdtgY6pgHmUYGZvnDxppvtRk2zk6f/64wlcxXFUqZzqppA297RU6qAQyt8Ys/H3ejf30MK5DFszuLAUu2evNjVL/xm8WeVKX7AdioiER3hoccOHR4CDsHUX8u8hF2caHnoVFx4aAOp9nJVKHGpbaQxwwrRAIjE+BTFJJxNmUzGG6XTaI2arzqwIaVDjcyiuP8yFV7GV0GpA8wqtPKErLL+VmF20lH+VX6WoWIV"

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
