docker run --rm \
    -p 5000:5000 \
    -v $PWD/webapp:/app \
    -v /root/notebooks/rec/IMDBPoster:/app/data \
    registry-vpc.cn-hangzhou.aliyuncs.com/hz-ns1/flask:latest