import requests
# Post
url = "http://127.0.0.1:8000/drf_app/book/117"
new_data = {
    "name": "New book10",
    "price": 10000,
    "publisher": {"id": 3, "name": "Publisher3"},
    "authors": [{"id": 1, "first_name": "Author_3_name","last_name": "Author_3_surname", "email": " author.3@gmail.com"}, {"id": 2, "first_name": "Author_4_name","last_name": "Author_4_surname", "email": " author.4@gmail.com"}]
}
resp = requests.post(url=url, json=new_data)
print(resp.content)
#Get
# url = "http://127.0.0.1:8000/drf_app/book/117"
# resp = requests.get(url=url)
# print(resp.content)
