
def format_urls(dataset_name: str, dataset_id: str, data_dates: list):
    '''Function to format urls with the appropriate format'''

    # Move this into a config in the future
    base_urls = {
        'TileMovement': 'https://www.facebook.com/geoinsights-portal/downloads/vector/?id={}&ds={}'
    }

    date_formats = {
        'TileMovement': '%Y-%m-%d+%H%M'
    }

    # https://www.facebook.com/geoinsights-portal/downloads/vector/?id=1671212783027520&ds=2020-03-10+0000#

    base_url = base_urls[dataset_name]

    date_format = date_formats[dataset_name]

    urls = []

    for date in data_dates:

        urls.append({
            'url': base_url.format(dataset_id, date.strftime(date_format)),
            'date': date
        })

    return(urls)
