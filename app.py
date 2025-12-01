# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import networkx as nx
from core.network import create_railway_network
from algorithms.graph_algorithms import find_dual_paths, calculate_betweenness_centrality
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
    algorithm = data.get('algorithm', 'dijkstra')
    
    if not start or not end:
        return jsonify({"error": "请选择起点和终点"}), 400
        
    result = find_dual_paths(G, start, end, algorithm)
    return jsonify(result)

@app.route('/api/hubs')
def get_hubs():
    """获取枢纽分析结果"""
    top_hubs = calculate_betweenness_centrality(G, top_n=5)
    # 格式化为前端易用的格式
    formatted_hubs = [{"name": city, "score": score} for city, score in top_hubs]
    return jsonify(formatted_hubs)

def get_city_category(city_name):
    for cat, cities in CITY_CATEGORIES.items():
        if city_name in cities:
            return cat
    return "其他"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
