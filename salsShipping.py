import bs4 as bs
import requests
import pandas as pd
import json

# Fetch Sal's shipping rates
url = "https://www.codecademy.com/projects/practice/python-sals-shipping"
response = requests.get(url)
soup = bs.BeautifulSoup(response.content, "html.parser")

# Step 2: Find the <script> tag containing JSON data
script_tag = soup.find("script", {"id": "__NEXT_DATA__"})


# Step 3: Extract JSON data from the <script> tag
json_data = json.loads(script_tag.string)

# Navigate to the dictionary where pricing information is stored
project_info = json_data["props"]["pageProps"]["reduxData"]["entities"]["contentItems"][
    "byId"
]

# Extract the project ID dynamically (as it changes)
project_id = list(project_info.keys())[0]  # First key should be the project ID

# Step 4: Locate the shipping pricing table
pricing_info = project_info[project_id]["projectInformation"]["objective"]


# Step 5: Extract pricing information
lines = pricing_info.split("\n")
shipping_data = []
method = None

for line in lines:
    line = line.strip()
    if "**Ground Shipping**" in line:
        method = "Ground Shipping"
    elif "**Ground Shipping Premium**" in line:
        method = "Ground Shipping Premium"
        shipping_data.append([method, "Flat charge", 125.00])
    elif "**Drone Shipping**" in line:
        method = "Drone Shipping"
    elif line.startswith("|") and method:  # Table row
        columns = [
            col.strip() for col in line.split("|")[1:-1]
        ]  # Clean and split table row
        if len(columns) == 3:
            weight, price, flat_charge = columns
            price = float(price.replace("$", "")) if "$" in price else price
            flat_charge = (
                float(flat_charge.replace("$", ""))
                if "$" in flat_charge
                else flat_charge
            )
            shipping_data.append([method, weight, price, flat_charge])

# Step 6: Create a Pandas DataFrame
df = pd.DataFrame(
    shipping_data,
    columns=["Shipping Method", "Weight", "Price per Pound", "Flat Charge"],
)

# Display the table
print(df)

# Write a shipping.py Python program that asks the user for the weight of their package and then tells them which method of shipping is cheapest and how much it will cost to ship their package using Sal’s Shippers.
