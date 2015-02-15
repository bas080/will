#!/usr/bin/env python
# needed to simplify remove features that are cluttery

import sys
import shutil
import os
import random
import time
import string
import filecmp
import time
import pprint
from ConfigParser import SafeConfigParser

EDITOR=os.getenv('EDITOR')

def is_valid_dir( path ):
  return os.path.isdir( path )

class Color:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'

class Will:
  # a task is basicly the file name of the task. Not the path. To get the path
  # of a task you would have to use get_task_path

  def __init__( self, path = '' ):
    # check if first arg is an option if not then check if  directory if not
    # then if neither then show usage.
    # # #
    self.path = self.find_will_path( path )
    self.statusses = [ 'Inactive', 'Ready', 'Assigned', 'Terminated', 'Expired', 'Forwarded', 'Finished', 'Failed', 'Completed', 'Revived' ]

  def get_config( self, key, default ):
    try:
      self.configurations = self.configurations
    except Exception, e:
      self.configurations = SafeConfigParser()
      self.configurations.read(self.path+'/.config/config')
      pass
    try:
      return self.configurations.get( 'configurations', key ).replace( '\\n', '\n' ).replace( '\\t', '\t' )
    except Exception, e:
      return default

  def create_config( self, path ):
    os.makedirs( path )
    conf_path = path + 'config'
    with open( conf_path, 'w+' ) as f:
      f.write( '[configurations]' )

  def config( self, args ):
    conf_dir = self.path + '/config/'
    conf_path = conf_dir+'config'
    if not os.path.exists( conf_path ):
      self.create_config( conf_dir )
    command = EDITOR+" "+conf_path
    os.system( command )

  def __getitem__( self, option ):
    self.options = {
      'ac'          : self.autocomplete,
      'assign'      : self.assign,
      'clean'       : self.clean,
      'complete'    : self.complete,
      'config'      : self.config,
      'create'      : self.create,
      'edit'        : self.edit,
      'grep'        : self.grep,
      'history'     : self.history,
      'init'        : self.init,
      'ls'          : self.ls,
      'path'        : self.get_path,
      'quick'       : self.quick_create,
      'ready'       : self.ready,
      'revive'      : self.revive,
      'rm'          : self.rm,
      'set'         : self.set_status,
      'status'      : self.status,
      'tag'         : self.tag,
      'view'        : self.view,
    }
    if option in self.options.keys():
      return self.options[option]
    else:
      return self.usage

  def autocomplete( self, option ):
    option = option[0]
    options = {
      'complete'   : self._complete,
      'edit'       : self._edit,
      'assign'     : self._assign,
      'options'    : self._options,
      'ready'      : self._ready,
      'revive'     : self._revive,
      'set'        : self._statusses,
      'rm'         : self._rm,
      'statusses'  : self._statusses,
      'tasks'      : self._tasks,
    }

    if option in options.keys():
      print ' '.join( options[ option ]( args ) )

  def _assign( self, args ):
    return self.get_tasks_with_status( [ 'Ready' ] )

  def _edit( self, args ):
    return self.get_tasks()

  def _rm( self, args ):
    return self.get_tasks()

  def ready( self, args ):
    for task in args:
      self.set_task_status( task, "Ready" )

  def _ready( self, args ):
    return self.get_tasks_with_status( ['Inactive', 'Assigned' ] )

  def complete( self, args ):
    for task in args:
      self.set_task_status( task, "Completed" )

  def _complete( self, args ):
    return self.get_tasks_with_status( [ 'Inactive', 'Terminated', 'Expired', 'Forwarded', 'Finished', 'Failed' ] )

  def revive( self, args ):
    # shows the recently completed tasks
    for task in args:
      self.set_task_status( task, 'Inactive' )

  def _revive( self, args ):
     return self.get_tasks_with_status( ['Completed'] )

  def assign( self, args ):
    for task in args[0:-1]:
      self.set_task_status( task, "Assigned" )

  def _statusses( self, args ):
    return self.statusses

  def set_status( self, args ):
    status = args [0]
    if not self.is_status( status ):
      # TODO return an error
      print( 'not valid status: '+status)
      return False
    tasks = args[1:]
    for task in tasks:
      self.set_task_status( task, status )

  def rm( self, args ):
    tasks = args
    for task in tasks:
      self.remove_task( task )
      return

  def remove_task( self, task ):
    task_path = self.get_task_path( task )
    if self.task_exists( task ):
      self.backup_task( task )
      os.remove ( task_path )
      print 'removed ' + task
      return True
    else:
      return False

  def _options( self, args ):
    return self.options.keys()

  def _tasks( self, args ):
    return self.get_tasks()

  def tag( self, args ):
    tasks = args[1:]
    tag = args[0]
    for task in tasks:
      if self.tag_task( task, tag ):
        print 'tagged '+ task + ' with ' + tag
      else:
        sys.stderr.write('unable to tag ' + task + ' as ' + tag + '\n' )

  def get_path(self, args ):
    print self.path

  def quick_create( self, args ):
    string = ' '.join( args )
    split = string.split('.')
    title = split[0]
    if len( split ) > 1:
      description = split[1]
    else:
      description = ''
    task_dict = {
      'title'       : title,
      'tags'        : ['quick'],
      'description' : description,
      'status'      : 'Inactive'
    }
    task = self.create_task( task_dict )
    self.view_task( task )

  def tag_task( self, task, tag ):
    try:
      lines = self.get_task_lines( task )
      lines.insert( 1, tag )
      contents = '\n'.join(lines)
      if self.task_exists( task ):
        self.write_task_to_file( task,  contents )
        return True
      return False
    except Exception, e:
      return False

  def status( self, args ):
    if len( args ) > 0:
      self.view_statusses( args )
    else:
      self.view_statusses( self.statusses )

  def set_task_status( self, task, status ):
    lines = self.get_task_lines( task )
    lines[-1] = status
    content = '\n'.join( lines )
    if self.write_task_to_file( task, content ):
      self.log( status + ' ' + task )
      return True
    else:
      return False

  def log( self, string ):
    #todo write to history log
    print string

  def is_status( self, status ):
    if status in self.statusses:
      return True
    else:
      return False

  def parse_tasks( self, tasks ):
    output = []
    for task in tasks:
      output.append( self.parse_task( task ) )
    return output

  def view_statusses( self, statusses ):
    statusses_template = 'In directory {path}\n  (use "will set <status> <task...>" to change task(s) as status)\n{statusses}'
    statusses_template = self.get_config( 'template_statusses', statusses_template )
    status_template = Color.bold + '\n  {status}: {amount}\n{tasks}\n' + Color.end
    status_template = self.get_config( 'template_status', status_template )
    task_template = Color.end + Color.red + '\n\t{id}\t' + Color.end + '{title}'
    task_template = self.get_config( 'template_task', task_template )

    statusses_string = ''
    for status in statusses:
      tasks = self.get_tasks_with_status( status )
      tasks_string = ''
      if not tasks:
        continue
      task_dicts = self.parse_tasks( tasks )
      for task in tasks:
        task_dict = self.parse_task( task )
        tasks_string = tasks_string + task_template.format( **task_dict )
      statusses_string = statusses_string + status_template.format(**{
        'amount' : len(tasks),
        'status' : status,
        'tasks'  : tasks_string
      })
    print statusses_template.format(**{
      'statusses' : statusses_string,
      'path'      : self.path,
    })
    return True
    #use a template better TODO
    template = '''In directory {path}\nIncompleted tasks:\n  (use "will set <status> <task...>" to mark task as done)\n'''
    tasks_done = []
    status_dict = { 'path' : self.path, }
    total = 1
    for index, task in enumerate( self.get_tasks() ):
      total = index
      task_dict = self.parse_task( task )
      if task_dict['status'] == 'Completed':
        tasks_done.append( task_dict )
        continue
      template = template+ '\n\t'+Color.red + task + Color.end + '\t' + task_dict['status'] + '\t' + ' ' + Color.bold + task_dict['title'] + Color.end
    template = template + '\n\n' + 'Completed tasks:\n  (use "will clean" to move long completed to history)' + '\n'
    for task_dict in tasks_done:
      template = template+ '\n\t'+Color.purple + task_dict['id'] + Color.end + '\t' + task_dict['status'] + '\t' + ' ' + task_dict['title']
    template = template+'\n\nCompleted '+str( len( tasks_done) ) + ' of ' + str( total +1 )
    contents = template.format( **status_dict )
    #template = 
    #template = 'In directory {path}\nIncompleted tasks:\n  (use "will set <status> <task...>" to mark task as done)\n'
    print contents
  
  def get_tasks_with_status( self, statusses ):
    if type(statusses) == str:
      statusses = [ statusses ]
    tasks = self.get_tasks()
    output = []
    for task in tasks:
      task_dict = self.parse_task( task )
      if task_dict['status'] in statusses:
        output.append( task )
    return output

  def grep( self, args ):
    # searches the file contents and prints the results in a specified way.
    # TODO make it regex not just a word
    template = '{task} ' #TODO
    word = args[0]
    for task in  self.get_tasks():
      lines = self.get_task_lines( task )
      fulls = [] # full lines
      for index, line in enumerate( lines ):
        if not line.strip() == '':
          fulls.append( str( index ) + ' ' + line )
        else:
          continue
        if word in line:
          fulls[-1] = Color.green + fulls[-1] + Color.end
          task_dict = self.parse_task( task )
          print( Color.red + task + ': ' + task_dict['title'] + Color.end )
          trailing = 4
          line_min = max( 0, len( fulls ) - trailing )
          print '\n'.join( fulls[line_min:] )
          break

  def create( self, args ):
    title = ' '.join( args )
    task = self.create_task({
      'title'       : title,
      'tags'        : [],
      'description' : '',
      'status'      : 'Inactive'
    })
    self.edit_task( task )

  def is_task( self, args ): #TODO
    return True

  def edit( self, args ):
    for task in args:
      if self.is_task( task ):
        self.edit_task( task )

  def edit_task( self, task ):
    task_path = self.get_task_path( task )
    print task_path
    command = EDITOR+" "+task_path
    os.system( command )
    #termcolor.cprint( 'edited: ' + task + '\n', color='red', attrs=['bold'] )
    self.view_task( task )
    sys.exit(0)

  def is_edited( task ):
    #TODO
    return True

  def view( self, args ):
    tasks = args
    for task in tasks:
      self.view_task( task )
    return True

  def ls( self, args ):
    tasks = self.get_tasks()
    for task in tasks:
      if not task:
        break
      task_dict = self.parse_task( task )
      print self.get_task_path( task )

  def init( self, args ):
    if self.create_will_dir():
      print( 'created .will in: '+self.path )
    else:
      sys.stderr.write('already initiated .will in '+self.path+'\n')

  def usage( self, args ):
    pass

  def create_will_dir( self ):
    path = self.get_will_path( )
    hist_path = self.get_history_path( )
    if not os.path.exists( path ):
      os.makedirs( path )
      os.makedirs( hist_path )
      return path
    else:
      return False

  def get_will_path( self ):
    return self.path+'/.will'

  def find_will_path( self, path='' ):
    # gives a string of the nearest .will directory that can be either in the
    # current directory or in its parent directories
    # # #
    if path == '':
      path = os.getcwd()
    while True:
      will = path + '/.will'
      if os.path.isdir( will ):
        return will
      path = os.path.abspath( os.path.join( path, os.pardir))

  def get_tasks( self ):
    tasks = [];
    for (dirpath, dirnames, filenames) in os.walk( self.path ):
      tasks = filenames
      break
    for index, task in enumerate(tasks):
      task_dict = self.parse_task( task )
      tasks[index] =  task
    return tasks;

  def view_task( self,  task ):
    #outputs to human readable format
    task_dict = self.parse_task( task )
    template = Color.red + '{id}' + Color.end + Color.bold + ' {title}' + Color.end + '{description}\n' + Color.cyan + '{status}\t' + Color.end + '{tags}'
    template = self.get_config( 'view_template', template )
    task_dict['tags'] = ' '.join(task_dict['tags'] )
    print template.format( **task_dict )

  def create_task( self, task_dict ):
    task = self.get_new_task()
    path = self.get_task_path( task )
    task_dict['tags'] = '\n'.join( task_dict['tags'] + self.get_config( 'tags', '').split(', ') )
    template = '{title}\n{tags}\n{description}\n{status}'
    template = self.get_config( 'template_file', template )
    contents = template.format( **task_dict )
    self.write_task_to_file( task, contents )
    return task

  def clean( self, args ):
    tasks = self.get_tasks()
    for task in tasks:
      task_dict = self.parse_task( task )
      if not task_dict['status'] == 'Completed':
        continue
      task_path = self.get_task_path( task )
      #week = 604800
      #week = 10
      #unix = time.time()
      #mtime = os.path.getmtime( task_path )
      #diff = unix - mtime
      #if diff > week:
      self.remove_task( task )

  def history( self, args ):
    try:
      if type( args[0] ) == int:
        print self.get_history( args[0] )
        return True
    except Exception, e:
      print  self.get_history()
      pass

  def get_history( self, amount=10 ):
    lines = self.get_history_log_lines()
    return lines[0:amount]

  def backup_task( self, task ):
    #TODO when changes are made to file
    unix = int( time.time() )
    name = str( unix ) + '_' + task
    task_path = self.get_task_path( task )
    back_path = self.get_history_path( )
    if not os.path.isdir( back_path ):
      os.makedirs( back_path )
    shutil.copy( task_path, back_path+name )

  def get_history_log_path( self, past=10 ):
    return self.get_history_path()+'log'

  def get_history_path( self ):
    return self.path+'/.history/'

  def task_exists( self, task ):
    task_path = self.get_task_path( task )
    return os.path.isfile( task_path )

  def write_task_to_file( self, task, contents ):
    # check if file changes make the file different. If not then do not save and
    # log the changes to the log
    # # #
    task_file = self.get_task_path( task )
    comp_file = task_file+'~'
    is_similar = False

    if self.task_exists( task ):
      with open( comp_file, 'w+' ) as f:
        f.write( contents )
      is_similar = filecmp.cmp( task_file, task_file+'~' )
      os.remove( task_file+'~' )

    if is_similar:
      #TODO log command to both log and print
      return False

    with open( task_file, 'w+' ) as f:
      f.write( contents )

    self.backup_task( task )
    return True

  def get_new_task( self ):
    tasks = self.get_tasks()
    task = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in xrange(4)])
    while task in tasks:
      task = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in xrange(4)])
    return task

  def get_task_path( self,  task ):
    return self.path+'/'+task

  def get_task_lines( self, task ):
    task_path = self.get_task_path( task )
    return self.get_file_lines( task_path )

  def get_history_log_lines( self ):
    log_file = self.get_history_log_path()
    return self.get_file_lines( log_file )

  def get_file_lines( self, file_path ):
    try:
      with open( file_path, 'r' ) as f:
        return f.read().strip().split('\n')
    except Exception, e:
      sys.stderr.write('could not read: '+file_path+'\n')
      return []

  def parse_task( self, task ):
    # consider making a TaskParser class
    lines = self.get_task_lines( task )
    if not lines:
      return {
        'title'       : "",
        'status'      : "",
        'tags'        : "",
        'description' : "",
        'id'          : str( task )
      }

    def get_title():
      return lines[0]

    def get_status():
      return lines[-1]

    def get_tags():
      tags = []
      for line in lines[1:]:
        if line.strip() == '':
          break
        else:
          tags.append( line )
      return tags

    def get_description():
      first_line = 0
      for index, line in enumerate(lines):
        if line.strip() == '':
          first_line = index
          break
      return '\n'.join( lines[first_line:-2] )

    return {
      'title'       : get_title(),
      'status'      : get_status(),
      'tags'        : get_tags(),
      'description' : get_description(),
      'id'          : task
    }

args = sys.argv

length = len( args )

if length == 1:
  args.append( 'status' )
  will = Will( args[1] )
else:
  first_char = args[1][0]
  if first_char in string.uppercase:
    args.insert( 1, 'create' )
  will = Will( args[1] )

if is_valid_dir( args[1] ):
  args = args[1:]

option = args[1]
params = args[2:]
sys.exit( will[option]( params ) )
