specific_date = '2023-06-08'
specific_subcategory = 'travel'

comments_df['created_at'] = pd.to_datetime(comments_df['created_at'], format='%Y-%m-%d')

filtered_comments_df = comments_df[(comments_df['is_buyer'] == True) &
                                   (comments_df['created_at'] == pd.to_datetime(specific_date, format='%Y-%m-%d'))]

merged_df = filtered_comments_df.merge(products_df, left_on='product_id', right_on='id')

filtered_by_subcategory = merged_df[merged_df['sub_category'] == specific_subcategory]

total_price = filtered_by_subcategory['Price'].sum()

print(f"Total price of products for comments made by buyers on {specific_date} in subcategory {specific_subcategory}: {total_price}")