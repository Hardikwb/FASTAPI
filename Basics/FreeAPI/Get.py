import requests
'''
# url="https://api.freeapi.app/api/v1/public/randomusers/1"
# or
url="https://api.freeapi.app/api/v1/public/randomusers"
querystring={"page":"1","limit":"2"}
#  page 1 get get 2 username
headers = {"accept": "application/json"}
# get in json format

# response=requests.get(url,params=querystring)
response=requests.get(url,headers=headers,params=querystring)
# https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=1
print(response.json())
'''

'''
url='https://api.freeapi.app/api/v1/public/randomproducts?page=1&limit=2&inc=category%252Cprice%252Cthumbnail%252Cimages%252Ctitle%252Cid&query=mens-watches'
url_modified='https://api.freeapi.app/api/v1/public/randomproducts'

# Best practice to write params
result=requests.get(url_modified,headers={"accept":"application/json"},
                    params={"page":"1",
                            "limit":"2",
                            "inc":"category,price,thumnail,images,title,id",
                            "query":"mens-watches"})
print(result.json)
'''

'''
,	Normal comma
%2C	Encoded comma
%252C	Encoded %2C (double encoding)
'''


'''
url_get_quotes = "https://api.freeapi.app/api/v1/public/quotes"
url_get_quotes_by_id = "https://api.freeapi.app/api/v1/public/quotes/12"
url_get_quotes_by_id_random = "https://api.freeapi.app/api/v1/public/quotes/random"
querystring = {"page":"1","limit":"10","query":"human"}
headers = {"accept": "application/json"}
response = requests.get(url_get_quotes, headers=headers, params=querystring)
print(response.json())
'''


url = "https://api.freeapi.app/api/v1/public/quotes"
querystring = {"page":"1","limit":"10","query":"human"}
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers, params=querystring)
print(response.json())