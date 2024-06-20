docker run -it --rm \
    -p 5000:5000 \
    -v $PWD/webapp:/app \
    -v /root/notebooks/rec/IMDBPoster/poster:/app/static/images \
    -v /root/notebooks/rec/ml-1m:/app/data/db \
    -v /root/notebooks/rec/model:/app/model \
    registry-vpc.cn-hangzhou.aliyuncs.com/hz-ns1/flask:latest