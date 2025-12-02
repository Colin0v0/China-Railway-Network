# 🚄 中国高铁网络规划与分析系统 (China High-Speed Railway Network System)

> 基于图论与 Web 可视化的中国高铁模拟分析平台

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![ECharts](https://img.shields.io/badge/Visualization-ECharts-red)

## 📖 项目介绍

本项目是一个基于 Python 和图论算法的高铁网络分析系统。通过模拟中国 34 个省级行政区中心城市的高铁连接，实现了路径规划、网络分析和交互式可视化功能。

系统采用 **B/S 架构**（Browser/Server），后端使用 **Flask** 框架处理图论算法，前端使用 **ECharts** 进行专业的地理数据可视化，界面现代、交互流畅。

### ✨ 核心功能

1.  **交互式地图可视化**
    - 基于真实地理坐标的中国地图。
    - 动态展示高铁线路网络和城市节点。
    - 支持缩放、平移、悬停查看详情。

2.  **智能路径规划**
    - **双目标优化**：同时计算“时间最短”和“票价最低”两种方案。
    - **多途径点规划**：支持添加多个中间途经城市，自动规划最优串联路线。
    - **多种算法支持**：集成 Dijkstra、A*、BFS 等多种寻路算法。

3.  **最小生成树 (MST) 演示**
    - **算法演示**：动态展示 Prim 和 Kruskal 算法构建最小生成树的过程。
    - **多维优化**：支持按“最低建设成本”或“最短连通时间”生成网络。
    - **动画交互**：可视化呈现算法执行步骤，直观理解图论原理。

4.  **复杂网络分析**
    - **多维指标**：计算介数中心性、度中心性、接近中心性及聚类系数。
    - **枢纽识别**：自动识别并展示网络中的关键枢纽城市。

## 🛠️ 技术栈

-   **后端**: Python, Flask, NetworkX
-   **前端**: HTML5, Bootstrap 5, Apache ECharts
-   **算法**: Dijkstra, A*, BFS, Prim, Kruskal, Centrality Algorithms

## 📂 目录结构

```
China Railway Network/
├── algorithms/          # 图论算法实现
├── core/                # 网络构建核心逻辑
├── data/                # 城市与线路数据
├── static/              # 静态资源 (CSS, JS)
├── templates/           # HTML 模板
├── visualization/       # 可视化辅助模块
├── app.py               # Flask Web 应用入口
└── README.md            # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

请确保已安装 Python 环境，并在终端中运行以下命令安装所需库：

```bash
pip install flask networkx
```

### 2. 启动系统

在项目根目录下运行：

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：`http://127.0.0.1:5000`

## 📝 课程设计说明

本项目展示了图论在交通网络中的实际应用：
-   **图建模**: 城市为节点，高铁线路为边，时间/票价为权重。
-   **最短路径**: 解决点对点及多途径点的最优路线问题。
-   **最小生成树**: 解决以最小成本连通所有城市的网络构建问题。
-   **中心性分析**: 解决网络关键节点的识别问题。

---
*Designed for Graph Theory Course Project*
