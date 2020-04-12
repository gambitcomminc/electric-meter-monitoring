
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

# alternative 1 - separate plots
# mostly from https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/04_plotting.html
def plot_alternative1 (df, timestamps):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(timestamps, df.consumption, 'bo', timestamps, df.consumption, 'k')
    # format timestamps on the x axis
    ax=plt.gca()
    xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
    days = md.DayLocator()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(xfmt)
    # and rotate them 30 degrees
    plt.xticks( rotation=30 )
    plt.ylabel('consumption kWh')

    numer = df.consumption.diff()
    print ("numer ", numer)
    deltat = timestamps.diff()
    print ("deltat ", deltat)
    seconds = deltat.dt.total_seconds()
    denom = seconds / 3600
    print ("denom ", denom)
    derivative = numer / denom
    print ("derivative ", derivative)
    # force derivative of first point to 0
    derivative[0] = 0

    plt.subplot(212)
    #plt.plot (timestamps, derivative)
    series1 = pd.Series (derivative.values, index=timestamps)
    series1.plot()
    ax=plt.gca()
    xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
    days = md.DayLocator()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30 )
    plt.ylabel('kW')

# alternative 2 - both plots in same figure
# mostly from https://matplotlib.org/gallery/api/two_scales.html
def plot_alternative2 (df, timestamps):
    fig, ax1 = plt.subplots()
    ax1.plot(timestamps, df.consumption, 'bo', timestamps, df.consumption, 'k')
    # format timestamps on the x axis
    xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
    days = md.DayLocator()
    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(xfmt)
    # and rotate them 30 degrees
    ax1.tick_params( rotation=30 )
    ax1.set_ylabel('consumption kWh')

    numer = df.consumption.diff()
    print ("numer ", numer)
    deltat = timestamps.diff()
    print ("deltat ", deltat)
    seconds = deltat.dt.total_seconds()
    denom = seconds / 3600
    print ("denom ", denom)
    derivative = numer / denom
    print ("derivative ", derivative)
    # force derivative of first point to 0
    derivative[0] = 0

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(timestamps, derivative)
    xfmt = md.DateFormatter('  %m-%d %H:%M:%S')
    days = md.DayLocator()
    ax2.xaxis.set_major_locator(days)
    ax2.xaxis.set_major_formatter(xfmt)
    ax2.set_ylabel('kW')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

df = pd.read_csv("data.csv")

utctimes = pd.to_datetime(df.timestamp)
#print ("utctimes ", utctimes)
timestamps = utctimes.dt.tz_convert('US/Eastern')
#print ("timestamps ", timestamps)

alternative = 2
if ( alternative == 1):
    plot_alternative1 (df, timestamps)
elif ( alternative == 2):
    plot_alternative2 (df, timestamps)

plt.show()

