# electric-meter-monitoring
# DIY Home-made IoT: Electric Meter Monitoring

by Uwe Zimmermann

Gambit Communications


## 1. Abstract

Smart meter analytics are common on an industrial scale, eg.

https://www.sagewell.com/smart-meter-analytics.html

This DIY project affordably implements collection and simple statistical
for a residential electric meter in your own home or business. Follow-up projects
can expand on the analytics of the collected data set.

## 2. Overview

Every month your electric utility sends you a statement with some
crude monthly analytics comparing the last month to the prior
months.

<img src=IMG_20200408_103136.jpg width=200>

But, wouldn't it be nice to report better analytics, such as relative
hourly electricity usage, so that you know when you are using the
most electricity? Or alert you in a timely way when your usage is
out of the ordinary? This would let you fine-tune your electricity
consumption, find waste, and ultimately save money.

There are commercial systems on the market that attempt to help you
(google "electric usage monitor") either based on an electrical plug
widget, or whole house (such as the Sense for $300).

This project implements such a system in under $100 added cost
(assuming you already have a PC) using off-the-shelf, standards-based
hardware and open-source or low-cost software:

1) a Raspberry Pi ($50)

2) a SDR receiver ($40)

3) MQTT

4) NODE-RED

5) Home Assistant

6) MIMIC MQTT Lab ($0.10/hour)

The added benefit is that this setup is extensible to use a miriad of
applicable software out there.

## 3. Hardware

Most electric meters in the U.S. broadcast consumption telemetry that
can be received with low-cost SDR (software defined radio) receivers

https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/

The SDR receiver

https://www.amazon.com/NooElec-NESDR-Smart-Bundle-R820T2-Based/dp/B01GDN1T4S

is connected over USB to an old Raspberry Pi (Model B Rev 2) with 512 MB RAM

https://www.raspberrypi.org/

<IMG src=IMG_20200224_084354.jpg width=200>

and it receives the telemetry broadcast by your electric meter.
Since all your neighbors' electric (and other utility) meters are
also broadcasting, you need to identify your meter's ID visually.
For privacy, I blocked out the meter's ID below:

<IMG src=IMG_20200208_165158.jpg width=200>

## 4. Software

## 4.1. Collection

The open-source SDR software tools running on the Raspberry Pi

https://github.com/bemasher/rtlamr

and

https://github.com/seanauff/metermon

build and run fine on the Raspbian GNU/Linux 10 (buster)
version. Only 2 lines needed to be fixed in

metermon.py

to run on Python 2.7.16.

They collect the periodic telemetry (several times per hour, at seemingly
random intervals) and publish it via MQTT

https://mqtt.org/

to a MQTT broker running on the intranet. You could also publish to any
public broker (google "public MQTT broker").

From there it can now be digested by MQTT subscriber clients to
display and archive. The JSON telemetry appears such as

> metermon/690xxxxxx {"Type": "Electric", "Unit": "kWh", "Protocol": "SCM+", "ID": "690xxxxx", "Consumption": 24043.43}

The open-source Home Assistant

https://www.home-assistant.io/

has an electric meter integration that shows absolute electric consumption

<IMG src=hass-electric-meter-2.png width=400>

or hourly, daily, monthly

https://community.home-assistant.io/t/daily-energy-monitoring/143436

<IMG src=hass-electric-hourly.png width=400>

but does not store long-term data, nor does it provide neat hourly
or daily usage graphs.

## 4.2. Archival

That's where NODE-RED running on a virtual machine (VM) comes in

https://nodered.org/

to collect the telemetry and store it. You could store the telemetry in
a database, but a flat file suffices. This NODE-RED flow collects JSON
telemetry from the MQTT topic and stores it in CSV format with a timestamp in a file:

## 4.3. Analysis

The telemetry data is a time series

<A HREF=https://en.wikipedia.org/wiki/Time_series>
https://en.wikipedia.org/wiki/Time_series
</A>

of absolute energy consumption values at irregular intervals.

## 4.4. MIMIC MQTT Lab

Since the meter only generates telemetry a couple of times per hour,
it takes forever to accumulate a time series large enough to do testing.
Also, the data is arbitrary, so it's hard to verify accuracy of the
processing and analysis.

For that reason, we used the MQTT simulator in MIMIC MQTT Lab

https://mqttlab.iotsim.io/

to publish artificial telemetry (in addition to the real telemetry)
to generate different data sets to test the analytics.

Now, you can use any MQTT publisher client to generate the telemetry
to be consumed by NODE-RED, or even generate the data files by hand.
And we did that.  But in the early stages of this project we needed
to test the NODE-RED telemetry collection, rather than short-circuiting
parts of the system.

We setup a MQTT lab sensor to publish the telemetry in the same format as
the real-world sensor to the topic <b>metermon/test</b> the public broker mqtt.eclipse.org,
then had a NODE-RED flow read that telemetry and process it, as shown here

<IMG src=nodered-mimic.png width=400>
  
Since our simulated sensor was publishing at a much higher rate than the real sensor,
eg. every couple of seconds, rather than a couple of times per hour, we got
that task done in a fraction of the time.

Then we quickly generated several test data sets to develop and exercise our
statistical analysis and plotting. We could generate the same data sets with
scripting and or text editting, but since we already had the lab setup, it was
just a matter of tweaking a couple of values and MIMIC scripts.

TODO sample plots

## 5. Next steps

1. Instead of a flat file, use a database such as MySQL.

2. Longer term analytics, such as seasonal.

3. Correlation to other factors, such as weather.

4. Investigate how commercial IoT platforms handle this use case.

                                                              229,0-
