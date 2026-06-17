import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

carriers = ["FedEx", "UPS", "DHL", "USPS", "Amazon Logistics"]
statuses = ["Delivered", "In Transit", "Out for Delivery", "Delayed", "Returned"]
origins = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ"]
destinations = ["Seattle, WA", "Miami, FL", "Boston, MA", "Denver, CO", "Atlanta, GA"]
categories = ["Electronics", "Clothing", "Furniture", "Food", "Books", "Sporting Goods"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 6, 17)

rows = []
for i in range(1, 201):
    ship_date = random_date(start_date, end_date)
    transit_days = random.randint(1, 14)
    delivery_date = ship_date + timedelta(days=transit_days)
    weight = round(random.uniform(0.1, 150.0), 2)
    cost = round(weight * random.uniform(0.5, 3.5) + random.uniform(5, 30), 2)
    rows.append({
        "Order ID": f"ORD-{10000 + i}",
        "Carrier": random.choice(carriers),
        "Status": random.choice(statuses),
        "Origin": random.choice(origins),
        "Destination": random.choice(destinations),
        "Category": random.choice(categories),
        "Ship Date": ship_date.strftime("%Y-%m-%d"),
        "Delivery Date": delivery_date.strftime("%Y-%m-%d"),
        "Transit Days": transit_days,
        "Weight (lbs)": weight,
        "Shipping Cost ($)": cost,
        "On Time": random.choice(["Yes", "Yes", "Yes", "No"]),
    })

df = pd.DataFrame(rows)
df.to_excel("shipping_data.xlsx", index=False)
print(f"Created shipping_data.xlsx with {len(df)} rows.")
