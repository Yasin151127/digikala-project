from matplotlib import pyplot as plt
import pandas as pd
from jdatetime import datetime as jd_datetime

data = pd.read_csv('D:\\University\\10\\RA\\Project-2\\digikala-comments.csv', low_memory=False)
df = pd.DataFrame(data)


persian_to_number = {
    'فروردین': '01',
    'اردیبهشت': '02',
    'خرداد': '03',
    'تیر': '04',
    'مرداد': '05',
    'شهریور': '06',
    'مهر': '07',
    'آبان': '08',
    'آذر': '09',
    'دی': '10',
    'بهمن': '11',
    'اسفند': '12'
}
# changing month str to int (cleaning)
for persian_month, number_month in persian_to_number.items():
    df['created_at'] = df['created_at'].str.replace(persian_month, number_month)



df['created_at'] = df['created_at'].str.replace(' ', '-')


def format_date(date_str):
    day, month, year = date_str.split('-')  # Split date string into day, month, and year
    # Ensure day and month have two digits
    day = day.zfill(2)
    month = month.zfill(2)
    # Join components back together with dashes
    return f"{day}-{month}-{year}"


df['created_at'] = df['created_at'].apply(format_date)


def jalali_to_gregorian(date_str):
    jalali_date = jd_datetime.strptime(date_str, '%d-%m-%Y')
    gregorian_date = jalali_date.togregorian()
    return gregorian_date.strftime('%d-%m-%Y')


df['created_at'] = df['created_at'].apply(jalali_to_gregorian)

df['created_at'] = pd.to_datetime(df['created_at'], format='%d-%m-%Y')

start_date = '20-03-2022'
end_date = '20-03-2023'

mask = (df['created_at'] >= start_date) & (df['created_at'] <= end_date)
filtered_df = df.loc[mask]

date_counts = filtered_df['created_at'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(date_counts.index, date_counts.values)
plt.title('Number of Occurrences Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Occurrences')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


