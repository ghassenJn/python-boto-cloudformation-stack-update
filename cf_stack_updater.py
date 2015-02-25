#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Nalinda Karunaratna"
__version__ = "0.0.1"

import boto.cloudformation
import time
import datetime
import json
import argparse

parser = argparse.ArgumentParser(description='Update CloudFromation Stacks')
parser.add_argument("-v", "--region", help="AWS Region", type=str)
parser.add_argument("-s", "--stack_name", help="Cloudformation Stack Name", type=str)
parser.add_argument("-t", "--template_body", help="Cloudformation template body, JSON", type=str)
parser.add_argument("-p", "--template_params", help="Cloudformation template parameters, JSON", type=str)
args = parser.parse_args()

# Get the time stamp
def timestamp():
  return datetime.datetime.utcnow()

# Passing variables
region = args.region
stack_name = args.stack_name
json_temp_body = args.template_body
json_temp_params = args.template_params

# Creation CF Connection
cf_connection = boto.cloudformation.connect_to_region(region)

# Preparing templates and parameters
temp_body = open(json_temp_body).read()
json_params = open(json_temp_params)

temp_params = json.load(json_params)
json_params.close()

# JSON Validator
def parse(text):
  try:
    return json.loads(text)
  except ValueError as e:
    print("Invalid JSON : %s" % e)
    return exit(1)

# Validating JSON file
parse(open(tem_body))
parse(open(json_temp_params).read())

# Validate Cloudformation template
try:
  cf_connection.validate_template(template_body=temp_body)
  print(str(timestamp()) + " " + "Template validation : Passed")
except boto.exception.BotoServerError, e:
  print(str(timestamp()) + " " + e.error_message)

# Assigning parameters to a Python list
params_list = []
for param in temp_params:
  params_list.append((param["ParameterKey"], param["ParameterValue"]))

# Updating CF stack
try:
  cf_connection.update_stack(stack_name, 
template_body=temp_body,
template_url=None,
parameters=params_list, 
notification_arns=[], 
disable_rollback=False, 
timeout_in_minutes=None, 
capabilities=None)
except boto.exception.BotoServerError, e:
  error_state = e.error_message
  print(str(timestamp()) + " " + "Stack update notification : " + error_state)

# Monitoring Stack Updates
try:
   evntsdata = str(cf_connection.describe_stack_events(stack_name)[0]).split(" ")
   if evntsdata[-1] == 'UPDATE_IN_PROGRESS' or evntsdata[-1] == 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS':
     loopcontinue = True
     while loopcontinue:
       evntsdata = str(cf_connection.describe_stack_events(stack_name)[0]).split(" ")
       if (evntsdata[-1] == 'UPDATE_COMPLETE' and evntsdata[-3] == 'AWS::CloudFormation::Stack'):
         loopcontinue = False
         print(str(timestamp()) + " " + "Stack Update is Completed!" + ' - ' + evntsdata[-3] + ' = ' + evntsdata[-1])
       else:
         print(str(timestamp()) + " " + "Stack Update in Progress!" + ' - ' + evntsdata[-3] + ' = ' + evntsdata[-1])
         time.sleep(10)
   elif error_state == 'No updates are to be performed':
     exit(0)
except:
   print(str(timestamp()) + " " + "ERROR: Stack Update Failure")
