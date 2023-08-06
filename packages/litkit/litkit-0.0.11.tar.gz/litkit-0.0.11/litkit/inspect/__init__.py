import datetime
import pandas as pd
import numpy as np
from beeprint import pp
from plotly import tools
from sklearn.base import BaseEstimator
from jinja2 import Template

from litkit.utils import open_file

import plotly.offline as py
import plotly.graph_objs as go


pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def show_images(data, title=None, transpose=False, reverse=False):
    image_handler = {
        True: {
            True: __show_single_rgb,
            False: __show_multi_rgb,
        },
        False: {
            True: __show_single_heat,
            False: __show_multi_heat,
        }
    }

    is_rgb = False
    if data.shape[-1] == 3:
        is_rgb = True

    is_single = False
    if is_rgb and len(data.shape) == 3:
        is_single = True

    if not is_rgb and len(data.shape) == 2:
        is_single = True

    image_handler[is_rgb][is_single](data, title, transpose, reverse)


def __process_image(data, transpose, reverse):
    if transpose:
        data = data.T

    if reverse:
        data = data[::-1]

    return data


def __show_single_rgb(data, title, transpose, reverse):
    from keras.preprocessing import image

    img_paths = []
    for i in range(len(data)):
        img = image.array_to_img(data[i])

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

    p = "/tmp/abc/imgs_{}.html".format(datetime.datetime.utcnow())
    with open(p, 'w') as f:
        f.write(html)

    open_file(p)


def __show_multi_rgb(data, title, transpose, reverse):
    from keras.preprocessing import image

    img_paths = []
    for i in range(len(data)):
        d = data[i]

        d = __process_image(d, transpose, reverse)

        img = image.array_to_img(d)

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

    p = "/tmp/abc/imgs_{}.html".format(datetime.datetime.utcnow())
    with open(p, 'w') as f:
        f.write(html)

    open_file(p)


def __show_single_heat(data, title, transpose, reverse):
    data = __process_image(data, transpose, reverse)

    trace = go.Heatmap(z=data, colorscale='Viridis')
    data = [trace]

    fig = go.Figure(data=data)
    fig['layout'].update(title=title)
    py.plot(fig, filename='basic-heatmap')

    return


def __show_multi_heat(data, title, transpose, reverse):
    def __get_grid_length(n):
        for i in range(100):
            if i ** 2 < n < (i + 1) ** 2:
                return (i + 1)

    l = __get_grid_length(len(data))

    fig = tools.make_subplots(rows=l, cols=l)

    for i, d in enumerate(data):
        r = int(i / l // 1 + 1)
        c = int(i % l + 1)

        d = __process_image(d, transpose, reverse)

        fig.append_trace(go.Heatmap(z=d, colorscale='Viridis',), r, c)

    fig['layout'].update(title=title)
    py.plot(fig, filename='basic-heatmap')

    return


def info(obj: pd.DataFrame):
    print(type(obj))

    if isinstance(obj, np.ndarray):
        __np_info(obj)
        df = pd.DataFrame(obj)

        __df_info(df)
        return

    if isinstance(obj, pd.DataFrame):
        df = pd.DataFrame(obj)

        __df_info(df)
        return

    if isinstance(obj, BaseEstimator):
        if hasattr(obj, "coef_"):
            pp(obj.coef_)

        if hasattr(obj, "feature_importances_"):
            pp(obj.feature_importances_)

        pp(obj.__dict__)
        return

    if isinstance(obj, dict):
        pp(obj)
        return

    raise ValueError(type(obj))


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
