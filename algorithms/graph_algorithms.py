# -*- coding: utf-8 -*-
"""
图论算法模块
============
包含 Dijkstra 最短路径和介数中心性算法
"""

import heapq
import networkx as nx
import math
import time

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

def calculate_advanced_metrics(G, top_n=5):
    """
    计算高级网络指标
    包含：度中心性、接近中心性、聚类系数
    """
    # 1. 度中心性 (Degree Centrality)
    degree_cent = nx.degree_centrality(G)
    top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # 2. 接近中心性 (Closeness Centrality)
    # 反映节点到其他所有节点的平均距离，越近说明去哪里都快
    closeness_cent = nx.closeness_centrality(G, distance='time')
    top_closeness = sorted(closeness_cent.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # 3. 聚类系数 (Clustering Coefficient)
    # 反映节点的邻居之间互连的程度，衡量网络的聚集性
    clustering = nx.clustering(G)
    avg_clustering = nx.average_clustering(G)
    top_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    return {
        'degree': top_degree,
        'closeness': top_closeness,
        'clustering': top_clustering,
        'avg_clustering': avg_clustering
    }

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

def get_mst_steps(G, algorithm='prim', weight_key='cost'):
    """
    获取最小生成树的构建步骤（用于动画）
    默认使用 'cost' (票价/建设成本) 作为权重
    """
    steps = []
    
    if algorithm == 'kruskal':
        # Kruskal: 按边权排序，从小到大添加不构成环的边
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append((u, v, data.get(weight_key, 0)))
        
        # 按成本排序
        edges.sort(key=lambda x: x[2])
        
        # 并查集初始化
        parent = {node: node for node in G.nodes()}
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
            
        for u, v, w in edges:
            if union(u, v):
                steps.append({'u': u, 'v': v, 'weight': w, 'action': 'add'})
            else:
                # 记录被拒绝的边（构成环），可选用于动画展示
                # steps.append({'u': u, 'v': v, 'weight': w, 'action': 'reject'})
                pass
                
    elif algorithm == 'prim':
        # Prim: 从一个节点开始，不断选择连接已访问集合和未访问集合的最小边
        if not G.nodes():
            return []
            
        start_node = list(G.nodes())[0] # 任意选择起点，例如北京
        visited = {start_node}
        candidate_edges = []
        
        # 初始化候选边
        for neighbor, data in G[start_node].items():
            heapq.heappush(candidate_edges, (data.get(weight_key, 0), start_node, neighbor))
            
        while candidate_edges:
            weight, u, v = heapq.heappop(candidate_edges)
            
            if v not in visited:
                visited.add(v)
                steps.append({'u': u, 'v': v, 'weight': weight, 'action': 'add'})
                
                for neighbor, data in G[v].items():
                    if neighbor not in visited:
                        heapq.heappush(candidate_edges, (data.get(weight_key, 0), v, neighbor))
    
    return steps

def find_multi_stop_path(G, start, end, waypoints):
    """
    多途径点路径规划
    逻辑：Start -> Waypoint1 -> Waypoint2 -> ... -> End
    """
    full_route_points = [start] + waypoints + [end]
    
    # 结果容器
    result = {
        'start': start,
        'end': end,
        'waypoints': waypoints,
        'time_path': [],
        'total_time': 0,
        'time_path_cost': 0,
        'cost_path': [],
        'total_cost': 0,
        'cost_path_time': 0,
        'time_details': [],
        'cost_details': []
    }
    
    try:
        # 1. 计算时间最短的拼接路径
        curr_path = []
        for i in range(len(full_route_points)-1):
            u, v = full_route_points[i], full_route_points[i+1]
            # 计算分段路径
            seg_path = nx.dijkstra_path(G, u, v, weight='time')
            # 拼接（注意去除重复的连接点）
            if i > 0:
                curr_path.extend(seg_path[1:])
            else:
                curr_path.extend(seg_path)
        
        result['time_path'] = curr_path
        result['total_time'] = get_path_weight(G, curr_path, 'time')
        result['time_path_cost'] = get_path_weight(G, curr_path, 'cost')
        result['time_details'] = get_path_details(G, curr_path)

        # 2. 计算票价最低的拼接路径
        curr_path = []
        for i in range(len(full_route_points)-1):
            u, v = full_route_points[i], full_route_points[i+1]
            seg_path = nx.dijkstra_path(G, u, v, weight='cost')
            if i > 0:
                curr_path.extend(seg_path[1:])
            else:
                curr_path.extend(seg_path)
                
        result['cost_path'] = curr_path
        result['total_cost'] = get_path_weight(G, curr_path, 'cost')
        result['cost_path_time'] = get_path_weight(G, curr_path, 'time')
        result['cost_details'] = get_path_details(G, curr_path)
        
        return result
        
    except nx.NetworkXNoPath:
        return {'error': '路径不可达，请检查途径点是否连通'}
