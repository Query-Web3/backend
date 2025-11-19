# 第一阶段：构建阶段
FROM golang:1.24-alpine AS builder

# 设置工作目录
WORKDIR /app

ADD gql /app/gql
ADD model /app/model
ADD server /app/server
# ADD gql model server go.mod go.sum /app/
ADD go.mod go.sum /app/

# 下载依赖（使用代理加速国内下载）
RUN go mod download && go mod verify

# 构建 Go 应用
RUN go build -o backend ./server/server.go 

RUN ls

# 第二阶段：生成最终镜像
FROM alpine:3.19

# 创建非 root 用户（增强安全性）
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 设置工作目录
WORKDIR /app

# 从构建阶段复制编译好的二进制文件
COPY --from=builder /app/backend .

# 更改文件所有权为非 root 用户
RUN chown -R appuser:appgroup /app

# 切换到非 root 用户运行
USER appuser

# 暴露应用端口（根据实际应用端口修改）
EXPOSE 8080

# 启动应用
CMD ["./backend"]
