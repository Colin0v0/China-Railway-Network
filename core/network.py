# -*- coding: utf-8 -*-
"""
网络构建模块
============
构建高铁网络图
"""

import networkx as nx
from data.cities import CITIES
from data.railways import RAILWAY_EDGES


def create_railway_network():
    """
    创建高铁网络图
    
    返回：
        G: NetworkX 图对象
        pos: 节点位置字典
    """
    G = nx.Graph()
    
    # 添加节点
    for city, coords in CITIES.items():
        G.add_node(city, pos=coords)
    
    # 添加边
    for city1, city2, time, cost in RAILWAY_EDGES:
        if city1 in G.nodes and city2 in G.nodes:
            G.add_edge(city1, city2, time=time, cost=cost)
    
    # 位置字典
    pos = {city: coords for city, coords in CITIES.items()}
    
    return G, pos


def get_network_stats(G):
    """获取网络统计信息"""
    degrees = dict(G.degree())
    avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
    max_degree_city = max(degrees, key=degrees.get) if degrees else None
    
    stats = {
        'node_count': G.number_of_nodes(),
        'edge_count': G.number_of_edges(),
        'avg_degree': avg_degree,
        'max_degree_city': max_degree_city,
        'max_degree': degrees.get(max_degree_city, 0) if max_degree_city else 0,
        'is_connected': nx.is_connected(G),
    }
    
    return stats
