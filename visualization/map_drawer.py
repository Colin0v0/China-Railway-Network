# -*- coding: utf-8 -*-
"""
可视化模块
==========
网络地图绘制
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

from data.map_outline import (
    get_china_outline, get_taiwan_outline,
    get_hainan_outline, get_nine_dash_line
)


def setup_chinese_font():
    """配置中文字体"""
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'FangSong', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False


def draw_china_map(ax):
    """绘制中国地图轮廓"""
    # 大陆轮廓
    mainland = get_china_outline()
    if mainland:
        xs, ys = zip(*mainland)
        ax.fill(xs, ys, color='#E8F4E8', alpha=0.6, edgecolor='#4A7C59', linewidth=1.5)
    
    # 台湾
    taiwan = get_taiwan_outline()
    if taiwan:
        xs, ys = zip(*taiwan)
        ax.fill(xs, ys, color='#E8F4E8', alpha=0.6, edgecolor='#4A7C59', linewidth=1.5)
    
    # 海南
    hainan = get_hainan_outline()
    if hainan:
        xs, ys = zip(*hainan)
        ax.fill(xs, ys, color='#E8F4E8', alpha=0.6, edgecolor='#4A7C59', linewidth=1.5)
    
    # 九段线（虚线）
    nine_dash = get_nine_dash_line()
    if nine_dash:
        xs, ys = zip(*nine_dash)
        ax.plot(xs, ys, color='#4A7C59', linewidth=1, linestyle='--', alpha=0.5)


def draw_network_on_map(ax, G, pos, time_path=None, cost_path=None, top_hubs=None):
    """
    在地图上绘制高铁网络
    """
    hub_cities = [hub[0] for hub in top_hubs] if top_hubs else []
    
    # 1. 绘制所有边（背景线路）
    for edge in G.edges():
        x1, y1 = pos[edge[0]]
        x2, y2 = pos[edge[1]]
        ax.plot([x1, x2], [y1, y2], color='#B0B0B0', linewidth=1.2, alpha=0.5, zorder=1)
    
    # 2. 绘制路径
    offset = 0.15
    
    if time_path and len(time_path) > 1:
        for i in range(len(time_path) - 1):
            x1, y1 = pos[time_path[i]]
            x2, y2 = pos[time_path[i + 1]]
            ax.plot([x1, x2], [y1 + offset, y2 + offset], 
                   color='#E63946', linewidth=3, alpha=0.9, zorder=3,
                   solid_capstyle='round')
    
    if cost_path and len(cost_path) > 1:
        for i in range(len(cost_path) - 1):
            x1, y1 = pos[cost_path[i]]
            x2, y2 = pos[cost_path[i + 1]]
            ax.plot([x1, x2], [y1 - offset, y2 - offset], 
                   color='#2A9D8F', linewidth=3, linestyle='--', alpha=0.9, zorder=3,
                   solid_capstyle='round')
    
    # 3. 绘制节点
    for node in G.nodes():
        x, y = pos[node]
        
        if time_path and node in time_path:
            # 时间最短路径上的节点
            circle = plt.Circle((x, y), 0.6, color='#E63946', ec='white', linewidth=2, zorder=5)
            ax.add_patch(circle)
        elif cost_path and node in cost_path:
            # 票价最低路径上的节点
            circle = plt.Circle((x, y), 0.6, color='#2A9D8F', ec='white', linewidth=2, zorder=5)
            ax.add_patch(circle)
        elif node in hub_cities:
            # 枢纽城市
            circle = plt.Circle((x, y), 0.7, color='#F4A261', ec='white', linewidth=2, zorder=4)
            ax.add_patch(circle)
        else:
            # 普通城市
            circle = plt.Circle((x, y), 0.45, color='#457B9D', ec='white', linewidth=1.5, zorder=4)
            ax.add_patch(circle)
    
    # 4. 绘制标签
    for node in G.nodes():
        x, y = pos[node]
        fontsize = 7
        fontweight = 'normal'
        
        if node in hub_cities or (time_path and node in time_path) or (cost_path and node in cost_path):
            fontsize = 8
            fontweight = 'bold'
        
        ax.annotate(node, (x, y), textcoords="offset points", 
                   xytext=(0, 8), ha='center', fontsize=fontsize,
                   fontweight=fontweight, color='#2D3436', zorder=6)


def create_visualization(G, pos, time_path=None, cost_path=None, top_hubs=None, 
                         result=None, save_path=None):
    """
    创建完整的可视化图
    """
    setup_chinese_font()
    
    # 创建画布
    fig = plt.figure(figsize=(18, 12), facecolor='#F8F9FA')
    
    # 主地图区域
    ax_map = fig.add_axes([0.02, 0.05, 0.68, 0.88])
    ax_map.set_facecolor('#E8F4FC')
    
    # 绘制地图和网络
    draw_china_map(ax_map)
    draw_network_on_map(ax_map, G, pos, time_path, cost_path, top_hubs)
    
    # 设置地图范围
    ax_map.set_xlim(72, 138)
    ax_map.set_ylim(16, 55)
    ax_map.set_aspect('equal')
    ax_map.axis('off')
    
    # 标题
    ax_map.set_title('中国高铁网络规划与分析系统', fontsize=20, fontweight='bold', 
                     color='#2D3436', pad=15)
    
    # ========== 右侧信息面板 ==========
    ax_info = fig.add_axes([0.72, 0.05, 0.26, 0.88])
    ax_info.set_facecolor('#FFFFFF')
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis('off')
    
    # 添加边框
    for spine in ax_info.spines.values():
        spine.set_visible(True)
        spine.set_color('#DEE2E6')
        spine.set_linewidth(2)
    
    y_pos = 0.95
    
    # 面板标题
    ax_info.text(0.5, y_pos, '[ 路线规划结果 ]', fontsize=14, fontweight='bold',
                ha='center', va='top', color='#2D3436')
    y_pos -= 0.06
    
    # 分隔线
    ax_info.axhline(y=y_pos, xmin=0.05, xmax=0.95, color='#DEE2E6', linewidth=1)
    y_pos -= 0.04
    
    if result:
        # 起终点信息
        ax_info.text(0.5, y_pos, f"{result['start']}  >>>  {result['end']}", 
                    fontsize=12, ha='center', va='top', color='#2D3436', fontweight='bold')
        y_pos -= 0.07
        
        # 方案A：时间最短
        ax_info.add_patch(FancyBboxPatch((0.03, y_pos - 0.18), 0.94, 0.18,
                         boxstyle="round,pad=0.01", facecolor='#FEE2E2', 
                         edgecolor='#E63946', linewidth=1.5))
        
        ax_info.text(0.07, y_pos - 0.02, '[A] 时间最短方案', fontsize=10, 
                    fontweight='bold', color='#E63946', va='top')
        
        if result['time_path']:
            path_str = ' > '.join(result['time_path'])
            # 自动换行
            if len(path_str) > 25:
                mid = len(result['time_path']) // 2
                line1 = ' > '.join(result['time_path'][:mid+1])
                line2 = ' > '.join(result['time_path'][mid:])
                ax_info.text(0.07, y_pos - 0.06, line1, fontsize=8, color='#4A4A4A', va='top')
                ax_info.text(0.07, y_pos - 0.10, line2, fontsize=8, color='#4A4A4A', va='top')
            else:
                ax_info.text(0.07, y_pos - 0.06, path_str, fontsize=8, color='#4A4A4A', va='top')
            
            ax_info.text(0.07, y_pos - 0.14, 
                        f"时间: {result['total_time']:.1f}h | 票价: {result['time_path_cost']}元 | {len(result['time_path'])}站",
                        fontsize=9, color='#E63946', va='top', fontweight='bold')
        else:
            ax_info.text(0.07, y_pos - 0.08, '未找到可达路径', fontsize=9, color='#999', va='top')
        
        y_pos -= 0.24
        
        # 方案B：票价最低
        ax_info.add_patch(FancyBboxPatch((0.03, y_pos - 0.18), 0.94, 0.18,
                         boxstyle="round,pad=0.01", facecolor='#D1FAE5', 
                         edgecolor='#2A9D8F', linewidth=1.5))
        
        ax_info.text(0.07, y_pos - 0.02, '[B] 票价最低方案', fontsize=10, 
                    fontweight='bold', color='#2A9D8F', va='top')
        
        if result['cost_path']:
            path_str = ' > '.join(result['cost_path'])
            if len(path_str) > 25:
                mid = len(result['cost_path']) // 2
                line1 = ' > '.join(result['cost_path'][:mid+1])
                line2 = ' > '.join(result['cost_path'][mid:])
                ax_info.text(0.07, y_pos - 0.06, line1, fontsize=8, color='#4A4A4A', va='top')
                ax_info.text(0.07, y_pos - 0.10, line2, fontsize=8, color='#4A4A4A', va='top')
            else:
                ax_info.text(0.07, y_pos - 0.06, path_str, fontsize=8, color='#4A4A4A', va='top')
            
            ax_info.text(0.07, y_pos - 0.14, 
                        f"票价: {result['total_cost']}元 | 时间: {result['cost_path_time']:.1f}h | {len(result['cost_path'])}站",
                        fontsize=9, color='#2A9D8F', va='top', fontweight='bold')
        
        y_pos -= 0.24
        
        # 方案对比
        if result['time_path'] and result['cost_path']:
            ax_info.text(0.5, y_pos, '📈 方案对比', fontsize=10, fontweight='bold',
                        ha='center', va='top', color='#2D3436')
            y_pos -= 0.05
            
            time_diff = result['cost_path_time'] - result['total_time']
            cost_diff = result['time_path_cost'] - result['total_cost']
            
            if result['time_path'] == result['cost_path']:
                ax_info.text(0.5, y_pos, '✨ 两方案路线相同，这是最优路径！', 
                            fontsize=9, ha='center', va='top', color='#10B981')
            else:
                ax_info.text(0.07, y_pos, f'• 选A可节省 {time_diff:.1f} 小时', 
                            fontsize=9, va='top', color='#E63946')
                y_pos -= 0.04
                ax_info.text(0.07, y_pos, f'• 选B可节省 {cost_diff} 元', 
                            fontsize=9, va='top', color='#2A9D8F')
            
            y_pos -= 0.06
    
    # 分隔线
    ax_info.axhline(y=y_pos, xmin=0.05, xmax=0.95, color='#DEE2E6', linewidth=1)
    y_pos -= 0.04
    
    # 枢纽分析
    if top_hubs:
        ax_info.text(0.5, y_pos, '🏆 网络枢纽 TOP 5', fontsize=11, fontweight='bold',
                    ha='center', va='top', color='#2D3436')
        y_pos -= 0.05
        
        for i, (city, score) in enumerate(top_hubs):
            medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i]
            bar_width = score * 2
            
            ax_info.add_patch(FancyBboxPatch((0.35, y_pos - 0.025), bar_width, 0.025,
                             boxstyle="round,pad=0.002", facecolor='#F4A261', alpha=0.7))
            
            ax_info.text(0.07, y_pos, f'{medal} {city}', fontsize=9, va='center', color='#2D3436')
            ax_info.text(0.93, y_pos, f'{score:.3f}', fontsize=8, va='center', 
                        ha='right', color='#666')
            y_pos -= 0.04
    
    y_pos -= 0.02
    
    # 分隔线
    ax_info.axhline(y=y_pos, xmin=0.05, xmax=0.95, color='#DEE2E6', linewidth=1)
    y_pos -= 0.04
    
    # 图例
    ax_info.text(0.5, y_pos, '📋 图例', fontsize=10, fontweight='bold',
                ha='center', va='top', color='#2D3436')
    y_pos -= 0.04
    
    legends = [
        ('━━━', '#E63946', '时间最短路径'),
        ('╍╍╍', '#2A9D8F', '票价最低路径'),
        ('●', '#F4A261', '枢纽城市'),
        ('●', '#457B9D', '普通城市'),
        ('━', '#B0B0B0', '高铁线路'),
    ]
    
    for symbol, color, label in legends:
        ax_info.text(0.12, y_pos, symbol, fontsize=10, va='center', 
                    color=color, fontweight='bold', family='monospace')
        ax_info.text(0.25, y_pos, label, fontsize=9, va='center', color='#4A4A4A')
        y_pos -= 0.035
    
    # 网络统计
    y_pos -= 0.02
    ax_info.axhline(y=y_pos, xmin=0.05, xmax=0.95, color='#DEE2E6', linewidth=1)
    y_pos -= 0.04
    
    ax_info.text(0.5, y_pos, '📌 网络信息', fontsize=10, fontweight='bold',
                ha='center', va='top', color='#2D3436')
    y_pos -= 0.04
    ax_info.text(0.07, y_pos, f'城市节点: {G.number_of_nodes()} 个', fontsize=9, va='top', color='#666')
    y_pos -= 0.035
    ax_info.text(0.07, y_pos, f'高铁线路: {G.number_of_edges()} 条', fontsize=9, va='top', color='#666')
    y_pos -= 0.035
    ax_info.text(0.07, y_pos, '含京台高铁(福州-台北)', fontsize=8, va='top', color='#999')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', 
                   facecolor='#F8F9FA', edgecolor='none')
    
    return fig
