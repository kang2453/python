PID=`ps -ef | grep python | grep main.py | awk '{ print $2}'`
if [ -n "$PID" ]; then
    kill -9  $PID
fi