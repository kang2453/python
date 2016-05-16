PID=`ps -ef | grep python | grep main.py | awk '{ print $2}'`
if [ -z "$PID" ]; then
    cd /data/python/PerformanceTest
    echo "Performance Test is not Execite...." >> log/logger.log
    sh start.sh  & > /dev/null
fi
