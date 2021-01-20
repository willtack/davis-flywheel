#!/bin/bash
#
# Loop fw-heudiconv from command line over a list of subjects (line-separated text file)
# Specify -x to override dry_run
#
#	Will Tackett
# October 10th, 2019
#

cmd=$(basename "$0")
syntax="$cmd [-x]{p Project}{-h heuristic} [Subjects]"

error_exit()
{
	echo "$@" 1>&2
	echo "$syntax" 1>&2
	exit 1
}

while getopts “xp:h:” opt; do
  case $opt in
    x ) execute=true ;;
    p ) project=$OPTARG ;;
    h ) heuristic=$OPTARG ;;
   \? ) error_exit "Invalid option: $OPTARG";;
    : ) error_exit "Invalid option: $OPTARG requires an argument";;
  esac
done

shift $((OPTIND -1))

if [ -z $project ]; then error_exit "You must specify a project"; fi
if [ -z $heuristic ]; then error_exit "You must provide a heuristic"; fi

logFile=fwheudiconv-logs-$(date +"%m-%d-%y").log
touch "${logFile}"
if [[ ${execute} == true ]]; then
	 echo "Curating ${project} with the following heuristic: ${heuristic}"
	 cat "$@" | while read sub; do
		 fw-heudiconv-curate --project ${project} --heuristic ${heuristic} --subject "$sub" --verbose
	 done 2>&1 | tee -a ${logFile}
else
	 echo "Starting a dry run for ${project} with the following heuristic: ${heuristic}"
   cat "$@" | while read sub; do
		 fw-heudiconv-curate --project ${project} --heuristic ${heuristic} --subject "$sub" --verbose --dry-run
   done 2>&1 | tee -a ${logFile}
fi

#fw upload davis/${project} "${logFile}"

exit 0
