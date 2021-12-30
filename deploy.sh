# 打包 liuli_schedule
docker build --no-cache=true -t liuliio/schedule:v0.1.2 -f schdule.Dockerfile .
# 打包使用缓存
docker build --no-cache=false -t liuliio/schedule:v0.1.2 -f schdule.Dockerfile .
# 运行
docker run -d -it --restart=always -v $PWD/pro.env:/data/code/pro.env --name liuli_schedule liuliio/schedule:v0.1.2
# 上传
docker push liuliio/schedule:v0.1.2

# 打包 liuli_api
docker build --no-cache=true -t liuliio/api:v0.1.0 -f api.Dockerfile .
# 打包使用缓存
docker build --no-cache=false -t liuliio/api:v0.1.0 -f api.Dockerfile .
# 运行
docker run -d -it --restart=always -v $PWD/pro.env:/data/code/pro.env --name liuli_api liuliio/api:v0.1.0
# 上传
docker push liuliio/api:v0.1.0