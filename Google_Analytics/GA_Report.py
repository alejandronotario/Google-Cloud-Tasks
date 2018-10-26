#!/usr/bin/env python


#Links:

# https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#ReportData.FIELDS.sampling_space_sizes

# https://note.nkmk.me/python-google-analytics-reporting-api-download/

# https://stackoverflow.com/questions/44296648/using-lists-in-pandas-to-replace-column-names

# http://code.markedmondson.me/googleAnalyticsR/v4.html

# https://www.themarketingtechnologist.co/getting-started-with-the-google-analytics-reporting-api-in-python/

# https://stackoverflow.com/questions/38084770/converting-google-analytics-reporting-api-v4-request-results-to-csv-with-python

# https://medium.com/analytics-for-humans/submitting-your-first-google-analytics-reporting-api-request-cdda19969940

# #https://stackoverflow.com/questions/44296648/using-lists-in-pandas-to-replace-column-names


# Libraries:

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
import numpy
import json
from pandas.io.json import json_normalize

# Account settings

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'	
VIEW_ID = 'your_VIEW_ID'

"""Google Analytics Reporting API V4."""

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

# Build the service object.

  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics

# first chunk

# This API in Python allows to get up to 100000 rows. The code below defines the first chunk. It is defined by pageToken='1' and pageSize=99999 

# In this example are included some metrics and dimensions as an example design, of course depending on each report design the change. Maximum 7 dimensions

# Date range in this example is from 7 days ago to today, of course it depends on each kind of report

def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  pageToken='1'
  pageSize=99999
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': datetime.strftime(datetime.now() - timedelta(days = 7),'%Y-%m-%d'), 'endDate': datetime.strftime(datetime.now(),'%Y-%m-%d')}],
          'metrics': [{'expression': 'ga:Sessions'},{'expression': 'ga:Pageviews'},{'expression': 'ga:timeOnPage'},{'expression': 'ga:uniquePageviews'},{'expression': 'ga:pageviewsPerSession'}],
          'dimensions': [{'name': 'ga:dimension4'},{'name': 'ga:dateHourMinute'},{'name': 'ga:pageTitle'}, {'name':'ga:contentGroup1'},{'name':'ga:dimension10'}],
	  'samplingLevel':'LARGE',
          'pageToken':pageToken,
          'pageSize': pageSize
          
        }]
      }
  ).execute()

# Parsing data

# First calling samplesReadCounts and samplingSpaceSizes, they give us if the data is sampled or not getting an output

# Then it is defined the file in .csv format with columns names and saving it in the same path it is running the script

def parse_data(response):
  
  sample_sizes=response['reports'][0]['data'].get('samplesReadCounts')
  sample_spaces=response['reports'][0]['data'].get('samplingSpaceSizes')
  print(sample_sizes)
  print(sample_spaces)
  if sample_sizes and sample_spaces:
    print ('Sampled Data!')
  else:
    print ('No Sampled Data')
  reports = response['reports'][0]
  columnHeader = reports['columnHeader']['dimensions']
  metricHeader = reports['columnHeader']['metricHeader']['metricHeaderEntries']

  columns = columnHeader
  for metric in metricHeader:
    columns.append(metric['name'])
  

  data = json_normalize(reports['data']['rows'])

  data_dimensions = pd.DataFrame(data['dimensions'].tolist())
  data_metrics = pd.DataFrame(data['metrics'].tolist())
  data_metrics = data_metrics.applymap(lambda x: x['values'])
  data_metrics = pd.DataFrame(data_metrics[0].tolist())
  result = pd.concat([data_dimensions, data_metrics], axis=1, ignore_index=True)
  
  columns_names=('dimension4','dateHourMinute','pageTitle','contentGroup1','Sessions','pageViews','timeOnPage','uniquePageViews','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTraffic.csv', encoding='utf8')

  return result


def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)  
  parse_data(response)
if __name__ == '__main__':
  main()


# Sequence of chunks

# Here pageToken and pageSize are defined on file shape, using it to get the last shape to define them

def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  webTraffic=pd.read_csv('./webTraffic.csv',sep=',',low_memory=False)
  pageToken=str(webTraffic.shape[0]+1)
  pageSize=int(pageToken)+99999
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': datetime.strftime(datetime.now() - timedelta(days = 7),'%Y-%m-%d'), 'endDate': datetime.strftime(datetime.now(),'%Y-%m-%d')}],
          'metrics': [{'expression': 'ga:Sessions'},{'expression': 'ga:Pageviews'},{'expression': 'ga:timeOnPage'},{'expression': 'ga:uniquePageviews'},{'expression': 'ga:pageviewsPerSession'}],
          'dimensions': [{'name': 'ga:dimension4'},{'name': 'ga:dateHourMinute'},{'name': 'ga:pageTitle'}, {'name':'ga:contentGroup1'},{'name':'ga:dimension10'}],
	  'samplingLevel':'LARGE',
          'pageToken':pageToken,
          'pageSize': pageSize
          
        }]
      }
  ).execute()

# Here at parsing the file is saved woth mode 'a' to add new rows an repeat the time you need

def parse_data(response):

  reports = response['reports'][0]
  columnHeader = reports['columnHeader']['dimensions']
  metricHeader = reports['columnHeader']['metricHeader']['metricHeaderEntries']

  columns = columnHeader
  for metric in metricHeader:
    columns.append(metric['name'])
  

  data = json_normalize(reports['data']['rows'])
  data_dimensions = pd.DataFrame(data['dimensions'].tolist())
  data_metrics = pd.DataFrame(data['metrics'].tolist())
  data_metrics = data_metrics.applymap(lambda x: x['values'])
  data_metrics = pd.DataFrame(data_metrics[0].tolist())
  result = pd.concat([data_dimensions, data_metrics], axis=1, ignore_index=True)  
  columns_names=('dimension4','dateHourMinute','pageTitle','contentGroup1','Sessions','pageViews','timeOnPage','uniquePageViews','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTraffic.csv', encoding='utf8', mode='a', header=False)

  return result

# Running the functions x times. This x depends on the typical size of the reports. There is no problem if the iteration is longer than you need. Is it easy to check if it has stopped before ending 
# calling the file shape, if it is as X00000 there are pending rows

def main():
  for _ in range(x):
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    parse_data(response)
if __name__ == '__main__':
  main()

