# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import networkx as nx
from core.network import create_railway_network
from algorithms.graph_algorithms import (
    find_dual_paths, 
    calculate_betweenness_centrality,
    calculate_advanced_metrics,
    get_mst_steps,
    find_multi_stop_path
)
from data.cities import CITIES, CITY_CATEGORIES

app = Flask(__name__)

# 初始化网络
G, pos = create_railway_network()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph-data')
def get_graph_data():
    """获取图数据用于前端渲染"""
    nodes = []
    for node, coords in pos.items():
        nodes.append({
            "name": node,
            "value": coords,  # [lng, lat]
            "category": get_city_category(node)
        })
    
    edges = []
    for u, v, data in G.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "time": data['time'],
            "cost": data['cost']
        })
        
    return jsonify({
        "nodes": nodes,
        "edges": edges
    })

@app.route('/api/cities')
def get_cities():
    """获取城市列表"""
    return jsonify(list(CITIES.keys()))

@app.route('/api/path', methods=['POST'])
def calculate_path():
    """计算路径"""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    waypoints = data.get('waypoints', [])
    algorithm = data.get('algorithm', 'dijkstra')
    
    if not start or not end:
        return jsonify({"error": "请选择起点和终点"}), 400
    
    if waypoints:
        result = find_multi_stop_path(G, start, end, waypoints)
    else:
        result = find_dual_paths(G, start, end, algorithm)
        
    return jsonify(result)

@app.route('/api/mst')
def get_mst():
    """获取最小生成树动画步骤"""
    algo = request.args.get('algorithm', 'prim')
    weight = request.args.get('weight', 'cost')
    steps = get_mst_steps(G, algo, weight)
    return jsonify({"steps": steps})

@app.route('/api/hubs')
def get_hubs():
    """获取枢纽分析结果"""
    top_hubs = calculate_betweenness_centrality(G, top_n=5)
    # 格式化为前端易用的格式
    formatted_hubs = [{"name": city, "score": score} for city, score in top_hubs]
    return jsonify(formatted_hubs)

@app.route('/api/advanced-analysis')
def get_advanced_analysis():
    """获取高级网络分析指标"""
    metrics = calculate_advanced_metrics(G, top_n=5)
    
    # 格式化数据
    result = {
        'degree': [{"name": c, "score": s} for c, s in metrics['degree']],
        'closeness': [{"name": c, "score": s} for c, s in metrics['closeness']],
        'clustering': [{"name": c, "score": s} for c, s in metrics['clustering']],
        'avg_clustering': metrics['avg_clustering']
    }
    return jsonify(result)

@app.errorhandler(Exception)
def handle_exception(e):
    """全局异常处理"""
    return jsonify({"error": str(e)}), 500

def get_city_category(city_name):
    for cat, cities in CITY_CATEGORIES.items():
        if city_name in cities:
            return cat
    return "其他"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
