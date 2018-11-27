#!/usr/bin/env python


#Links:

#https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#ReportData.FIELDS.sampling_space_sizes

#https://note.nkmk.me/python-google-analytics-reporting-api-download/

# https://stackoverflow.com/questions/44296648/using-lists-in-pandas-to-replace-column-names
# http://code.markedmondson.me/googleAnalyticsR/v4.html

# https://www.themarketingtechnologist.co/getting-started-with-the-google-analytics-reporting-api-in-python/

# https://stackoverflow.com/questions/38084770/converting-google-analytics-reporting-api-v4-request-results-to-csv-with-python

# https://medium.com/analytics-for-humans/submitting-your-first-google-analytics-reporting-api-request-cdda19969940

# #https://stackoverflow.com/questions/44296648/using-lists-in-pandas-to-replace-column-names




#Libraries

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
import numpy
import json
from pandas.io.json import json_normalize
import sys

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'	
VIEW_ID = '88406164'

"""Google Analytics Reporting API V4."""

print("Enter startDate:")
startDate = input()
print("Enter timedelta(days):")
x=input()
start=datetime.strptime(startDate,'%Y-%m-%d')
endDate=datetime.strftime(start + timedelta(days = x),'%Y-%m-%d')

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

#Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics

#first chunk

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
          'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
          'metrics': [{'expression': 'ga:Sessions'},{'expression': 'ga:Pageviews'},{'expression': 'ga:timeOnPage'},{'expression': 'ga:pageviewsPerSession'}],
          'dimensions': [{'name': 'ga:dimension4'},{'name': 'ga:dateHourMinute'},{'name': 'ga:pageTitle'}, {'name':'ga:dimension5'},{'name':'ga:dimension6'},{'name':'ga:contentGroup1'},
		{'name':'ga:dimension10'}],
	  'samplingLevel':'LARGE',
          'pageToken':pageToken,
          'pageSize': pageSize
          
        }]
      }
  ).execute()


def parse_data(response):

  
  sample_sizes=response['reports'][0]['data'].get('samplesReadCounts')
  sample_spaces=response['reports'][0]['data'].get('samplingSpaceSizes')
  
  if sample_sizes and sample_spaces:
    sys.exit('Sampled Data!')  
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
  
  columns_names=('id_user','date','pageTitle','url','referrer','contentGroup1','pageAccess','sessions','pageViews','timeOnPage','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTraffic_{}.csv'.format(startDate), encoding='utf8')

  return result

def parse_data_complete(response):
 
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
  
  columns_names=('id_user','date','pageTitle','url','referrer','contentGroup1','pageAccess','sessions','pageViews','timeOnPage','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTrafficYear.csv', encoding='utf8',mode='a', header=False)

  return result


def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)  
  parse_data(response)
  parse_data_complete(response)
if __name__ == '__main__':
  main()


#sequence of chunks

def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """

  webTraffic=pd.read_csv('./webTraffic_{}.csv'.format(startDate),sep=',',low_memory=False)
  pageToken=str(webTraffic.shape[0]+1)
  pageSize=int(pageToken)+99999
  
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
          'metrics': [{'expression': 'ga:Sessions'},{'expression': 'ga:Pageviews'},{'expression': 'ga:timeOnPage'},{'expression': 'ga:pageviewsPerSession'}],
          'dimensions': [{'name': 'ga:dimension4'},{'name': 'ga:dateHourMinute'},{'name': 'ga:pageTitle'}, {'name':'ga:dimension5'},{'name':'ga:dimension6'},{'name':'ga:contentGroup1'},
		{'name':'ga:dimension10'}],
	  'samplingLevel':'LARGE',
          'pageToken':pageToken,
          'pageSize': pageSize
          
        }]
      }
  ).execute()



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
  columns_names=('id_user','date','pageTitle','url','referrer','contentGroup1','pageAccess','sessions','pageViews','timeOnPage','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTraffic_{}.csv'.format(startDate), encoding='utf8', mode='a', header=False)

  return result

def parse_data_complete(response):
 
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
  
  columns_names=('id_user','date','pageTitle','url','referrer','contentGroup1','pageAccess','sessions','pageViews','timeOnPage','pageViewsPerSession')
  result.columns=columns_names
  result=result.to_csv('webTrafficYear.csv', encoding='utf8',mode='a', header=False)

  return result


def main():
  for _ in range(10):
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    parse_data(response)
    parse_data_complete(response)

if __name__ == '__main__':
  try:
    main()
  except KeyError:
    pass






