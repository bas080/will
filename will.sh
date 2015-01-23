#!/bin/bash

init(){
  local p=${@:2};
  case "$1" in
  'init')
    create_will $p;
    ;;
  'find')
    find_tasks $p;
    ;;
  'edit')
    edit_task $p;
    ;;
  'list')
    list_tasks $p;
    ;;
  'ls')
    list_tasks $p;
    ;;
  'view')
    view_task $p;
    ;;
  'remove')
    remove_task $p;
    ;;
  'rm')
    remove_task $p;
    ;;
  'export')
    export_tsv $p;
    ;;
  *)
    if [[ $p ]]; then
      #if a subject is given
      create_task $@;
      else
      #if no subject is given
      list_tasks $@;
    fi
    ;;
  esac
}

create_task(){
  local will_dir=$( get_will_dir $PWD );
    #returns an empty string if not .will file is found.
  if [[ $will_dir == '' ]]; then
    will_dir=$( create_will $PWD );
  fi
  local filename='';
  while true; do
    #keeps looping till it finds a unique task id
    local filename="$RANDOM.md";
    if [ ! -f  "$will_dir/$filename" ];then
      break;
    fi
  done
  local task_file=$will_dir/$filename;
  echo -e "$@	nocategory" > $task_file;
  echo -e "===" >> $task_file;
  echo -e "" >> $task_file;
  echo -e ` date "+%d %b %Y"` >> $task_file;
  $EDITOR $task_file;
  echo '---';
  echo $task_file;
  echo '   ';
  cat $task_file; #shows you what you saved
  echo '---';
}

view_task(){
  get_will_files $@ | while read file; do
    cat $file;
    echo;
  done
}

edit_task(){
  local task_file=$( find_tasks $@ | head -n 1 );
  $EDITOR $task_file;
  cat $task_file;
}

list_tasks(){
  #when no keyword is given it will list all
  #otherwise it shows only the tasks containing the keywords
  export_tsv $@ | column -s '	' -t -n;
}

remove_task(){
  local will_path=$( get_will_dir $PWD );
  for task in $@; do
    local task_file="$will_path/$task.md";
    if [[ -f $task_file ]]; then
      echo $task_file;
      echo
      cat $task_file;
      echo
      echo 'removed';
      rm $task_file;
    else
      echo Task with ID $task does not exist
    fi
  done
}

find_tasks(){
  get_will_files $@ | while read file; do
    echo $file;
  done
}

create_will(){
  if [[ $1 == '' ]]; then
    local path=$PWD;
  else
    local path="$1";
  fi
  local dir="$path/.will";
  if [ ! -d $dir ]; then
    echo $dir
  else
    exit 1;
  fi
  mkdir -p $dir;
}

get_will_files(){
  #takes either a task ID or keywords that are withing the file
  local will_dir=$(get_will_dir $PWD);
  if [[ "$@" == '' ]]; then
    find $will_dir -type f -name '*.md';
  elif [ "$@" -eq "$@" ] 2>/dev/null; then
    #if an ID is given
    local file="$will_dir/$@.md";
    if [ -f $file ]; then
      echo $file;
    fi
  elif [[ $@ ]]; then
    #return using keywords
    ls $will_dir | while read file; do
      for word in $@; do
        if grep -q $word $will_dir/$file; then
          echo $will_dir/$file;
        fi
      done
    done
  fi
}

get_will_dir(){
  #takes a path string returns a string containing the .todo file it's absolute
  #path. If the file is not found in current directory or all of it's ancestors.
  #It will return an empty string.
  local dir=$1;
  if [ ! -d $dir/.will ]; then
    if [ ! $dir == '/' ]; then
      get_will_dir $( dirname $dir );
    else
      return 1;
    fi
  else
    echo $dir/.will;
    return 0;
  fi
}

get_task_subject(){
  cat $1 | head -n 1 | cut -d '	' -f1;
}

get_task_categories(){
  cat $1 | head -n 1 | cut -d '	' -f2-;
}

get_task_description(){
  local task_file_len=$( cat $1 | wc -l );
  cat $1 | sed -n "3,$(( $task_file_len - 1 ))p" | cut -c1-16;
}

is_valid_date(){
  if ! date -d "$@" 2> /dev/null 1>/dev/null; then
    return 0;
  else
    return 1;
  fi
}

get_task_creation_date(){
  #TODO
  local date=cat $1 | tail -n 1;
  if is_valid_date $date; then
    echo $date;
  fi
}

get_task_deu_date(){
  local date=$(cat $1 | tail -n 1);
  if ! is_valid_date $date; then
    echo 'nvd';
    return;
  fi
  local unix=$( date -d "$date" +%s );
  local cure=$( date +%s );
  if [[ $unix -gt $cure ]]; then
    local dura=$(( $unix - $cure ));
    echo $( duration $dura );
  else
    local dura=$(( $cure - $unix ));
    echo "$( duration $dura ) ago";
  fi
}

export_tsv(){
  #when no keyword is given it will list all
  #otherwise it shows only the tasks containing the keywords
  local out=$(mktemp);
  echo -e "id\tsubject\tcategories\tdescription\tdeadline\n\n" >> $out;
  #echo -e "--\t-------\t----------\t-----------\t--------" >> $out;
  get_will_files $@ | while read file; do
    local sub=$(get_task_subject $file);
    local des=$(get_task_description $file | head -n 1);
    local cat=$(get_task_categories $file | tr '\t' ',');
    local deu=$(get_task_deu_date $file);
    local  id=$(basename $file | sed 's/\.md//g');
    echo -e "$id\t$sub\t$cat\t$des\t$deu" >> $out;
  done
  cat $out;
}

#helpers
duration() {
  local seconds=$1
  if ((seconds < 0)); then
    ((seconds *= -1))
  fi

  local times=(
  $((seconds / 60 / 60 / 24 / 365)) # years
  $((seconds / 60 / 60 / 24 / 30)) # months
  $((seconds / 60 / 60 / 24))    # days
  $((seconds / 60 / 60))      # hours
  $((seconds / 60))         # minutes
  $((seconds))           # seconds
  )
  local names=(year month day hour minute second)

  local i j
  for ((i = 0; i < ${#names[@]}; i++)); do
    if ((${times[$i]} > 1)); then
      echo "${times[$i]} ${names[$i]}s"
      return
    elif ((${times[$i]} == 1)); then
      echo "${times[$i]} ${names[$i]}"
      return
    fi
  done
  echo '0 seconds'
}

init $@;
exit 0;