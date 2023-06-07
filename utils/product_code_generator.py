import pandas as pd
import datetime


def get_product_code():

    product_code = ''
    today = datetime.datetime.now().strftime("%Y%m%d")

    try:
        df = pd.read_pickle('product_code_cache.pkl')
        if df['date'] == today:
            df['today_code'] = df['today_code'] + 1
        else:
            df['date'] = today
            df['today_code'] = 0
            
    except:
        df = pd.Series([today, 0], index = ['date', 'today_code'])

    df.to_pickle('product_code_cache.pkl')
    product_code = df['date'] + "{0:03d}".format(df['today_code'])
        
    
    return product_code



if __name__ == "__main__":
    print(get_product_code())
