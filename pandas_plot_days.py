
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md

matplotlib.rcParams['timezone'] = 'US/Eastern'

# timestamps are in UTC that need to be converted to my timezone
# and make it the index
df = pd.read_csv("data.csv")
df.timestamp = pd.to_datetime(df.timestamp).dt.tz_convert('US/Eastern')
df.index = df.timestamp

# both plots in same figure
# mostly from https://matplotlib.org/gallery/api/two_scales.html
fig, ax1 = plt.subplots()
ax1.plot(df.index, df.consumption, 'bo', df.index, df.consumption, 'b-')

# format timestamps on the x axis
xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
days = md.DayLocator()
ax1.xaxis.set_major_locator(days)
ax1.xaxis.set_major_formatter(xfmt)
# and rotate them 30 degrees
ax1.tick_params( rotation=30 )
ax1.set_ylabel('consumption kWh')

# resampled hourly
# UWE: this does not work because holes are backfilled, causing spike
# for upsampled periods
#resampled = df.resample('H').pad().bfill()

# from https://stackoverflow.com/questions/25234941/python-regularise-irregular-time-series-with-linear-interpolation
rs = pd.DataFrame (index=df.resample('H').pad().iloc[1:].index)
idx_after = np.searchsorted(df.index.values, rs.index.values)
rs['after'] = df.loc[df.index[idx_after], 'consumption'].values
rs['before'] = df.loc[df.index[idx_after - 1], 'consumption'].values
rs['after_time'] = df.index[idx_after]
rs['before_time'] = df.index[idx_after - 1]

rs['span'] = (rs['after_time'] - rs['before_time'])
rs['after_weight'] = (rs['after_time'] - rs.index) / rs['span']
rs['before_weight'] = (pd.Series(data=rs.index, index=rs.index) - rs['before_time']) / rs['span']

rs['consumption'] = rs.eval('after * before_weight + before * after_weight')

print ("rs ", rs)
ax1.plot(rs.index, rs.consumption, 'g*', rs.index, rs.consumption, 'k')

df2 = rs.copy()
df2.timestamp = df2.index

# plot daily mean
df3 = df2.resample('D').pad()
#df3 = pd.DataFrame (index=df2.resample('D').pad().iloc[1:].index)
print ('df3 ', df3)
#fig2, ax3 = plt.subplots()
ax1.plot(df3.index, df3.consumption, 'c^')

numer = df3.consumption.diff()
print ("numer ", numer)
# deltat is 1 hour
#deltat = df2.timestamp.diff()
#print ("deltat ", deltat)
#seconds = deltat.dt.total_seconds()
#denom = seconds / 3600
#print ("denom ", denom)
derivative = numer / 24.0
print ("derivative ", derivative)
# force derivative of first point to 0
derivative[0] = 0

ax2 = ax1.twinx()  # instantiate a second axis that shares the same x-axis
ax2.plot(df3.index, derivative)
xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
days = md.DayLocator()
ax2.xaxis.set_major_locator(days)
ax2.xaxis.set_major_formatter(xfmt)
ax2.set_ylabel('kW')

# calculate and plot overall hourly rate - the mean
# on the same axis as first derivative
totalperiod = df.timestamp[df.timestamp.size-1]-df.timestamp[0]
totalhours = totalperiod.total_seconds() / 3600
totalcons = df.consumption[df.consumption.size-1] - df.consumption[0]
meanvalue = totalcons / totalhours
meantimes = (df.timestamp[0], df.timestamp[df.timestamp.size-1])
timeseries = pd.Series(meantimes)
print ("timeseries ", timeseries)
meanvals = (meanvalue, meanvalue)
valseries = pd.Series(meanvals)
print ("valseries ", valseries)
ax2.plot(timeseries, valseries, 'r-')
annot = 'mean ' + str(meanvalue)
print ('annot ', annot)
ax2.annotate(annot, xy=(0.5, 0.72),  xycoords='figure fraction',
        xytext=(0.5, 0.8), textcoords='axes fraction',
        arrowprops=dict(facecolor='red', shrink=0.05),
        horizontalalignment='left', verticalalignment='top',
        )

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.show()

