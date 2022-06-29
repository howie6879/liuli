# Web项目镜像构建
docker buildx build --no-cache=false --platform linux/amd64 -t docker.zfty.work/brandark/brandark-web:v0.1.0-dev -f Dockerfile .
docker build --no-cache=false -t docker.zfty.work/brandark/brandark-web:v0.1.0-dev -f Dockerfile .

docker run -p 8080:80 -e BA_API=http://192.168.1.16:18432 docker.zfty.work/brandark/brandark-web:v0.1.0-dev