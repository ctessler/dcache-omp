#!/bin/bash

function usage {
	src=`basename $0`
	cat <<-EOF
	Usage: ${src} [dir] > list.txt

	[dir] the directory to search for CSV files, defaults to .

	Finds the CSV files within this directory
EOF
}

args=`getopt -o h -l help -- "$@"`
eval set -- ${args}

while true
do
	case "$1" in
	-h|--help)
		  usage;
		  shift
		  exit -1
		  ;;
	--)
	   shift
	   break;
	esac
done
argdir="$1"

if [[ -z $argdir ]] ; then
	searchdir="."
else
	searchdir=$argdir
fi


find $searchdir -name "*.csv"
	   

		  
