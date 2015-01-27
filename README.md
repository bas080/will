Will Do
=======

Do you have the will to do your todos? Now with "will" you can easily manage
your todo tasks using the command line and storing tasks in a human readable
markdown format combined with Tabular Format.

Features
========
- Every directory can have a todo list (.will directory)
- Tasks have properties including categories, description and due-date.
- Tasks are simple .md files that only require a certain layout.
- List, view, edit and remove tasks quickly.
- Tasks can be exported to JSON. (WIP)

Setup
=====

Add the following alias to your .~/bashrc
```bash
export EDITOR=nano

alias will='python ~/path/to/will.py'
```

*You can of course use your preferred editor. You can also install will by adding
it to a bin-like folder. The above is just an example.*

Usage
=====

This is a command line tool. The command is "will". Here are some examples on
how to use the "will".

**create a todo list in current directory**
```bash
will init
```
Creates a .will folder in the current directory. Another option would be to
give a path.
```bash
will init ~/development
```
It will now create a file in the development folder. Absolute paths are also
allowed.

**create a new task**
```bash
will Start typing my task title
```
Important to know is that the .will folder that will be used is the first one
found while looking in the current folder and then with every search iteration
going in the parent folder.

Thus if there is no .will folder in the current folder but there is one in it's
parent. Then that one will be used.

This opens your default editor with the subject in it already. See chapter named
tasks to find out what a task file can and should contain.

*Remember to start typing with a capital letter. This is done to avoid conflicts with the
options.*

**list the tasks**
```bash
will
```

This will output the following

```bash
TASK  SUBJECT                   CATEGORY      DESCRIPTION                       DEADLINE         
9197  Add font icons to portof  ...           replace the folder file and chap  2w 4d 21h        
4955  Fix dammen board generat  Bug           The board generator is doing som  done             
7097  Learn Angular             Learn         The technologies industry uses.   Jan 21 2015      
4562  Nationalist               Development   data/scenarios/nationalist.js:    3w 2d 21h        
6439  Learn Git better          Learn         Make aliases from learned comman  3w 3d 21h        
2986  Will todo manager         Development   Keep the readme up to date with   -2d 2h           
4839  Dammen                    Development   - Ability to add a game. States   21h              
```

You can also list tasks that contain either the ID or certain keywords. It
searches case insensitively.

```bash
will ls dev
  #or
will list dev

TASK  SUBJECT                   CATEGORY      DESCRIPTION                       DEADLINE         
4562  Nationalist               Development   data/scenarios/nationalist.js:    3w 2d 21h        
2986  Will todo manager         Development   Keep the readme up to date with   -2d 2h           
4839  Dammen                    Development   - Ability to add a game. States   21h              
```

**view tasks**
```bash
will view 3826
```
show the file contents

**find tasks**
```bash
will find bug
```
This returns the files of the tasks that contain CSS in the title and in the content.
```bash
/home/oen/.will/18839.md
```

**edit a task**
```bash
will edit 1843
  #or
will edit re-factor code
```
Opens up the task with corresponding ID or the task that matches the keywords
the most in your favorite EDITOR. 

**remove task**
```bash
will rm 8372 3729 6234
  #or
will remove 5819
```
You cannot remove using keywords. This is done to avoid accidental removals.
Remember that when removing a task it is gone for good. In case you want to set
the status of a task to completed or something similar, consider using categories instead to
set the category of a task to completed or done. That way you do not loose
valuable information regarding the tasks.

**export the tasks**
*not yet implemented*
```bash
will export
```
*An example of the output looks like this.*
```bash
```

Tasks
=====
A task file format is dead simple here it goes.
```markdown
Title	category_one	category_two	category...
=====
This is a description
- That include markdown style bullets
- And it describes clearly what the
- task is about.
15 feb 2015
```
First line is the title and the categories. Notice the tabs between the title
and the categories. To define a category you have to use tabs and it has to be
on the first line.

The description should always start on the third line. The second line should
always have the === separation which at the same time defines the header.

The bottom line is used to define the due date. The format for now must be 15
feb 2015 for it to show time till and time since. In the future I might also add
a start of task date. Making it also more useful for planning activities.

Road map
=======
- log the changes made to the tasks and save it in a human readable format in
  the .will folder.
- Auto-completion functions for bash and Zsh shell.
- A way to easily get and set the status of the task. Statuses include:
  Inactive Ready Assigned Terminated Expired Forwarded Finished Failed Completed

Contribute
==========
Please leave a comment if you know of improvements or even better, send me a
pull request. If you really like the project then consider starring or following
it.

Links
=====
<a href="https://github.com/bas080/will">GitHub</a>
