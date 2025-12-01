# -*- coding: utf-8 -*-
"""
中国高铁网络规划与分析系统 - 主程序
====================================
交互式控制台界面

功能：
1. 双目标路径规划（时间最短 / 票价最低）
2. 网络枢纽分析（介数中心性）
3. 网络可视化（带中国地图轮廓）

运行：python main.py
"""

import sys
import matplotlib.pyplot as plt

# 添加项目根目录到路径
sys.path.insert(0, '.')

from data.cities import CITIES, CITY_CATEGORIES, get_all_city_names
from core.network import create_railway_network, get_network_stats
from algorithms.graph_algorithms import find_dual_paths, calculate_betweenness_centrality
from visualization.map_drawer import setup_chinese_font, create_visualization
from ui.console_ui import (
    clear_screen, print_header, print_menu,
    print_cities_list, select_city,
    print_path_result, print_hub_analysis,
    print_network_stats, wait_for_key
)


class RailwaySystem:
    """高铁网络系统主类"""
    
    def __init__(self):
        """初始化系统"""
        print("正在初始化系统...")
        setup_chinese_font()
        
        # 构建网络
        self.G, self.pos = create_railway_network()
        self.cities = get_all_city_names()
        self.stats = get_network_stats(self.G)
        
        # 缓存枢纽分析结果
        self.top_hubs = None
        
        print(f"✓ 系统初始化完成")
        print(f"  - 加载 {self.stats['node_count']} 个城市")
        print(f"  - 加载 {self.stats['edge_count']} 条高铁线路")
    
    def path_planning(self):
        """路径规划功能"""
        clear_screen()
        print_header()
        print("【路径规划】请选择起点和终点城市\n")
        
        # 选择起点
        start = select_city(self.cities, "📍 请选择起点城市:")
        print(f"✓ 起点: {start}\n")
        
        # 选择终点
        end = select_city(self.cities, "📍 请选择终点城市:")
        print(f"✓ 终点: {end}\n")
        
        if start == end:
            print("⚠️ 起点和终点相同，无需规划路径")
            wait_for_key()
            return
        
        print("正在计算最优路径...")
        
        # 计算双目标路径
        result = find_dual_paths(self.G, start, end)
        
        # 打印结果
        print_path_result(result)
        
        # 询问是否显示地图
        choice = input("\n是否显示可视化地图? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '是', '']:
            # 获取枢纽信息
            if self.top_hubs is None:
                self.top_hubs = calculate_betweenness_centrality(self.G, top_n=5)
            
            print("正在生成可视化地图...")
            fig = create_visualization(
                self.G, self.pos,
                time_path=result['time_path'],
                cost_path=result['cost_path'],
                top_hubs=self.top_hubs,
                result=result,
                save_path='railway_route.png'
            )
            print("✓ 地图已保存至 railway_route.png")
            plt.show()
        
        wait_for_key()
    
    def hub_analysis(self):
        """枢纽分析功能"""
        clear_screen()
        print_header()
        print("【网络枢纽分析】\n")
        
        print("正在计算介数中心性...")
        self.top_hubs = calculate_betweenness_centrality(self.G, top_n=5)
        
        print_hub_analysis(self.top_hubs)
        
        # 询问是否显示地图
        choice = input("\n是否显示可视化地图? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '是', '']:
            print("正在生成可视化地图...")
            fig = create_visualization(
                self.G, self.pos,
                top_hubs=self.top_hubs,
                save_path='railway_hubs.png'
            )
            print("✓ 地图已保存至 railway_hubs.png")
            plt.show()
        
        wait_for_key()
    
    def show_cities(self):
        """显示城市列表"""
        clear_screen()
        print_header()
        print_cities_list(self.cities, CITY_CATEGORIES)
        wait_for_key()
    
    def show_stats(self):
        """显示网络统计"""
        clear_screen()
        print_header()
        print_network_stats(self.stats)
        wait_for_key()
    
    def show_map_only(self):
        """仅显示网络地图"""
        clear_screen()
        print_header()
        print("【网络地图】\n")
        
        if self.top_hubs is None:
            print("正在分析网络枢纽...")
            self.top_hubs = calculate_betweenness_centrality(self.G, top_n=5)
        
        print("正在生成网络地图...")
        fig = create_visualization(
            self.G, self.pos,
            top_hubs=self.top_hubs,
            save_path='railway_network.png'
        )
        print("✓ 地图已保存至 railway_network.png")
        plt.show()
        
        wait_for_key()
    
    def run(self):
        """运行主程序"""
        while True:
            clear_screen()
            print_header()
            print_menu()
            
            choice = input("请输入选项 [0-5]: ").strip()
            
            if choice == '1':
                self.path_planning()
            elif choice == '2':
                self.hub_analysis()
            elif choice == '3':
                self.show_cities()
            elif choice == '4':
                self.show_stats()
            elif choice == '5':
                self.show_map_only()
            elif choice == '0':
                clear_screen()
                print("\n👋 感谢使用中国高铁网络规划与分析系统！")
                print("   再见！\n")
                break
            else:
                print("⚠️ 无效选项，请重新输入")
                wait_for_key()


def main():
    """主函数入口"""
    try:
        system = RailwaySystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
