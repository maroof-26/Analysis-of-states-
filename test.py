from __future__ import division
import pandas as pd

# Importing CSVs
keys = pd.read_csv("/home/maroof/Downloads/Analysis of States - KEYS.csv")
census_population_state = pd.read_csv("/home/maroof/Downloads/Analysis of States - CENSUS_POPULATION_STATE.tsv", sep="\t")
census_mhi_estate = pd.read_csv("/home/maroof/Downloads/Analysis of States - CENSUS_MHI_STATE.csv")
redfin_median_sale_price = pd.read_csv("/home/maroof/Downloads/Analysis of States - REDFIN_MEDIAN_SALE_PRICE.csv", header =1)



#Helper Functions
def get_population(key):
    # getting row with pop size
    tmp_census = census_population_state[census_population_state['Label (Grouping)'].str.contains('Total population', case=False, na=False)]
    
    # getting col for particular state
    matching_cols = [col for col in tmp_census.columns 
                        if key.lower() in col.lower() and "estimate" in col.lower()]
    if matching_cols:
        value = tmp_census.iloc[0][matching_cols[0]]
    else:
        value = None

    return value


def get_median_income(key):
    
    # getting row with Households 
    tmp_census = census_mhi_estate[
        census_mhi_estate['Label (Grouping)'].str.contains('Households', case=False, na=False)
    ]
    
    # getting median income dollar col for particular state 
    matching_cols = [col for col in tmp_census.columns 
                    if key.lower() in col.lower() and "median income" in col.lower()]
    if matching_cols:
        return tmp_census.iloc[0][matching_cols[0]]
    
    return None

def get_median_sale_price(key):

    # getting row with particular region/state 
    tmp_df = redfin_median_sale_price[
        redfin_median_sale_price['Region'].str.contains(key, case=False, na=False)
    ]
    if not tmp_df.empty:
        # a little processing to comvert K to 1000s
        return tmp_df.iloc[0][-1].replace("K", "000").replace("$", "")
        
    return None
    
def get_suffix(rank):
    if 11 <= rank % 100 <= 13:
        return f"{rank}th"
    last_digit = rank % 10
    if last_digit == 1:
        return f"{rank}st"
    elif last_digit == 2:
        return f"{rank}nd"
    elif last_digit == 3:
        return f"{rank}rd"
    else:
        return f"{rank}th"

def create_blurb(state, rank, base_col_name):

    if base_col_name == "census_population":
        txt = f"{state.capitalize()} is {rank} in the nation in population among states, DC, and Puerto Rico."
    elif base_col_name == "median_household_income":
        txt = f"{state.capitalize()} is {rank} in median household income  among states, DC, and Puerto Rico."
    elif base_col_name == "median_sale_price":
        txt = f"{state.capitalize()} has the {rank} highest median sale price on homes in the nation in population among states, DC, and Puerto Rico."
    elif base_col_name == "house_affordability_ratio":
        txt = f"{state.capitalize()} has the {rank} lowest house affordability ratio in the nation in population among states, DC, and Puerto Rico."

    return txt


def add_necessary_information(df,
                              base_column_name,
                              rank_col_name,
                              blurb_col_name                              
                              ):
    
    """ Helper func to avoid redundancy in code"""
    
    df[base_column_name] = df[base_column_name].apply(
        lambda x: int(x.replace(",", "")) if isinstance(x, str) else x
    )

    asc_order = False
    if base_column_name == "house_affordability_ratio":
        asc_order = True

    df = df.sort_values(base_column_name,ascending=asc_order).reset_index().reset_index()
    df['level_0'] =df['level_0'] + 1
    df[rank_col_name] = df['level_0'].apply(get_suffix)

    
    df[blurb_col_name] = df.apply(
        lambda x: create_blurb(x['key_row'],x[rank_col_name], base_column_name) ,axis = 1
    )

    df.drop(columns=['index','level_0'],inplace=True)
    return df


# Excercise
keys = keys.dropna(subset=['zillow_region_name'])

keys['census_population']= keys['zillow_region_name'].apply(get_population)
keys = keys.dropna(subset=['census_population'])
keys = add_necessary_information(keys, 'census_population','population_rank','population_blurb')

keys['median_household_income'] = keys['zillow_region_name'].apply(get_median_income)
keys = add_necessary_information(keys, 'median_household_income','median_household_income_rank','median_household_income_blurb')

keys['median_sale_price'] = keys['zillow_region_name'].apply(get_median_sale_price)
keys = add_necessary_information(keys, 'median_sale_price','median_sale_price_rank','median_sale_price_blurb')

keys['house_affordability_ratio'] = keys['median_sale_price'] / keys['median_household_income']
keys = add_necessary_information(keys, 'house_affordability_ratio','house_affordability_ratio_rank','house_affordability_ratio_blurb')


keys = keys.drop(columns = [
    "realtor_cbsa_title",
    "zillow_region_name",
    "redfin_region",
    "census_msa",
    "region_type",
    "state_abbreviation",
    "alternative_name"
])
