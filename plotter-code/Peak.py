def gregorian_to_jalali(g_date):
    j_date = JalaliDate(g_date.year, g_date.month, g_date.day)
    return f"{j_date.year}-{j_date.month}-{j_date.day}"


def find_peak_date(data, start_date, end_date):

    data['created_at'] = pd.to_datetime(data['created_at'], format='%Y-%m-%d')

    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    mask = (data['created_at'] >= start_date) & (data['created_at'] <= end_date)
    filtered_df = data.loc[mask]

    date_counts = filtered_df['created_at'].value_counts().sort_index()

    peak_date = date_counts.idxmax()

    peak_jalali_date = gregorian_to_jalali(peak_date)

    return peak_jalali_date


peak_date = find_peak_date(df, start_date, end_date)

print("The exact date of the biggest peak:", peak_date)
