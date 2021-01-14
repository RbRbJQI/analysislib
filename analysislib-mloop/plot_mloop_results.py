import lyse
import numpy as np
import matplotlib.pyplot as plt
import mloop_config
from fake_result import fake_result
import warnings
warnings.filterwarnings("ignore")

try:
    df = lyse.data()
    config = mloop_config.get()
    # x = list(config['mloop_params'])[7]
    x = 'B_bias_mol_y'
    y = 'compress_freq'
    z = config['cost_key']
    try:
        # Try to use the most recent mloop_session ID
        gb = df.groupby('mloop_session')
        mloop_session = list(gb.groups.keys())[-1]
        subdf = gb.get_group(mloop_session)
    except Exception:
        # Fallback to the entire lyse DataFrame
        subdf = df
        mloop_session = None
    subdf.plot(x=x, y=y, kind='scatter', color=(1,1,1))
    x_p = np.linspace(df[x].min(), df[x].max(), 200)
    # plt.plot(x_p, fake_result(x_p, s=0))
    plt.axis(ymin=df[y].min(), ymax=df[y].max())
    plt.title('M-LOOP session: {:}'.format(mloop_session))
    max_level = np.nanmax(subdf[z].values)
    # print(subdf[z].values)
    for ind in range(len(subdf.index)):
        try:
            if subdf.iloc[ind][z].values[0]>2550:
                dist = []
                for rind in list(config['mloop_params']):
                    if type(subdf.iloc[ind][rind].values[0])==np.float64 or type(subdf.iloc[ind][rind].values[0])==np.int64:
                        new_dist = (subdf.iloc[ind][rind].values[0]-subdf.iloc[0][rind].values[0])**2/(np.max(subdf[rind].values)-np.min(subdf[rind].values))**2
                        # print(rind, subdf.iloc[ind][rind].values[0]-subdf.iloc[0][rind].values[0], np.max(subdf[rind].values)- np.min(subdf[rind].values), new_dist)
                        if not np.isnan(new_dist):
                            dist.append(new_dist)
                dist = np.sqrt(np.array(dist))
                large_dist = max(dist)
                large_dist_par = list(config['mloop_params'])[list(dist).index(large_dist)]
                
                # print(dist)
                sum_dist = round(np.sum(dist/len(dist)),3)
                if sum_dist>0.06:
                    print('dist_from_org=', sum_dist, 'cost=', subdf.iloc[ind][z].values[0])
                    print(large_dist_par, round(large_dist,3), df.iloc[ind]['filepath'].values, '\n\n')
                
            if abs(subdf.iloc[ind][z].values[0]-2.85e3)<50:
                plt.annotate(str(int(subdf.iloc[ind][z].values[0])), (subdf.iloc[ind][x].values, subdf.iloc[ind][y].values))
            level = subdf.iloc[ind][z].values[0]
            scale = round(min(level/80e-3, 1), 1)
            plt.plot(subdf.iloc[ind][x].values, subdf.iloc[ind][y].values,  marker='o', markersize=3, color=(1,0,0, scale))
                
                
            if ind==len(subdf.index)-1 or ind==0:
                plt.plot(subdf.iloc[ind][x], subdf.iloc[ind][y],  marker='x', markersize=16, color="green")
                plt.annotate(str(round(subdf.iloc[ind][z].values[0],2)), (subdf.iloc[ind][x], subdf.iloc[ind][y]))
                # print(z,subdf.iloc[ind][z].values[0])
            if level==max_level:
                plt.plot(subdf.iloc[ind][x], subdf.iloc[ind][y],  marker='x', markersize=16, color="blue")
                plt.annotate(str(round(subdf.iloc[ind][z].values[0],2)), (subdf.iloc[ind][x], subdf.iloc[ind][y]))
                
        except Exception as e:
            print(e)
            print(subdf.iloc[ind][y].values[0])
            continue
    plt.show()
except Exception as e:
    print(e)
    pass
