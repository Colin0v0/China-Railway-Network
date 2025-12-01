# -*- coding: utf-8 -*-
"""
图论算法模块
============
包含 Dijkstra 最短路径和介数中心性算法
"""

import heapq
import networkx as nx
import math

def heuristic(u, v, G):
    """
    A* 算法的启发式函数 (欧几里得距离)
    """
    x1, y1 = G.nodes[u]['pos']
    x2, y2 = G.nodes[v]['pos']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def get_path_weight(G, path, weight):
    """计算路径的总权重"""
    if not path:
        return 0
    return sum(G[path[i]][path[i+1]][weight] for i in range(len(path)-1))

def bfs_shortest_path(G, start, end):
    """BFS 最少中转路径"""
    try:
        path = nx.shortest_path(G, source=start, target=end)
        return path, len(path) - 1, None
    except nx.NetworkXNoPath:
        return None, float('inf'), "无路径"

def astar_shortest_path(G, start, end, weight='time'):
    """A* 最短路径"""
    try:
        # 定义针对特定权重的启发式函数包装器
        # 注意：这里简单使用距离作为启发，实际应根据权重类型调整比例
        # 但作为演示，保持 admissible 即可
        h = lambda u, v: heuristic(u, v, G) if weight == 'time' else 0
        
        path = nx.astar_path(G, start, end, heuristic=h, weight=weight)
        total = get_path_weight(G, path, weight)
        return path, total, None
    except nx.NetworkXNoPath:
        return None, float('inf'), "无路径"

def dijkstra_shortest_path(G, start, end, weight='time'):
    """Dijkstra 最短路径"""
    try:
        path = nx.dijkstra_path(G, start, end, weight=weight)
        total = get_path_weight(G, path, weight)
        return path, total, None
    except nx.NetworkXNoPath:
        return None, float('inf'), "无路径"

def find_dual_paths(G, start, end, algorithm='dijkstra'):
    """
    多算法路径规划
    """
    result = {
        'start': start,
        'end': end,
        'algorithm': algorithm,
        'time_path': None,
        'cost_path': None,
        'time_details': [],
        'cost_details': []
    }

    if algorithm == 'bfs':
        # BFS 仅计算最少中转
        path, stops, err = bfs_shortest_path(G, start, end)
        if path:
            result['time_path'] = path
            result['total_time'] = get_path_weight(G, path, 'time')
            result['time_path_cost'] = get_path_weight(G, path, 'cost')
            # BFS 模式下，Cost Path 设为相同，或者不显示
            result['cost_path'] = path
            result['total_cost'] = result['time_path_cost']
            result['cost_path_time'] = result['total_time']
    
    elif algorithm == 'astar':
        # A* 算法
        t_path, t_val, t_err = astar_shortest_path(G, start, end, 'time')
        c_path, c_val, c_err = astar_shortest_path(G, start, end, 'cost')
        
        result['time_path'] = t_path
        result['total_time'] = t_val
        result['cost_path'] = c_path
        result['total_cost'] = c_val
        
        if t_path:
            result['time_path_cost'] = get_path_weight(G, t_path, 'cost')
        if c_path:
            result['cost_path_time'] = get_path_weight(G, c_path, 'time')

    else:
        # 默认 Dijkstra
        t_path, t_val, t_err = dijkstra_shortest_path(G, start, end, 'time')
        c_path, c_val, c_err = dijkstra_shortest_path(G, start, end, 'cost')
        
        result['time_path'] = t_path
        result['total_time'] = t_val
        result['cost_path'] = c_path
        result['total_cost'] = c_val
        
        if t_path:
            result['time_path_cost'] = get_path_weight(G, t_path, 'cost')
        if c_path:
            result['cost_path_time'] = get_path_weight(G, c_path, 'time')

    # 生成详细的分段数据（用于前端标注）
    if result.get('time_path'):
        result['time_details'] = get_path_details(G, result['time_path'])
    if result.get('cost_path'):
        result['cost_details'] = get_path_details(G, result['cost_path'])

    return result

def calculate_betweenness_centrality(G, top_n=5):
    """计算介数中心性"""
    betweenness = nx.betweenness_centrality(G, weight='time', normalized=True)
    sorted_cities = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    return sorted_cities[:top_n]

def get_path_details(G, path):
    """获取路径详细信息"""
    if not path or len(path) < 2:
        return []
    
    details = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        data = G[u][v]
        details.append({
            'source': u,
            'target': v,
            'time': data['time'],
            'cost': data['cost']
        })
    return details
