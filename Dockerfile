FROM python:3.12-alpine

# 时区: 默认北京时间, 部署时可用 TZ 环境变量覆盖 (如 Asia/Tokyo)
# Alpine 换用阿里云 apk 源(自行换成腾讯/华为/清华); 海外部署可删这两行
RUN sed -i 's|dl-cdn.alpinelinux.org|mirrors.aliyun.com/alpine|g' /etc/apk/repositories \
 && apk add --no-cache tzdata \
 && rm -rf /var/cache/apk/*
ENV TZ=Asia/Shanghai

WORKDIR /app

COPY requirements.txt .
# 清华 PyPI 镜像, 国内网络下容器内访问 PyPI 更好; 海外部署可删掉 -i 参数
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY app ./app

ENV DATA_DIR=/data
VOLUME /data
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]