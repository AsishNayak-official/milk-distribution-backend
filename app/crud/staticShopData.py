from datetime import datetime, timedelta
from .. import schemas

# Get the current date
now = datetime.now()

# Get the first day of the current month
first_day_of_month = now.replace(day=1)

# Get the last day of the current month
# We can add one month, then subtract one day from the first day of the next month
last_day_of_month = (first_day_of_month.replace(month=now.month % 12 + 1, day=1) - timedelta(days=1))

# Convert to string format (ISO format) or any format required
start_bill_date = first_day_of_month.strftime('%Y-%m-%d')
end_bill_date = last_day_of_month.strftime('%Y-%m-%d')

# Static shop data with dynamic start and end date for current month
static_shop_data = schemas.shop.ShopCreate(
    society_name="OMM SAI WMPCS",
    society_code="MA346",
    unit="MAHANGA",
    month=now.strftime('%B'),  # Current month name (e.g., 'January')
    start_bill_date=start_bill_date,
    end_bill_date=end_bill_date
)
