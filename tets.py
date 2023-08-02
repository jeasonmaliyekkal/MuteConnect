import pandas as pd

# Create a DataFrame with the correct columns
df = pd.DataFrame(columns=['timestamp', 'landmarks', 'hand_sign_id'])

# Write the DataFrame to a CSV file
df.to_csv('log.csv', index=False)