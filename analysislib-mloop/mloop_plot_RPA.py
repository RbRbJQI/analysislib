import lyse
import numpy as np
import matplotlib.pyplot as plt
import mloop_config
from fake_result import fake_result

try:
    df = lyse.data()
    config = mloop_config.get()
    x=[]
    # print(len(config['mloop_params']))
    for ind in np.arange(len(config['mloop_params'])):
        # print(ind)
        x.append( list(config['mloop_params'])[ind])
    y = config['cost_key']
    # print(y)
    try:
        # Try to use the most recent mloop_session ID
        gb = df.groupby('mloop_session')
        mloop_session = list(gb.groups.keys())[-1]
        subdf = gb.get_group(mloop_session)
    except Exception as e:
        # Fallback to the entire lyse DataFrame
        subdf = df
        mloop_session = None
        print(e)
        
    for ind in np.arange(len(config['mloop_params'])):
        plt.figure(str(x[ind]))
        subdf.plot(x=x[ind], y=y, kind='scatter')
        # print(x[ind],y)
        x_p = np.linspace(df[x[ind]].min(), df[x[ind]].max(), 200)
        # plt.plot(x_p, fake_result(x_p, s=0))
        # plt.axis(ymin=18500, ymax=27500)
        plt.title('M-LOOP session: {:}'.format(mloop_session))
        # plt.show()
except Exception as e:
    print (e)