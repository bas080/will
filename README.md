Will Do
=======

Do you have the will to do your todos? Now with "will" you can easily manage
your todo tasks using the command line. There is both a version written in bash
and another written in python. They both have similar functions and can be run
independent of eachother.

*Some features might differ between the two. I am considering continueing this
project using python only*

Features
========
- Every directory can have a todo list (.will directory)
- Tasks have properties including categories, description and due-date.
- Tasks are simple .md files that only require a certain layout.
- List, view, edit and remove tasks quickly.
- Tasks can be exported to json.

Setup
=====
Simply download the script and add it to one of your bin folders.

*Make sure you have your EDITOR variable set in environment. This can be easily done by adding
export EDITOR=vim to your .bashrc*

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
found while looking in the current folder and then with every search itteration
going in the parent folder.

Thus if there is no .will folder in the current folder but there is one in it's
parent. Then that one will be used.

This opens your default editor with the subject in it already. See chapter named
tasks to find out what a task file can and should contain.

*Remember to start typing with a capital letter. This avoids conflicts with the
options.*

**list the tasks**
```bash
will ls
  #or
will list
```
This will output the following
```bash
id     subject                categories   description       deadline
256    Make screencast jUnix  development  Make a screencas  19 jan 2015
18839  Fix error #14243       bug,urgent   Irritating bug o  19 jan 2015
```
This example contains two tasks that are listed.

**find tasks**
```bash
will find bug
```
This returns the files of the tasks that contain css in the title and in the content.
```bash
/home/boi/.will/18839.md
```

**edit a task**
```bash
will edit 1843
  #or
will edit refactor code project alpha
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
Remeber that when removing a task it is gone for good. In case you want to set
the status of a task to completed or something similar, consider using categories instead to
set the category of a task to completed or done. That way you do not loose
valuable information regarding the tasks.

**export the tasks**
```bash
will export
```
*An example of the output looks like this.*
```bash
TODO
```

Tasks
=====
A task file format is dead simple here it goes.
```markdown
Title	category_one	category_two
===
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
always have the === seperation which at the same time defines the header.

The bottom line is used to define the deu date. In the future I might also add a
start and or creation date. They will also be spaced using tabs.

Roadmap
=======
- Add dates of category changes to the bottom of the file this way you know when
  the state of a "ticket has changed.

Contribute
==========
Please leave a comment if you know of improvements or even better, send me a
pull request. If you really like the project then consider starring or following
it.

Links
=====
<a href="https://github.com/bas080/will">GitHub</a>
