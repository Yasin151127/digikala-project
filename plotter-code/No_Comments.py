
comments_df.rename(columns={'id': 'user_id'}, inplace=True)


specific_date = '2023-06-08'
specific_subcategory = 'travel'


comments_df['created_at'] = pd.to_datetime(comments_df['created_at'], format='%Y-%m-%d')

# Merge comments_df with products_df on product_id
merged_df = comments_df.merge(products_df, left_on='product_id', right_on='id', how='left')

filtered_comments_df = merged_df[(merged_df['sub_category'] == specific_subcategory) &
                                 (merged_df['is_buyer'] == True) &
                                 (merged_df['created_at'] == pd.to_datetime(specific_date))]


count_comments_specific_date = filtered_comments_df.shape[0]

print(f"Number of comments for subcategory {specific_subcategory} on {specific_date} by buyers: {count_comments_specific_date}")
