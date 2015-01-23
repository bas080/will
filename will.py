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
#import argparse TODO for better argument parsing and extra features

EDITOR=os.getenv('EDITOR')

def main( args ):
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
    sys.exit( create_will( val ) )
  elif opt == 'list' or opt == 'ls':
    list_tasks( )
  elif opt == 'rm' or opt == 'remove':
    remove_task( val )
  elif opt == 'edit':
    edit_task( val )
  elif opt == 'view':
    view_tasks( val )
  elif opt == 'path':
    print find_will( )
  elif opt == 'export':
    export_tasks( val )
  elif opt == 'find':
    if val:
      tasks = find_tasks( val )
    else:
      tasks = get_tasks( )
    if tasks:
      for task in tasks:
        print task
      sys.exit(0)
    else:
      sys.exit(1)
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
  sys.exit(1)

def view_tasks( keywords ):
  for task in find_tasks( keywords ):
    with open( task, 'r' ) as f:
      print f.read()
  sys.exit(0)

def search_file( keywords ):
  return ''

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

def edit_task( keywords ):
  try:
    task = find_tasks( keywords )[0];
    print task
    command=EDITOR+" "+task
    os.system( command )
    sys.exit(0)
  except Exception, e:
    print "no matching file to edit"
    sys.exit(1)
    pass

def create_will( params ):
  path=' '.join(params)
  if path == '':
    path = os.getcwd()+'/.will'
  else:
    path = path+'/.will'
  if not os.path.exists( path ):
    os.makedirs( path )
    print path
    return 0
  else:
    return 1

def create_task( params ):
  subject=' '.join( params )

  task_file=str(find_will()+'/'+str(random.randint( 1000, 9999 )))+".md"

  with open( task_file, 'w+' ) as f:
    f.write(subject+'\n')
    f.write( re.sub('.', '=', subject)+'\n')
    f.write( 'description of the task here\n' )
    f.write( datetime.datetime.now().strftime('%d %b %Y') )

  command=EDITOR+" "+task_file
  os.system( command )
  #subprocess.Popen( command )

def find_tasks( keywords=[] ):
  # flexibly searches for tasks that contain either the keywords in or
  # or partially match the ID.
  output = []
  for task in get_tasks():
    for keyword in keywords:
      if keyword in task:
        output.append( task )
        break
      with open( task, 'r' ) as task_file:
        if keyword in task_file.read():
          output.append( task )
          break
  return output

  #if type(substr) == 'string':
  #  return
  #else if type(substr == 'int'):
  #  return
  #check files for regex matches

def find_will( ):
  path = os.path.dirname( __file__ )
  while True:
    will = path + '/.will'
    if os.path.isdir( will ):
      return path+'/.will'
    path = os.path.abspath( os.path.join( path, os.pardir ) )

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

    task_identif = get_task_id          ( task )
    task_subject = get_task_subject     ( lines )
    task_categor = get_task_categories  ( lines )
    task_descrip = get_task_description ( lines )
    task_duratio = get_task_duration    ( lines )

    #print task_identif+'\t'+task_subject+'\t'+task_categor+'\t'+task_descrip+'\t'+task_duratio
    rows.append([ task_identif, task_subject, task_categor, task_descrip, task_duratio]);
  rows.insert(0, [ 'TASK', 'SUBJECT', 'CATEGORY', 'DESCRIPTION', 'DEADLINE' ] )
  collumnize( rows, [4, 24, 12, 32, 15] ) #including the 2 spaces after each collumn
  sys.exit(0);

def get_task_id( file_name ):
  return file_name.split('/')[-1][0:4]

def collumnize( rows, widths ):
  def length( string, length):
    string_length = len ( str ( string ) )
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
  line = lines[-1]
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
  lines = []
  with open( task, 'r' ) as task_file:
    for line in task_file.read().split('\n'):
      if not line == '':
        lines.append( line )
  return lines

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


