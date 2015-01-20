#!/usr/bin/env python
"""
Brief     Easily manage your tasks with the commandline
Created   Jan 20 2015
Version   0.1
Author    bas080
"""

import datetime
import random
import string
import time
import sys
import os
import re

EDITOR=os.getenv('EDITOR')

#import argparse TODO

def main( args ):


  #get all the necessary arguments
  try:
    opt = args[1]
  except Exception, e:
    opt = ''

  try:
    val = args[2:]
  except Exception, e:
    val = []

  if len(args) < 2: #check if has no arguments
    list_tasks( )
    return '';

  opt = args[1]
  if opt == 'init':
    create_will( val );
  elif opt == 'list' or opt == 'ls':
    list_tasks( )
  elif opt == 'rm' or opt == 'remove':
    remove_task( val )
  elif opt == 'edit':
    edit_task( val )
  elif opt == 'view':
    view_task( val )
  elif opt == 'export':
    export_tasks( val )
  elif opt == 'find':
    find_tasks( val )
  elif args[1][0] == args[1][0].upper():
    create_task( args[1:] )
  else:
    usage()

def usage():
  print '''
will Subject title has to start with capital letter
  or
will init|remove|find|export|edit
'''

def remove_task( tasks ):
  total = 0
  print 'o = succes; x = failed (removal)'
  for task in tasks:
    task_file=find_will()+'/'+task+'.md'
    if os.path.exists( task_file ):
      os.remove ( task_file )
      total = total + 1
      print 'o '+task_file
    else:
      print 'x '+task_file

  print str(total)+' tasks removed'
  sys.exit(0);

def edit_task( params ):
  task_file=str(find_will()+'/'+params[0])+".md"
  command=EDITOR+" "+task_file
  os.system( command )
  sys.exit(0)
  #subprocess.Popen( command )

def find_will( ):
  path = os.path.abspath( __file__ )
  path = os.path.abspath( os.path.join( path, os.pardir ) )
  while True:
    path = os.path.abspath( os.path.join( path, os.pardir ) )
    will = path+'/.will'
    if os.path.isdir( will ):
      return path+'/.will'

def create_will( params ):
  path=' '.join(params)
  if path == '':
    path = os.getcwd()+'/.will'
  else:
    path = path+'/.will'
  if not os.path.exists( path ):
    os.makedirs( path )
    print 'created .will'
    return True
  else:
    print '.will directory already exists'
    return False

def create_task( params ):

  subject=' '.join( params )

  task_file=str(find_will()+'/'+str(random.randint( 10000, 99999 )))+".md"

  with open( task_file, 'w+' ) as f:
    f.write(subject+'\n')
    f.write( re.sub('.', '=', subject)+'\n')
    f.write( 'description of the task here\n' )
    f.write( datetime.datetime.now().strftime('%b %d %Y') )

  command=EDITOR+" "+task_file
  os.system( command )
  #subprocess.Popen( command )

def find_task( match ):
  print 'find the task corresponding to ID or keywords'
  #check files for regex matches

def get_tasks():
  tasks = [];
  path = find_will();
  for (dirpath, dirnames, filenames) in os.walk( path ):
    tasks = filenames;
    break
  for index, task in enumerate(tasks):
    tasks[index] = path+'/'+task
  return tasks;


def list_tasks( ):
  rows = []
  for task in get_tasks():

    lines = get_task_lines( task )
    # cleanup the lines by removing empty strings. This removes empty lines
    # after the file of empty files between title and description
    index=0;
    for line in lines:
      if not line == '':
        lines[index] = line;
      index = index + 1
    lines = lines[0:index]

    task_identif = task.split('/')[-1][0:-3] #filename without file extension
    task_subject = get_task_subject     ( lines )
    task_categor = get_task_categories  ( lines )
    task_descrip = get_task_description ( lines )
    task_duratio = get_task_duration    ( lines );

    #print task_identif+'\t'+task_subject+'\t'+task_categor+'\t'+task_descrip+'\t'+task_duratio
    rows.append([ task_identif, task_subject, task_categor, task_descrip, task_duratio]);
  rows.insert(0, [ 'TASK', 'SUBJECT', 'CATEGORY', 'DESCRIPTION', 'DEADLINE' ] )
  collumnize( rows, [5, 24, 12, 32, 15] ) #including the 2 spaces after each collumn
  sys.exit(0);

def collumnize( rows, widths ):
  def length( string, length):

    string_length = len ( str ( string ) )

    #print str( string_length ) +' '+ str( length )

    if string_length >= length:
      return string[0:length]
    else:
      def spaces( amount ):
        string=''
        for i in range( 0, amount ):
          string = string + ' '
        return string
      #print string_length - length
      return string + spaces( length - string_length )

  for row in rows:
    line = ''
    for index, field in enumerate(row):
      line = line + length( field, widths[index] ) + '  '
    print line

def get_task_duration( lines ):
  line = lines[-2]
  try:
    due_date = int( datetime.datetime.strptime( line.split('\t')[0], '%d %b %Y').strftime('%s'));
    cur_date = int( datetime.datetime.now().strftime('%s') );
    if due_date > cur_date:
      return duration( due_date - cur_date );
    else:
      return '-'+duration( cur_date - due_date )
  except Exception, e:
    return line

def get_task_subject( lines ):
  try:
    return lines[0].split('\t')[0];
  except Exception, e:
    return ''

def get_task_categories( lines ):
  try:
    string=''
    categories = lines[0].split('\t')[1:]
    sublen = 12 / len(categories)
    for category in lines[0].split('\t')[1:]:
      string=string+category[0:sublen].capitalize()+'';
    return string
  except Exception, e:
    return '...'

def get_task_description( lines ):
  try:
    return lines[2];
  except Exception, e:
    return ''

def get_task_lines( task ):
  with open( task, 'r' ) as task_file:
    return task_file.read().split('\n');

def duration(seconds, suffixes=['y','w','d','h','m','s'], add_s=False, separator=' '):
  # the formatted time string to be returned
  time = []
  # the pieces of time to iterate over (days, hours, minutes, etc)
  # - the first piece in each tuple is the suffix (d, h, w)
  # - the second piece is the length in seconds (a day is 60s * 60m * 24h)
  parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
  (suffixes[1], 60 * 60 * 24 * 7),
  (suffixes[2], 60 * 60 * 24),
  (suffixes[3], 60 * 60)
  #(suffixes[4], 60)
  #(suffixes[5], 1)
  ]
  # for each time piece, grab the value and remaining seconds, and add it to
  # the time string
  for suffix, length in parts:
    value = seconds / length
    if value > 0:
      seconds = seconds % length
      time.append('%s%s' % (str(value),
      (suffix, (suffix, suffix + 's')[value > 1])[add_s]))
    if seconds < 1:
      break
  return separator.join(time)

print main ( sys.argv );


