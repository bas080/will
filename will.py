#!/usr/bin/env python
"""
Brief     Easily manage your tasks with the commandline
Created   Jan 20 2015
Version   0.1
Author    bas080
"""

import termcolor
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
    if opt[0].upper() == opt[0]:
      create_task( args[1:] )
      sys.exit(0)
  except Exception, e:
    opt = 'list'
  try:
    val = args[2:]
  except:
    val = []

  options = {
    'init'  : create_will,
    'ls'    : list_tasks,
    'list'  : list_tasks,
    'rm'    : remove_task,
    'remove': remove_task,
    'edit'  : edit_task,
    'view'  : view_tasks,
    'path'  : find_path,
    'paths' : find_paths,
    'export': export_tasks,
    'find'  : path_tasks,
    'help'  : usage,
  }
  try:
    options[opt]( val );
    sys.exit(0)
  except Exception, e:
    usage( options )
    sys.exit(1)
    pass

def usage( options ):
  keys = []
  for option in options:
    keys.append(option)
  print '''
NAME
	will - Create and manage user tasks using commandline by bas080@hotmail.com

SYNOPSIS
	will [ [[OPTIONS] [WORDS | TASKS] | ... ] | [TITLE] ] | ...

OPTIONS
	'''+' '.join(keys)+'''

DESCRIPTION
	Start typing the task TITLE with a capital letter to create a new task.
	Some OPTIONS do not require the use of WORDS or TASKS. TASKS are simply
	the name of the task's file without the .md extension.
	New tasks are added to the .will directory that is in the nearest parent
	folder.

EXAMPLES
	will init - create a todo list in current folder

	will New task - New task with "New task" as title. Capital letter required!

	will - list the tasks in a neat list

FORMAT
	folder to the specified file, and allowing the adding,removing and editing of
	the tasks within that file. The syntax of a todo file is a combination between
	markdown and Tabular Seperated Data (TSV).

DOCUMENTATION
	For more examples and more extensive explanation on will's functionaliaty
	visit this website.
	https://github.com/bas080/will#usage
	'''
  sys.exit(1)

def view_tasks( keywords ):
  total = 0
  if keywords:
    tasks = find_tasks( keywords )
  else:
    tasks = get_tasks()
  termcolor.cprint( 'viewing: ' + str( len(tasks) ) + ' task(s)' + '\n', color='red', attrs=['bold'] )
  for task in tasks:
    view_task( task )
  termcolor.cprint( find_will(), color='red', attrs=['bold'] )
  sys.exit(0)

def view_task( task ):
  lines = get_task_lines( task )
  termcolor.cprint( lines[0], color='cyan', attrs=['bold'] )
  termcolor.cprint( '\n'.join( lines[2:-1] ), color='white' )
  termcolor.cprint( lines[-1]+'\n', color='yellow', attrs=['bold'] )

def get_task_contents( task ):
  with open( task, 'r' ) as f:
    return f.read()

def remove_task( tasks ):
  termcolor.cprint( 'removing: ' + str( len(tasks)) + '\n', color='red', attrs=['bold'] )
  for task in tasks:
    task_file = find_will() + '/' + task + '.md'
    if os.path.exists( task_file ):
      view_task( task_file )
      os.remove ( task_file )
    else:
      termcolor.cprint( 'failed: '+task_file, color='yellow', attrs=['bold'] )

  sys.exit(0);

def edit_file( task ):
  command=EDITOR+" "+task
  os.system( command )
  termcolor.cprint( 'edited: ' + task + '\n', color='red', attrs=['bold'] )
  view_task( task )
  sys.exit(0)

def edit_task( keywords ):
  try:
    task = find_tasks( keywords )[0];
    edit_file( task )
    view_task( task )
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
    sys.exit(0)
  else:
    print 'error: already initiated'
    sys.exit(1)

def create_task( params ):
  subject=' '.join( params )
  task = str( random.randint( 1000, 9999 ) )
  task_file=str(find_will()+'/'+task)+".md"
  with open( task_file, 'w+' ) as f:
    f.write(subject+'\n')
    f.write( re.sub('.', '=', subject)+'\n')
    f.write( 'description\n' )
    f.write( datetime.datetime.now().strftime('%d %b %Y') )
  print task_file
  print task
  edit_file( task_file )
  view_task( task_file )
  print 'created: ' + task_file
  sys.exit(0)

def find_tasks( keywords=[] ):
  output = []
  for task in get_tasks():
    for keyword in keywords:
      if keyword in task:
        output.append( task )
        continue
      if keyword.lower() in get_task_contents( task ).lower():
        output.append( task )
  if output:
    return output
  else:
    return False

def path_tasks( keywords=[] ):
  if keywords:
    output =  find_tasks( keywords )
  else:
    output = get_tasks()
  if output:
    print '\n'.join( output )
    sys.exit(0)
  else:
    sys.exit(1)

def find_path( _path ):
  print find_will( _path )
  sys.exit(0)

def find_paths( args ):
  path = os.getcwd()
  for root, dirs, files in os.walk(path):
    for d in dirs:
      if d == '.will':
        print(os.path.join(root, d))
  return 0

def find_will( _path=False ):
  if _path:
    path = _path
  else:
    path = os.getcwd()
  while True:
    will = path + '/.will'
    if os.path.isdir( will ):
      return will
    path = os.path.abspath( os.path.join( path, os.pardir))

def get_tasks():
  tasks = [];
  path = find_will();
  for (dirpath, dirnames, filenames) in os.walk( path ):
    tasks = filenames;
    break
  for index, task in enumerate(tasks):
    tasks[index] = path+'/'+task
  return tasks;

def list_tasks( keywords ):
  rows = []
  if keywords:
    exit
    tasks = find_tasks( keywords )
  else:
    tasks = get_tasks()
  if not tasks:
    print 'error: no matching tasks found'
    return 0
  for task in tasks:
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
  rows.insert(0, [ 'task', 'subject', 'category', 'description', 'deadline' ] )
  collumnize( rows, [4, 24, 12, 32, 15] ) #including the 2 spaces after each collumn
  termcolor.cprint( '\n'+find_will(), color='red', attrs=['bold'] )
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
  for i, row in enumerate(rows):
    line = ''
    for index, field in enumerate(row):
      line = line + length( field, widths[index] ) + '  '
    if ( i == 0 ):
      termcolor.cprint( line, color='cyan', attrs=['bold'] )
    else:
      print line

def get_task_title( lines ):
  return lines[0].split('\t')[0]

def get_task_date( lines ):
  return lines[-1]

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
  for line in get_task_contents( task ).split('\n'):
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

def export_tasks():
  return 0 #TODO

print main ( sys.argv );
