# 项目概述

本项目为南开大学《软件测试与维护》课程大作业，基于 Google 提供的 Online-Boutique 微服务示例系统，完成从环境部署到数据验证的全链路测试实践。通过混沌工程工具注入故障，结合监控与测试工具实现微服务系统的稳定性评估与异常检测。

## 技术栈

* **微服务框架**：Online-Boutique（Google 开源微服务示例系统）
* **混沌工程工具**：ChaosMesh（故障注入）
* **监控系统**：Prometheus + Grafana（性能指标采集与可视化）
* **自动化测试工具**：Selenium（功能测试）、JMeter（性能测试）
* **异常检测算法**：GDN（Graph Deviation Network，基于图神经网络）

## 环境部署

1. ### 微服务系统部署

   ```
   # 克隆项目
   git clone --depth 1 --branch v0 https://github.com/GoogleCloudPlatform/microservices-demo.git
   cd microservices-demo/

   # 创建 minikube 集群（Docker 驱动，4核6GB内存）
   minikube start --driver=docker --cpus=4 --memory=6g

   # 更新集群上下文
   minikube update-context
   minikube start

   # 部署微服务
   kubectl apply -f ./release/kubernetes-manifests.yaml

   # 查看微服务状态
   kubectl get svc
   kubectl get pods

   # 启动前端服务
   minikube service frontend-external
   ```
2. ### ChaosMesh故障注入部署

   ```
   # 添加 ChaosMesh Helm 仓库
   helm repo add chaos-mesh https://charts.chaos-mesh.org

   # 安装 ChaosMesh
   helm install chaos-mesh chaos-mesh/chaos-mesh --namespace chaos-testing --create-namespace

   # 创建故障注入实验（示例：购物车服务高延迟）
   kubectl apply -f chaos-experiment1.yaml
   kubectl apply -f chaos-experiment2.yaml

   # 访问 ChaosMesh 仪表盘
   kubectl port-forward -n chaos-testing svc/chaos-dashboard 2333:2333
   ```
3. ### Prometheus + Grafana 监控部署

   ```
   # 部署监控资源（需自行编写监控配置文件）
   kubectl create -f ./deploy/kubernetes/manifests-monitoring

   # 查看监控服务
   kubectl get svc -n monitoring

   # 获取访问地址
   minikube service prometheus -n monitoring --url
   minikube service grafana -n monitoring --url

   # Grafana 配置
   1. 登录（默认用户名/密码：admin/admin）
   2. 添加 Prometheus 数据源
   3. 导入可视化模板（示例 ID：12345）
   ```

## 测试流程

1. ### Selenium功能测试

   #### 测试场景


   * 场景 1：正常购买流程（点击商品→下单）
   * 场景 2：多商品购买流程
   * 场景 3：重新购买流程（清空购物车→重新选择）
   * 场景 4：货币转换功能（切换日元单位）
   * 场景 5：购物车状态同步测试
   * 场景 6：推荐系统功能测试（YouMayAlsoLike）

   ### 执行流程

   1. 使用 Selenium 插件录制测试脚本
   2. 导出为 Python 脚本并封装为类
   3. 使用 time 库记录关键指标（首页加载时间、交互响应时间、总执行时间）
   4. 在 Edge/Chrome/Firefox 浏览器中运行测试
2. ### JMeter性能测试

   #### 测试场景


   * **突发高并发**：1 秒内启动 20 个用户
   * **渐进式负载**：120 秒内逐步增加至 20 个用户

   #### 关键指标

   * 样本数、最小 / 最大 / 平均响应时间
   * 异常数、吞吐量（TPS）
     ```
     # JMeter 测试执行（GUI 模式）
     jmeter -q user.properties -n -t scenario_test.jmx -l result.jtl
     ```
3. ### 数据采集与预处理


   * 使用 Prometheus 采集 CPU / 内存 / 负载等时序数据
   * 时间戳对齐、缺失值填充（列均值）
   * Min-Max 归一化处理（缩放到 [0,1] 区间）
   * 划分训练集（仅正常数据）与测试集（含故障标注）
4. ### 数据采集与预处理


   * 复现论文《Graph Neural Network-Based Anomaly Detection in Multivariate Time Series》中的 GDN 模型
   * 使用 PyTorch 实现图结构学习与注意力机制
   * 训练参数：滑动窗口 5、隐藏层 64、学习轮数 30
   * 评估指标：F1 分数 0.9286、精确率 0.8571、召回率 0.9231

## 实验结果

    

### 1. Selenium 测试结果

| 浏览器  | 平均首页加载时间 (s) | 平均交互响应时间 (s) | 平均总执行时间 (s) |
| ------- | -------------------- | -------------------- | ------------------ |
| Edge    | 6.52                 | 1.10                 | 15.93              |
| Chrome  | 6.08                 | 1.16                 | 15.64              |
| Firefox | 6.37                 | 1.43                 | 18.78              |

 **结论** ：Chrome 浏览器在多数场景性能最优，Edge 在购物车和推荐功能中表现更佳，Firefox 兼容性最差。


### 2. JMeter 测试结果

#### 瞬时 20 用户并发

* **平均响应时间：98-105 ms**
* **异常率：场景 3（15%）、场景 4（5%）较高**
* **吞吐量：9.3-11.0 TPS**

#### 120 秒渐进负载

* **平均响应时间：42-67 ms**
* **异常率：场景 5（8.57%）最高**
* **吞吐量：15.2-23.9 TPS**

### 3. 模型复现结果

| 指标    | 值     |
| ------- | ------ |
| F1 分数 | 0.9286 |
| 精确率  | 0.8571 |
| 召回率  | 0.9231 |

## 团队分工

* **刘泽宇** ：微服务系统部署、Prometheus+Grafana 配置
* **谢其桐** ：数据采集与预处理
* **冯金涛** ：Selenium 与 JMeter 测试脚本开发
* **杨亚轩** ：GDN 模型算法复现
* **毛玉林** ：ChaosMesh 故障注入、论文阅读与结果评估

## 常见问题与解决办法

1. **minikube 集群上下文异常**
   执行 `minikube update-context` 与 `minikube start` 刷新集群状态。
2. **Selenium 测试因浏览器缓存中断**
   禁用浏览器 BFCache 机制，导出 Python 脚本本地运行。
3. **JMeter 命令行运行崩溃**
   改用 GUI 模式运行测试（`jmeter -g result.jtl -e -o report`）。
4. **数据预处理缺失值问题**
   采用列均值填充缺失值，使用 Min-Max 归一化统一特征尺度。

## 项目总结

本实验构建了从故障注入、性能监控到自动化测试的完整微服务质量保障体系，验证了 Online-Boutique 系统在不同负载下的稳定性。通过 GDN 模型实现了高精度的异常检测，为微服务系统的可靠性优化提供了数据支撑。团队协作完成了从环境搭建到算法复现的全流程实践，积累了微服务测试与维护的实战经验。
