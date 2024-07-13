import pandas as pd
import jdatetime

persian_months = {
    'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4,
    'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8,
    'آذر': 9, 'دی': 10, 'بهمن': 11, 'اسفند': 12
}

def persian_to_gregorian(date_str):
    day, month_name, year = date_str.split()
    day = int(day)
    month = persian_months[month_name]
    year = int(year)
    jdate = jdatetime.date(year, month, day)
    gdate = jdate.togregorian()
    return pd.Timestamp(gdate)

df = pd.read_csv('digikala-comments.csv')
df['created_at'] = df['created_at'].apply(persian_to_gregorian)
df.to_csv('digikala_comments_converted.csv', index=False)

comments_df = pd.read_csv('digikala_comments_converted.csv', parse_dates=['created_at'])
comments_df['product_id'] = comments_df['product_id'].astype(str)
products_df = pd.read_csv('digikala-products.csv', dtype={'id': str, 'sub_category': str, 'Category1': str})
merged_df = pd.merge(comments_df, products_df[['id', 'sub_category', 'Category1']], left_on='product_id', right_on='id', how='left')
if 'id' in merged_df.columns:
    merged_df.drop(columns=['id'], inplace=True)
merged_df.to_csv('digikala_comments_with_categories.csv', index=False)
