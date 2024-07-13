
merged_df = pd.merge(comments_df, products_df[['id', 'sub_category']], left_on='product_id', right_on='id',
                     how='left')

merged_df.drop('id', axis=1, inplace=True)

# Define start_date and end_date
start_date = '2023-03-20'
end_date = '2024-03-20'
specific_category = 'travel'  # Specify the category you want to plot


filtered_df = merged_df[(merged_df['sub_category'] == specific_category) &
                        (pd.to_datetime(merged_df['created_at'], errors='coerce') >= pd.to_datetime(start_date)) &
                        (pd.to_datetime(merged_df['created_at'], errors='coerce') <= pd.to_datetime(end_date))]


filtered_df.loc[:, 'created_at'] = pd.to_datetime(filtered_df['created_at'], errors='coerce')

filtered_df.set_index('created_at', inplace=True)

filtered_df = filtered_df.infer_objects()

category_counts = filtered_df.resample('D').size()

plt.figure(figsize=(10, 6))
category_counts.plot()
plt.title(f'Time Series of {specific_category} Counts')
plt.xlabel('Date')
plt.ylabel('Number of Occurrences')
plt.grid(True)
plt.show()