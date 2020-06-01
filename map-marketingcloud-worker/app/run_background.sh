TASK="background queue processor"
CMD="/usr/local/bin/python3.7 -m worker.work"
REDIRECT="/proc/1/fd/1 2> /proc/1/fd/2"
FULL_CMD="PYTHONPATH=/app ${CMD} > ${REDIRECT}"
INITIAL_SLEEP_MINUTES=2
LOOP_SLEEP_MINUTES=2

# PYTHONPATH=/app /usr/local/bin/python3.7 -m worker.work > /proc/1/fd/1 2> /proc/1/fd/2

echo "run_background.sh -- My container just woke up, I won't start processing until after ${INITIAL_SLEEP_MINUTES} minutes has passed"
eval "sleep ${INITIAL_SLEEP_MINUTES}m"

while :
do
  # loop infinitely
  if [ `ps -aux | grep "${CMD}" | grep -v "grep" | wc -l` -eq "0" ]
  then
    echo "(re)starting ${TASK}"
    # echo ${FULL_CMD}
    eval "${FULL_CMD}";
  fi
  eval "sleep ${LOOP_SLEEP_MINUTES}m"
done