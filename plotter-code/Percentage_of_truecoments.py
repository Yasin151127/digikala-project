true_count = df['is_buyer'].sum()

print((true_count/len(df.index))*100)