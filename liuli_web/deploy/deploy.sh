# Web项目镜像构建
docker buildx build --no-cache=false --platform linux/amd64 -t liuliio/web-amd64:v0.1.0 -f Dockerfile .
docker buildx build --no-cache=false --platform linux/arm64 -t liuliio/web-arm64:v0.1.0 -f Dockerfile .
docker buildx build --no-cache=false --platform linux/arm/v7 -t liuliio/web-armv7:v0.1.0 -f Dockerfile .
docker buildx build --no-cache=false --platform linux/arm/v8 -t liuliio/web-armv8:v0.1.0 -f Dockerfile .

docker push liuliio/web-amd64:v0.1.0
docker push liuliio/web-armv7:v0.1.0
docker push liuliio/web-armv8:v0.1.0
docker push liuliio/web-arm64:v0.1.0

docker manifest rm liuliio/web:v0.1.0
docker manifest create liuliio/web:v0.1.0 liuliio/web-amd64:v0.1.0 liuliio/web-armv7:v0.1.0 liuliio/web-armv8:v0.1.0 liuliio/web-arm64:v0.1.0
docker manifest push liuliio/web:v0.1.0

docker run -p 8080:80 -e LL_API=http://liuli_api:8765 liuliio/web:v0.1.0