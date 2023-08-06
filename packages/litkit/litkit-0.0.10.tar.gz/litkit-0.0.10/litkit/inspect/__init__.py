import pandas as pd
import numpy as np
from beeprint import pp
from sklearn.base import BaseEstimator
from keras.preprocessing import image
from jinja2 import Template

from litkit.utils import open_file


pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def show_images(img_arrays):
    img_paths = []
    for i in range(len(img_arrays)):
        img = image.array_to_img(img_arrays[i])

        p = '/tmp/abc/img_{}.jpeg'.format(i)

        img.save(p)

        img_paths.append(p)

    tpl = """
    <html>
        <head>
        </head>
        <body>
        {% for path in image_paths %}
            <div style="float: left;">
            <p>{{loop.index - 1}}</p>    
            <img src="file://{{path}}"/>
            </div>    
        {% endfor %}
        </body>
    </html>
    """
    template = Template(tpl)
    html = template.render(image_paths=img_paths)

    with open("/tmp/abc/imgs.html", 'w') as f:
        f.write(html)

    open_file('/tmp/abc/imgs.html')

def info(obj: pd.DataFrame):
    if isinstance(obj, np.ndarray):
        __np_info(obj)
        df = pd.DataFrame(obj)

        __df_info(df)

    if isinstance(obj, pd.DataFrame):
        df = pd.DataFrame(obj)

        __df_info(df)

    if isinstance(obj, BaseEstimator):
        if hasattr(obj, "coef_"):
            pp(obj.coef_)

        if hasattr(obj, "feature_importances_"):
            pp(obj.coef_)

        pp(obj.__dict__)


def __np_info(arr: np.ndarray):
    print('ndim:     {}'.format(arr.ndim))
    print('shape:    {}'.format(arr.shape))
    print('size:     {}'.format(arr.size))
    print('dtype:    {}'.format(arr.dtype))
    print('itemsize: {}'.format(arr.itemsize))


def __df_info(df):
    stats = {
        'column': [],
        'type': [],
        'unique_n': [],
        'unique_samples': [],
        'nan_n': [],
        'non_nan_n': [],
        'length': [],
        'kB': [],
        'kB_deep': [],
        'mean': [],
        'std': [],
        'min': [],
        '25%th': [],
        '50%th': [],
        '75%th': [],
        '90%th': [],
        '99%th': [],
        'max': [],
    }

    for c in df.columns:
        s = df[c]
        stats['column'].append(c)
        stats['type'].append(s.dtype)
        u = s.unique()
        stats['unique_n'].append(len(u))

        if len(u) > 5:
            u = np.array(u[:5])
            try:
                if u.dtype == 'object':
                    u = u.astype('float')
            except:
                pass

            if np.issubdtype(u.dtype, np.number):
                u = np.around(u, 2)

        stats['unique_samples'].append(u)

        nan_c = s.isnull().sum()
        length = len(s)

        stats['nan_n'].append(nan_c)
        stats['non_nan_n'].append(length - nan_c)
        stats['length'].append(length)
        stats['kB'].append(round(s.memory_usage() / 1024, 1))
        stats['kB_deep'].append(round(s.memory_usage(deep=True) / 1024, 1))

        v = s.dropna().values
        try:
            if v.dtype == 'object':
                v = v.astype('float')
        except:
            stats['mean'].append(None)
            stats['std'].append(None)
            stats['min'].append(None)
            stats['25%th'].append(None)
            stats['50%th'].append(None)
            stats['75%th'].append(None)
            stats['90%th'].append(None)
            stats['99%th'].append(None)
            stats['max'].append(None)
            continue

        stats['mean'].append(round(np.mean(v), 1))
        stats['std'].append(round(np.std(v), 1))
        stats['min'].append(round(np.min(v), 1))
        stats['25%th'].append(round(np.percentile(v, 25), 2))
        stats['50%th'].append(round(np.percentile(v, 50), 2))
        stats['75%th'].append(round(np.percentile(v, 75), 2))
        stats['90%th'].append(round(np.percentile(v, 90), 2))
        stats['99%th'].append(round(np.percentile(v, 99), 2))
        stats['max'].append(round(np.max(v), 1))

    stats_df = pd.DataFrame(stats)

    stats_df = stats_df[['column', 'type', 'length', 'kB', 'kB_deep', 'nan_n', 'non_nan_n', 'unique_n', 'unique_samples', 'mean', 'std', 'min', '25%th', '50%th', '75%th', '90%th', '99%th', 'max']]

    print('\n\nmemory: {}kB deep: {}kB'.format(round(df.memory_usage().sum() / 1024, 1), round(df.memory_usage(deep=True).sum() / 1024, 1)))

    print('\ncolumn types:')

    pp(stats_df['type'].value_counts().sort_index())

    print()

    pp(stats_df)
