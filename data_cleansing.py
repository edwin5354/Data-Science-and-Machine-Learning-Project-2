import pandas as pd

df = pd.read_csv("./download.csv", index_col=0)

# Data cleansing
df['price'] = df['price'].str.replace("$","")
df['price'] = df['price'].str.replace("M","")

df['area'] = df['area'].str.replace(',', '')

df['price'] = df['price'].astype('float64')
df['area'] = df['area'].astype('int64')

# Create new column price per feet
df['ppf'] = round((df['price'] / df['area']) * (10**6)) # convert million to dollars

# Create dictionary as regions (New Territories, Kowloon, HK Island)
region_dict = {
    'HK Island': ['Mid-Levels Central'],
    'Kowloon': ['Tseung Kwan O', 'Kwun Tong'],
    'NT East': ['Fo Tan', 'Pak Shek Kok', 'Tai Wai', 'Pak Shek Kok'],
    'NT West': ['Wu Kai Sha', 'Yuen Long Southeast', 
                'Tuen Mun Town Centre', 'Ma Wan', 'Luk Yeung',
                'Tsuen Wan West', 'Tin Shui Wai', 'Yuen Long Town Centre',
                'Tuen Mun San Hui', 'Discovery Park', 'Yuen Long Station',
                'Tung Chung Town Centre']
}

def get_region(district):
    for region, districts in region_dict.items():
        if district in districts:
            return region

df['region'] = df['district'].apply(get_region)

df.to_csv("./cleaned.csv")