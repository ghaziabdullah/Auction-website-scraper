import requests
import pandas as pd

def get_data(page):
    url = "https://www.vakantieveilingen.be/gateway/v3/categories"
    querystring = {"page": page, "pageSize": 100, "sort": "popularity"}
    response = requests.get(url, params=querystring)
    print(f"Page No {page} status code : {response.status_code}")
    return response.json()

def parse_product_data(data):
    title = data['product']['title']
    category = data['categoryTree']['childCategories'][0]['tagName']
    bid_count = data['bidCount']
    highest_bid_amount = data['highestBidAmount']
    description = data['product']['abstract']
    rel_url = data['url']
    abs_url = f"https://www.vakantieveilingen.be{rel_url}"
    return {
        "Title": title,
        "Category": category,
        "Bid Count": bid_count,
        "Highest Bid Amount(€)": highest_bid_amount,
        "Description": description,
        "URL": abs_url
    }

def fetch_all_products():
    all_products = []

    for page in range(1, 9):
        response_data = get_data(page)
        products = response_data['data']['blocks']['lots']
        for product in products:
            product_data = parse_product_data(product)
            all_products.append(product_data)
    
    return all_products

def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    products = fetch_all_products()
    save_to_csv(products, "all_auction_products.csv")
    print(f"Saved {len(products)} items")


# import requests

# url = "https://www.vakantieveilingen.be/gateway/v3/categories"

# querystring = {"page":"1","pageSize":"1","sort" : "popularity"}

# response = requests.request("GET", url, params=querystring)

# resp = response.json()
# data = resp['data']['blocks']['lots'][0]

# title = print(data['product']['title'])
# category = print(data['categoryTree']['childCategories'][0]['tagName'])
# bid_count = print(data['bidCount'])
# highestBidAmount = print(data['highestBidAmount'])
# description = print(data['product']['abstract'])
# rel_url = data['url']
# abs_url = f"https://www.vakantieveilingen.be{rel_url}"
# print(abs_url)
