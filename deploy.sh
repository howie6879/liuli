# 打包 2c_schedule
docker build --no-cache=true -t howie6879/2c:schedule_v0.1.2 -f schdule.Dockerfile .
# 打包使用缓存
docker build --no-cache=false -t howie6879/2c:schedule_v0.1.2 -f schdule.Dockerfile .
# 运行
docker run -d -it --restart=always -v $PWD/pro.env:/data/code/pro.env --name 2c_schedule howie6879/2c:schedule_v0.1.2