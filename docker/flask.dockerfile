# 使用python:3.6.8基础镜像
FROM python:3.6.8

# 设置工作目录
WORKDIR /app

# 创建数据目录
RUN mkdir -p /app/data

# 复制requirements.txt并安装所需的Python包
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 公开容器的端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 运行Flask应用
CMD ["flask", "run", "--host=0.0.0.0"]