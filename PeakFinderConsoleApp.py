import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import jdatetime
import argparse

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

def gregorian_to_persian(date):
    jdate = jdatetime.date.fromgregorian(date=date)
    day = jdate.day
    month_name = [k for k, v in persian_months.items() if v == jdate.month][0]
    year = jdate.year
    return f"{day} {month_name} {year}"

def find_peaks_by_category(df, start_date, end_date, category_column=None, category_value=None, threshold_type='percentage', threshold_value=0.20, plot=True):
    start_date_gregorian = persian_to_gregorian(start_date)
    end_date_gregorian = persian_to_gregorian(end_date)
    
    mask = (df['created_at'] >= start_date_gregorian) & (df['created_at'] <= end_date_gregorian)
    filtered_df = df[mask]
    
    if category_column and category_value:
        filtered_df = filtered_df[filtered_df[category_column] == category_value]

    daily_counts = filtered_df['created_at'].value_counts().sort_index().reset_index()
    daily_counts.columns = ['created_at', 'count']

    x = np.arange(len(daily_counts))
    y = daily_counts['count'].values
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    regression_line = slope * x + intercept

    if threshold_type == 'percentage':
        deviations = np.abs(y - regression_line) / regression_line
        peaks = deviations > threshold_value
    elif threshold_type == 'std_dev':
        deviations = np.abs(y - regression_line)
        mean_deviation = np.mean(deviations)
        peaks = deviations > (mean_deviation + threshold_value * np.std(deviations))
    else:
        raise ValueError("Invalid threshold_type. Choose 'percentage' or 'std_dev'.")

    peak_dates = daily_counts['created_at'][peaks]

    peak_dates_persian = peak_dates.apply(gregorian_to_persian)

    print("Peak dates with significant deviations:", peak_dates_persian.tolist())

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(daily_counts['created_at'], y, label='Actual Counts')
        plt.plot(daily_counts['created_at'], regression_line, label='Regression Line', linestyle='--')
        plt.scatter(peak_dates, y[peaks], color='red', label='Peaks')
        plt.xlabel('Date')
        plt.ylabel('Comment Count')
        plt.title(f'Comment Peaks' + (f' for {category_column}: {category_value}' if category_column and category_value else ''))
        plt.legend()
        plt.show()

    return peak_dates_persian

def find_common_peaks(df, start_year1, start_year2, category_column=None, category_value=None, threshold_type='percentage', threshold_value=0.20):
    start_date1 = f'1 فروردین {start_year1}'
    end_date1 = f'29 اسفند {start_year1}'
    start_date2 = f'1 فروردین {start_year2}'
    end_date2 = f'29 اسفند {start_year2}'

    peaks1 = find_peaks_by_category(df, start_date1, end_date1, category_column, category_value, threshold_type, threshold_value, False)

    peaks2 = find_peaks_by_category(df, start_date2, end_date2, category_column, category_value, threshold_type, threshold_value, False)

    peak_days1 = {(date.split()[0], date.split()[1]) for date in peaks1}
    peak_days2 = {(date.split()[0], date.split()[1]) for date in peaks2}

    common_peak_days = peak_days1.intersection(peak_days2)

    print("Common peak days in both years:", common_peak_days)

    return common_peak_days

def find_common_peak_days(df, category_column=None, category_value=None, threshold_type='percentage', threshold_value=0.20):
    common_peak_days = {} 
    
    unique_years = range(1399, 1403)
    for year in unique_years:
        start_date = f'1 فروردین {year}'
        end_date = f'29 اسفند {year}'

        peaks = find_peaks_by_category(df, start_date, end_date, category_column, category_value, threshold_type, threshold_value, False)

        for peak_date in peaks:
            day_month = ' '.join(peak_date.split(' ')[0:2])  
            if day_month in common_peak_days:
                common_peak_days[day_month] += 1
            else:
                common_peak_days[day_month] = 1

    common_peak_days = {date: count for date, count in common_peak_days.items() if count > 1}

    common_peak_days_list = list(common_peak_days.items())

    print("Common peak days occurring in more than one year:")
    for date, count in common_peak_days_list:
        print(f"{date}: {count} occurrences")

    return common_peak_days_list

def main():
    parser = argparse.ArgumentParser(description='Peak Finder for Digikala Comments')

    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing comments data')
    parser.add_argument('command', choices=['find_peaks', 'find_common_peaks', 'find_common_peak_days'], help='Command to execute')
    parser.add_argument('--start_date', type=str, help='Start date in Persian (e.g., "1 فروردین 1402")')
    parser.add_argument('--end_date', type=str, help='End date in Persian (e.g., "29 اسفند 1402")')
    parser.add_argument('--start_year1', type=int, help='Start year 1 for finding common peaks')
    parser.add_argument('--start_year2', type=int, help='Start year 2 for finding common peaks')
    parser.add_argument('--category_column', type=str, help='Category column for filtering')
    parser.add_argument('--category_value', type=str, help='Category value for filtering')
    parser.add_argument('--threshold_type', choices=['percentage', 'std_dev'], default='percentage', help='Threshold type for peak detection')
    parser.add_argument('--threshold_value', type=float, default=0.20, help='Threshold value for peak detection')
    parser.add_argument('--plot', action='store_true', help='Whether to plot the results')

    args = parser.parse_args()

    comments_df = pd.read_csv(args.csv_file, parse_dates=['created_at'])

    if args.command == 'find_peaks':
        if not args.start_date or not args.end_date:
            print("Error: --start_date and --end_date are required for find_peaks")
            return
        find_peaks_by_category(comments_df, args.start_date, args.end_date, args.category_column, args.category_value, args.threshold_type, args.threshold_value, args.plot)
    
    elif args.command == 'find_common_peaks':
        if args.start_year1 is None or args.start_year2 is None:
            print("Error: --start_year1 and --start_year2 are required for find_common_peaks")
            return
        find_common_peaks(comments_df, args.start_year1, args.start_year2, args.category_column, args.category_value, args.threshold_type, args.threshold_value)
    
    elif args.command == 'find_common_peak_days':
        find_common_peak_days(comments_df, args.category_column, args.category_value, args.threshold_type, args.threshold_value)

if __name__ == "__main__":
    main()
