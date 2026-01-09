import tkinter as tk
import math
import random
import time
from collections import deque

class UltimatePixelKnightV3:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("终极像素装甲骑士 V3.0 - 集群制造系统")
        self.window.geometry("1200x800")
        self.window.configure(bg='#0a0a14')
        
        # 主画布
        self.canvas = tk.Canvas(self.window, width=1200, height=800, bg='#0a0a14', highlightthickness=0)
        self.canvas.pack()
        
        # === 核心系统 ===
        self.x, self.y = 600, 400
        self.target_x, self.target_y = 600, 400
        self.angle = 0
        self.speed = 0
        self.breath_phase = 0
        self.action_phase = 0
        self.action_type = 0
        
        # === 移动轨道 ===
        self.trail_positions = deque(maxlen=30)
        
        # === 粒子系统 ===
        self.particles = deque(maxlen=200)
        
        # === 属性系统 ===
        self.attributes = {
            '光': {'color': '#FFFF99', 'value': 1.0, 'abbr': 'LGT', 'synergy': {'火': 1.2, '电': 1.1}},
            '火': {'color': '#FF5555', 'value': 1.0, 'abbr': 'FIR', 'synergy': {'光': 1.2, '风': 1.1}},
            '冰': {'color': '#66CCFF', 'value': 1.0, 'abbr': 'ICE', 'synergy': {'水': 1.3, '地': 0.9}},
            '电': {'color': '#FFFF66', 'value': 1.0, 'abbr': 'ELC', 'synergy': {'光': 1.1, '风': 1.2}},
            '地': {'color': '#CC9966', 'value': 1.0, 'abbr': 'ERT', 'synergy': {'冰': 0.9, '火': 0.8}},
            '风': {'color': '#88FF88', 'value': 1.0, 'abbr': 'WND', 'synergy': {'火': 1.1, '电': 1.2}},
            '水': {'color': '#4488FF', 'value': 1.0, 'abbr': 'WTR', 'synergy': {'冰': 1.3, '地': 1.1}}
        }
        
        # === 制造系统 ===
        self.manufacturing = {
            'materials': {'光': 0, '火': 0, '冰': 0, '电': 0, '地': 0, '风': 0, '水': 0},
            'items_limit': 10,  # 物品限制
            'crafting_queue': [],
            'crafted_items': [],
            'blueprints': self.create_blueprints()
        }
        
        # === 通讯系统 ===
        self.communication = {
            'connected_nodes': [],
            'messages': deque(maxlen=20),
            'signal_strength': 100,
            'transmission_range': 150,
            'last_broadcast': 0
        }
        
        # === 发射系统 ===
        self.launch_system = {
            'projectiles': deque(maxlen=50),
            'energy': 100,
            'cooldown': 0,
            'launch_types': self.create_launch_types()
        }
        
        # === 分离系统 ===
        self.separation_system = {
            'deployed_units': deque(maxlen=5),
            'separation_cooldown': 0,
            'unit_types': self.create_unit_types()
        }
        
        # === 集群系统 ===
        self.swarm_system = {
            'swarm_units': deque(maxlen=20),
            'formation_patterns': self.create_formation_patterns(),
            'current_formation': 'circle',
            'swarm_intelligence': {'defense': 0, 'attack': 0, 'speed': 0}
        }
        
        # === 侦测系统 ===
        self.detection_system = {
            'detected_objects': [],
            'scan_range': 200,
            'scan_cooldown': 0,
            'scan_particles': deque(maxlen=50),
            'threat_level': 0
        }
        
        # === 装甲元素 ===
        self.armor_elements = self.create_armor_elements()
        
        # === 场景系统 ===
        self.scene_boundary = (100, 100, 1100, 700)
        self.scene_objects = self.create_scene_objects()
        
        # === 固定位置 ===
        self.fixed_positions = [
            {'x': 200, 'y': 200, 'type': '制造站', 'active': True},
            {'x': 1000, 'y': 200, 'type': '通讯塔', 'active': True},
            {'x': 600, 'y': 500, 'type': '发射台', 'active': True},
            {'x': 200, 'y': 600, 'type': '分离点', 'active': True},
            {'x': 1000, 'y': 600, 'type': '集群中心', 'active': True}
        ]
        
        # === 数据收集 ===
        self.collected_items = 0
        self.data_log = deque(maxlen=100)
        
        # === UI系统 ===
        self.ui_elements = []
        
        # 绑定事件
        self.setup_controls()
        
        # 开始动画
        self.animate()
        self.window.mainloop()
    
    def create_blueprints(self):
        """创建蓝图"""
        return {
            '防御核心': {'光': 2, '地': 1, '水': 1, 'time': 5.0, 'color': '#4A90E2'},
            '攻击模块': {'火': 3, '电': 1, 'time': 4.0, 'color': '#FF5555'},
            '通讯节点': {'电': 2, '风': 1, 'time': 3.0, 'color': '#FFFF66'},
            '扫描探针': {'光': 1, '水': 2, 'time': 3.5, 'color': '#66CCFF'},
            '集群单元': {'地': 2, '风': 1, '冰': 1, 'time': 6.0, 'color': '#88FF88'},
            '分离舱': {'火': 1, '地': 2, '水': 1, 'time': 7.0, 'color': '#CC9966'}
        }
    
    def create_launch_types(self):
        """创建发射类型"""
        return {
            '能量弹': {'cost': 10, 'speed': 8, 'color': '#FF5555', 'effect': 'explosion'},
            '信号弹': {'cost': 5, 'speed': 5, 'color': '#FFFF66', 'effect': 'signal'},
            '扫描波': {'cost': 15, 'speed': 12, 'color': '#66CCFF', 'effect': 'scan'},
            '通讯包': {'cost': 8, 'speed': 6, 'color': '#88FF88', 'effect': 'message'}
        }
    
    def create_unit_types(self):
        """创建单位类型"""
        return {
            '侦察机': {'health': 50, 'speed': 3, 'color': '#88CCFF', 'abilities': ['scan']},
            '护卫机': {'health': 100, 'speed': 2, 'color': '#FF8888', 'abilities': ['defend']},
            '工程机': {'health': 80, 'speed': 2, 'color': '#88FF88', 'abilities': ['repair', 'collect']},
            '信号机': {'health': 60, 'speed': 2, 'color': '#FFFF88', 'abilities': ['boost_signal']}
        }
    
    def create_formation_patterns(self):
        """创建阵型模式"""
        return {
            'circle': lambda center, radius, count: [
                (center[0] + math.cos(i*2*math.pi/count)*radius,
                 center[1] + math.sin(i*2*math.pi/count)*radius)
                for i in range(count)
            ],
            'line': lambda center, spacing, count: [
                (center[0] + i*spacing - (count-1)*spacing/2, center[1])
                for i in range(count)
            ],
            'triangle': lambda center, size, count: [
                (center[0] + size*math.cos(i*2*math.pi/3),
                 center[1] + size*math.sin(i*2*math.pi/3))
                for i in range(3)
            ],
            'v_formation': lambda center, spacing, count: [
                (center[0] + abs(i-count//2)*spacing*0.5,
                 center[1] + (i-count//2)*spacing)
                for i in range(count)
            ]
        }
    
    def create_armor_elements(self):
        """创建装甲元素"""
        elements = []
        
        element_configs = [
            # (id, x_offset, y_offset, width, height, color, attributes)
            ('头盔', 0, -15, 12, 8, '#4A90E2', ['光', '风']),
            ('面甲', 0, -8, 10, 6, '#FFD700', ['电', '光']),
            ('核心', 0, 0, 8, 8, '#FF5555', ['火', '光']),
            ('左肩甲', -12, 0, 8, 10, '#32CD32', ['地', '火']),
            ('右肩甲', 12, 0, 8, 10, '#32CD32', ['地', '冰']),
            ('左膝甲', -6, 18, 6, 6, '#8B4513', ['冰', '地']),
            ('右膝甲', 6, 18, 6, 6, '#8B4513', ['冰', '水']),
            ('徽章', 0, -25, 6, 6, '#FF3366', ['光', '火', '冰', '电', '地', '风', '水'])
        ]
        
        for config in element_configs:
            elem_id, px, py, w, h, color, attrs = config
            elements.append({
                'id': elem_id,
                'position': (px, py),
                'size': (w, h),
                'color': color,
                'attributes': attrs,
                'active': True,
                'energy': 100
            })
        
        return elements
    
    def create_scene_objects(self):
        """创建场景物体"""
        objects = []
        
        # 资源点
        for i, (attr, data) in enumerate(self.attributes.items()):
            x = 150 + i * 140
            y = 150
            objects.append({
                'type': 'resource',
                'subtype': 'crystal',
                'attribute': attr,
                'position': (x, y),
                'size': 15,
                'collected': False,  # 修复这里！
                'color': data['color'],
                'value': random.randint(1, 3),
                'respawn_timer': 0
            })
        
        # 制造站
        objects.append({
            'type': 'station',
            'subtype': 'manufacturing',
            'position': (200, 300),
            'size': 20,
            'color': '#8888FF',
            'active': True,
            'progress': 0
        })
        
        # 通讯塔
        objects.append({
            'type': 'station',
            'subtype': 'communication',
            'position': (1000, 300),
            'size': 20,
            'color': '#FFFF88',
            'active': True,
            'signal_strength': 100
        })
        
        # 威胁目标
        for i in range(3):
            x = random.randint(300, 900)
            y = random.randint(400, 600)
            objects.append({
                'type': 'threat',
                'subtype': 'drone',
                'position': (x, y),
                'size': 12,
                'color': '#FF4444',
                'health': 100,
                'detected': False,
                'movement_pattern': random.choice(['circle', 'patrol', 'stationary'])
            })
        
        return objects
    
    def setup_controls(self):
        """设置控制"""
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.window.bind("<KeyPress>", self.on_key_press)
        
        # 鼠标滚轮
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        
        # 拖拽
        self.canvas.bind("<B1-Motion>", self.on_drag)
    
    def on_mouse_move(self, event):
        """鼠标移动"""
        self.target_x = max(self.scene_boundary[0] + 30, 
                           min(self.scene_boundary[2] - 30, event.x))
        self.target_y = max(self.scene_boundary[1] + 30,
                           min(self.scene_boundary[3] - 30, event.y))
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
    
    def on_left_click(self, event):
        """左键点击"""
        # 收集资源
        for obj in self.scene_objects:
            if obj['type'] == 'resource' and not obj.get('collected', False):
                dx = event.x - obj['position'][0]
                dy = event.y - obj['position'][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < obj['size'] * 2:
                    self.collect_resource(obj)
                    return
        
        # 发射能量弹
        if self.launch_system['cooldown'] <= 0 and self.launch_system['energy'] >= 10:
            self.launch_projectile('能量弹', (event.x, event.y))
    
    def on_right_click(self, event):
        """右键点击"""
        # 启动扫描
        if self.detection_system['scan_cooldown'] <= 0:
            self.initiate_scan((event.x, event.y))
    
    def on_key_press(self, event):
        """按键控制"""
        key = event.keysym.lower()
        
        if key == 'space':
            # 冲刺
            self.speed = 12
            self.create_dash_particles()
            
        elif key == 'c':
            # 通讯广播
            self.broadcast_message("同步请求")
            
        elif key == 'm':
            # 制造物品
            self.start_crafting('防御核心')
            
        elif key == 'd':
            # 分离单位
            self.separate_unit('侦察机')
            
        elif key == 's':
            # 集群命令
            self.command_swarm('gather')
            
        elif key == 'r':
            # 重置
            self.reset_systems()
            
        elif key == '1':
            self.swarm_system['current_formation'] = 'circle'
        elif key == '2':
            self.swarm_system['current_formation'] = 'line'
        elif key == '3':
            self.swarm_system['current_formation'] = 'triangle'
        elif key == '4':
            self.swarm_system['current_formation'] = 'v_formation'
    
    def on_mouse_wheel(self, event):
        """鼠标滚轮"""
        # 调整发射能量
        delta = event.delta
        if delta > 0:
            self.launch_system['energy'] = min(100, self.launch_system['energy'] + 5)
        else:
            self.launch_system['energy'] = max(10, self.launch_system['energy'] - 5)
    
    def on_drag(self, event):
        """拖拽控制"""
        # 拖拽制造物品
        pass
    
    def collect_resource(self, resource):
        """收集资源"""
        resource['collected'] = True
        resource['respawn_timer'] = random.randint(300, 600)  # 5-10秒后重生
        
        attr = resource['attribute']
        value = resource['value']
        
        if attr in self.manufacturing['materials']:
            self.manufacturing['materials'][attr] += value
            self.collected_items += 1
            
            # 创建收集特效
            self.create_collection_effect(resource['position'])
            
            # 记录数据
            self.log_data(f"收集{attr}资源 x{value}")
    
    def launch_projectile(self, proj_type, target):
        """发射弹丸"""
        if proj_type not in self.launch_system['launch_types']:
            return
        
        launch_data = self.launch_system['launch_types'][proj_type]
        if self.launch_system['energy'] < launch_data['cost']:
            return
        
        self.launch_system['energy'] -= launch_data['cost']
        self.launch_system['cooldown'] = 10
        
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance == 0:
            return
        
        speed_x = dx / distance * launch_data['speed']
        speed_y = dy / distance * launch_data['speed']
        
        projectile = {
            'x': self.x,
            'y': self.y,
            'vx': speed_x,
            'vy': speed_y,
            'type': proj_type,
            'color': launch_data['color'],
            'size': 6,
            'life': 100,
            'effect': launch_data['effect'],
            'damage': launch_data.get('damage', 10)
        }
        
        self.launch_system['projectiles'].append(projectile)
        
        # 发射特效
        self.create_launch_effect()
        
        self.log_data(f"发射{proj_type}")
    
    def initiate_scan(self, position):
        """启动扫描"""
        self.detection_system['scan_cooldown'] = 60
        self.detection_system['threat_level'] = 0
        
        # 创建扫描波
        for i in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 4)
            
            self.detection_system['scan_particles'].append({
                'x': position[0],
                'y': position[1],
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': '#66CCFF',
                'size': random.uniform(2, 4),
                'life': 40
            })
        
        # 检测威胁
        for obj in self.scene_objects:
            if obj['type'] == 'threat':
                dx = position[0] - obj['position'][0]
                dy = position[1] - obj['position'][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < self.detection_system['scan_range']:
                    obj['detected'] = True
                    self.detection_system['threat_level'] += 20
                    self.log_data(f"侦测到威胁: {obj['subtype']}")
        
        self.log_data("扫描完成")
    
    def broadcast_message(self, message):
        """广播消息"""
        if time.time() - self.communication['last_broadcast'] < 2:
            return
        
        self.communication['last_broadcast'] = time.time()
        self.communication['messages'].append({
            'sender': '骑士',
            'message': message,
            'time': time.time(),
            'position': (self.x, self.y)
        })
        
        # 创建通讯特效
        for i in range(20):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(50, self.communication['transmission_range'])
            
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': 0,
                'vy': 0,
                'color': '#FFFF88',
                'size': 2,
                'life': 30,
                'type': 'signal'
            })
        
        self.log_data(f"广播: {message}")
    
    def start_crafting(self, blueprint_name):
        """开始制造"""
        if blueprint_name not in self.manufacturing['blueprints']:
            return
        
        blueprint = self.manufacturing['blueprints'][blueprint_name]
        
        # 检查材料
        for material, amount in blueprint.items():
            if material in self.attributes:
                if self.manufacturing['materials'][material] < amount:
                    self.log_data(f"材料不足: 需要{amount}{material}")
                    return
        
        # 消耗材料
        for material, amount in blueprint.items():
            if material in self.attributes:
                self.manufacturing['materials'][material] -= amount
        
        # 添加到制造队列
        if len(self.manufacturing['crafting_queue']) < 3:  # 队列限制
            self.manufacturing['crafting_queue'].append({
                'name': blueprint_name,
                'progress': 0,
                'total_time': blueprint.get('time', 5.0),
                'color': blueprint.get('color', '#FFFFFF')
            })
            
            self.log_data(f"开始制造: {blueprint_name}")
    
    def separate_unit(self, unit_type):
        """分离单位"""
        if unit_type not in self.separation_system['unit_types']:
            return
        
        if self.separation_system['separation_cooldown'] > 0:
            return
        
        if len(self.separation_system['deployed_units']) >= 5:  # 单位限制
            self.log_data("单位数量已达上限")
            return
        
        unit_data = self.separation_system['unit_types'][unit_type]
        
        unit = {
            'type': unit_type,
            'x': self.x,
            'y': self.y,
            'vx': math.cos(self.angle + math.pi) * 2,
            'vy': math.sin(self.angle + math.pi) * 2,
            'health': unit_data['health'],
            'max_health': unit_data['health'],
            'color': unit_data['color'],
            'size': 8,
            'abilities': unit_data['abilities'],
            'target': None,
            'state': 'following',
            'formation_offset': len(self.separation_system['deployed_units']) * 20
        }
        
        self.separation_system['deployed_units'].append(unit)
        self.separation_system['separation_cooldown'] = 60
        
        # 分离特效
        self.create_separation_effect()
        
        self.log_data(f"分离{unit_type}")
    
    def command_swarm(self, command):
        """命令集群"""
        if not self.separation_system['deployed_units']:
            return
        
        for unit in self.separation_system['deployed_units']:
            if command == 'gather':
                unit['state'] = 'following'
                unit['target'] = None
            elif command == 'defend':
                unit['state'] = 'defending'
                unit['target'] = (self.x, self.y)
            elif command == 'attack':
                # 寻找最近威胁
                nearest_threat = None
                min_distance = float('inf')
                
                for obj in self.scene_objects:
                    if obj['type'] == 'threat' and obj.get('detected', False):
                        dx = unit['x'] - obj['position'][0]
                        dy = unit['y'] - obj['position'][1]
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        if distance < min_distance:
                            min_distance = distance
                            nearest_threat = obj['position']
                
                if nearest_threat:
                    unit['state'] = 'attacking'
                    unit['target'] = nearest_threat
        
        self.log_data(f"集群命令: {command}")
    
    def reset_systems(self):
        """重置系统"""
        self.x, self.y = 600, 400
        self.trail_positions.clear()
        self.launch_system['energy'] = 100
        self.separation_system['deployed_units'].clear()
        self.swarm_system['swarm_units'].clear()
        
        # 重置场景物体
        for obj in self.scene_objects:
            if obj['type'] == 'resource':
                obj['collected'] = False
            elif obj['type'] == 'threat':
                obj['detected'] = False
        
        self.log_data("系统重置")
    
    def create_dash_particles(self):
        """创建冲刺粒子"""
        for _ in range(10):
            angle = self.angle + math.pi + random.uniform(-0.3, 0.3)
            speed = random.uniform(3, 6)
            
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice(['#FF5555', '#FFAA00']),
                'size': random.uniform(2, 4),
                'life': 15
            })
    
    def create_collection_effect(self, position):
        """创建收集特效"""
        x, y = position
        
        for _ in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 4)
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': '#88FF88',
                'size': random.uniform(2, 3),
                'life': 25
            })
    
    def create_launch_effect(self):
        """创建发射特效"""
        for _ in range(10):
            angle = self.angle + random.uniform(-0.2, 0.2)
            speed = random.uniform(1, 3)
            
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': '#FFAA00',
                'size': random.uniform(1, 2),
                'life': 20
            })
    
    def create_separation_effect(self):
        """创建分离特效"""
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': '#FF88FF',
                'size': random.uniform(1, 3),
                'life': 30
            })
    
    def log_data(self, message):
        """记录数据"""
        self.data_log.append({
            'time': time.time(),
            'message': message
        })
    
    def update_systems(self):
        """更新所有系统"""
        # 更新动画
        self.breath_phase += 0.1
        
        # 更新位置
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            move_speed = min(distance * 0.2, 5) + self.speed
            self.x += dx / distance * move_speed
            self.y += dy / distance * move_speed
        
        self.speed *= 0.9
        
        # 更新轨道
        self.trail_positions.append((self.x, self.y))
        
        # 更新粒子
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vx'] *= 0.97
            p['vy'] *= 0.97
            p['life'] -= 1
        
        self.particles = deque([p for p in self.particles if p['life'] > 0], maxlen=200)
        
        # 更新发射系统
        for proj in self.launch_system['projectiles']:
            proj['x'] += proj['vx']
            proj['y'] += proj['vy']
            proj['life'] -= 1
            
            # 碰撞检测
            for obj in self.scene_objects:
                if obj['type'] == 'threat':
                    dx = proj['x'] - obj['position'][0]
                    dy = proj['y'] - obj['position'][1]
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < obj['size'] + proj['size']:
                        obj['health'] -= proj['damage']
                        if obj['health'] <= 0:
                            obj['collected'] = True  # 标记为摧毁
                            self.log_data("目标摧毁")
                        proj['life'] = 0
                        break
        
        self.launch_system['projectiles'] = deque(
            [p for p in self.launch_system['projectiles'] if p['life'] > 0],
            maxlen=50
        )
        
        if self.launch_system['cooldown'] > 0:
            self.launch_system['cooldown'] -= 1
        if self.launch_system['energy'] < 100:
            self.launch_system['energy'] += 0.1
        
        # 更新分离单位
        for unit in self.separation_system['deployed_units']:
            if unit['state'] == 'following':
                # 跟随骑士
                dx = self.x - unit['x']
                dy = self.y - unit['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 40:
                    unit['vx'] = dx / distance * 2
                    unit['vy'] = dy / distance * 2
                else:
                    unit['vx'] *= 0.9
                    unit['vy'] *= 0.9
            elif unit['state'] == 'defending' and unit['target']:
                # 防御位置
                dx = unit['target'][0] - unit['x']
                dy = unit['target'][1] - unit['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 20:
                    unit['vx'] = dx / distance * 1.5
                    unit['vy'] = dy / distance * 1.5
                else:
                    unit['vx'] *= 0.9
                    unit['vy'] *= 0.9
            elif unit['state'] == 'attacking' and unit['target']:
                # 攻击目标
                dx = unit['target'][0] - unit['x']
                dy = unit['target'][1] - unit['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 10:
                    unit['vx'] = dx / distance * 2.5
                    unit['vy'] = dy / distance * 2.5
                else:
                    unit['vx'] *= 0.9
                    unit['vy'] *= 0.9
                    unit['target'] = None
                    unit['state'] = 'following'
            
            unit['x'] += unit['vx']
            unit['y'] += unit['vy']
        
        if self.separation_system['separation_cooldown'] > 0:
            self.separation_system['separation_cooldown'] -= 1
        
        # 更新制造系统
        for item in self.manufacturing['crafting_queue']:
            item['progress'] += 1 / 30.0  # 每帧增加
            if item['progress'] >= item['total_time']:
                # 制造完成
                self.manufacturing['crafted_items'].append(item)
                self.log_data(f"制造完成: {item['name']}")
        
        self.manufacturing['crafting_queue'] = [
            item for item in self.manufacturing['crafting_queue']
            if item['progress'] < item['total_time']
        ]
        
        # 更新资源重生
        for obj in self.scene_objects:
            if obj['type'] == 'resource' and obj.get('collected', False):
                obj['respawn_timer'] -= 1
                if obj['respawn_timer'] <= 0:
                    obj['collected'] = False
                    obj['value'] = random.randint(1, 3)
        
        # 更新扫描系统
        for p in self.detection_system['scan_particles']:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
        
        self.detection_system['scan_particles'] = deque(
            [p for p in self.detection_system['scan_particles'] if p['life'] > 0],
            maxlen=50
        )
        
        if self.detection_system['scan_cooldown'] > 0:
            self.detection_system['scan_cooldown'] -= 1
        
        # 边界检查
        self.check_boundaries()
    
    def check_boundaries(self):
        """边界检查"""
        x1, y1, x2, y2 = self.scene_boundary
        padding = 30
        
        if self.x < x1 + padding:
            self.x = x1 + padding
        elif self.x > x2 - padding:
            self.x = x2 - padding
        
        if self.y < y1 + padding:
            self.y = y1 + padding
        elif self.y > y2 - padding:
            self.y = y2 - padding
    
    def draw_background(self):
        """绘制背景"""
        # 边界
        x1, y1, x2, y2 = self.scene_boundary
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                    outline='#446688', width=3,
                                    dash=(5, 3))
        
        # 网格
        for x in range(x1, x2, 50):
            self.canvas.create_line(x, y1, x, y2, fill='#223344', width=1)
        for y in range(y1, y2, 50):
            self.canvas.create_line(x1, y, x2, y, fill='#223344', width=1)
        
        # 固定位置
        for pos in self.fixed_positions:
            self.canvas.create_oval(pos['x']-8, pos['y']-8,
                                   pos['x']+8, pos['y']+8,
                                   fill='#FF8888', outline='#FFFFFF')
            self.canvas.create_text(pos['x'], pos['y']-15,
                                   text=pos['type'], fill='#FF8888',
                                   font=('Arial', 8))
    
    def draw_scene_objects(self):
        """绘制场景物体"""
        for obj in self.scene_objects:
            x, y = obj['position']
            size = obj['size']
            color = obj['color']
            
            if obj['type'] == 'resource':
                if obj.get('collected', False):  # 修复这里！
                    # 已收集，显示残留
                    self.canvas.create_oval(x-size//2, y-size//2,
                                           x+size//2, y+size//2,
                                           fill='#444444', outline='#666666')
                    # 重生倒计时
                    if obj['respawn_timer'] > 0:
                        progress = 1 - obj['respawn_timer'] / 300
                        angle = progress * 360
                        self.canvas.create_arc(x-10, y-10, x+10, y+10,
                                              start=90, extent=-angle,
                                              outline=color, width=2)
                else:
                    # 资源水晶
                    pulse = math.sin(time.time() * 2) * 2
                    current_size = size + pulse
                    
                    self.canvas.create_polygon(
                        x, y-current_size,
                        x+current_size*0.866, y+current_size*0.5,
                        x-current_size*0.866, y+current_size*0.5,
                        fill=color, outline='#FFFFFF', width=1
                    )
                    
                    # 属性标签
                    attr = obj.get('attribute', '')
                    abbr = self.attributes.get(attr, {}).get('abbr', attr[:3])
                    self.canvas.create_text(x, y-current_size-10,
                                           text=abbr, fill=color,
                                           font=('Arial', 9, 'bold'))
                    
                    # 资源数量
                    self.canvas.create_text(x, y+current_size+10,
                                           text=f"x{obj['value']}",
                                           fill='#FFFFFF',
                                           font=('Arial', 8))
            
            elif obj['type'] == 'station':
                # 站点
                if obj['subtype'] == 'manufacturing':
                    # 制造站
                    self.canvas.create_rectangle(x-size, y-size, x+size, y+size,
                                                fill=color, outline='#FFFFFF', width=2)
                    self.canvas.create_text(x, y, text='M', fill='#000000',
                                           font=('Arial', 10, 'bold'))
                    
                    # 制造进度
                    if obj['active']:
                        self.canvas.create_line(x-15, y+size+5, x+15, y+size+5,
                                               fill='#8888FF', width=3)
                
                elif obj['subtype'] == 'communication':
                    # 通讯塔
                    self.canvas.create_polygon(
                        x, y-size,
                        x+size, y+size,
                        x-size, y+size,
                        fill=color, outline='#FFFFFF', width=2
                    )
                    self.canvas.create_text(x, y, text='C', fill='#000000',
                                           font=('Arial', 10, 'bold'))
                    
                    # 信号强度
                    strength = obj.get('signal_strength', 100)
                    for i in range(3):
                        if strength > i*33:
                            bar_height = 5 + i*3
                            self.canvas.create_rectangle(x-15+i*5, y+size+10,
                                                         x-12+i*5, y+size+10-bar_height,
                                                         fill='#FFFF88')
            
            elif obj['type'] == 'threat':
                # 威胁目标
                if obj.get('detected', False) or obj.get('collected', False):
                    # 被侦测或摧毁
                    if obj.get('collected', False):
                        # 摧毁状态
                        self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                               fill='#444444', outline='#666666')
                        self.canvas.create_line(x-size, y-size, x+size, y+size,
                                               fill='#FF0000', width=2)
                        self.canvas.create_line(x+size, y-size, x-size, y+size,
                                               fill='#FF0000', width=2)
                    else:
                        # 被侦测状态
                        self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                               fill=color, outline='#FFFFFF', width=2)
                        
                        # 健康条
                        health_ratio = obj['health'] / 100
                        bar_width = size * 2 * health_ratio
                        bar_color = '#FF0000' if health_ratio < 0.3 else '#FFAA00' if health_ratio < 0.6 else '#88FF88'
                        self.canvas.create_rectangle(x-size, y-size-8,
                                                     x-size+bar_width, y-size-5,
                                                     fill=bar_color)
                        
                        self.canvas.create_text(x, y-size-15,
                                               text='THREAT', fill=color,
                                               font=('Arial', 7, 'bold'))
                
                else:
                    # 未被侦测
                    self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                           fill='#444444', outline='#666666')
    
    def draw_knight(self):
        """绘制骑士"""
        # 基础身体
        body_size = 12
        self.canvas.create_oval(self.x-body_size, self.y-8,
                               self.x+body_size, self.y+8,
                               fill='#444444', outline='#666666', width=2)
        
        # 方向指示
        dx = math.cos(self.angle) * 20
        dy = math.sin(self.angle) * 20
        self.canvas.create_line(self.x, self.y, self.x+dx, self.y+dy,
                               fill='#00FFFF', width=2, arrow='last')
        
        # 装甲元素
        for elem in self.armor_elements:
            if elem['active']:
                ex = self.x + elem['position'][0]
                ey = self.y + elem['position'][1]
                ew, eh = elem['size']
                
                # 元素主体
                if elem['id'] in ['头盔', '左肩甲', '右肩甲']:
                    self.canvas.create_rectangle(ex-ew//2, ey-eh//2,
                                                ex+ew//2, ey+eh//2,
                                                fill=elem['color'], outline='#FFFFFF', width=1)
                else:
                    self.canvas.create_oval(ex-ew//2, ey-eh//2,
                                           ex+ew//2, ey+eh//2,
                                           fill=elem['color'], outline='#FFFFFF', width=1)
                
                # 能量显示
                energy_ratio = elem['energy'] / 100
                if energy_ratio < 0.3:
                    energy_color = '#FF5555'
                elif energy_ratio < 0.6:
                    energy_color = '#FFFF66'
                else:
                    energy_color = '#88FF88'
                
                self.canvas.create_rectangle(ex-ew//2, ey+eh//2+2,
                                            ex-ew//2+ew*energy_ratio, ey+eh//2+4,
                                            fill=energy_color)
        
        # 呼吸效果
        core_size = 8 + math.sin(self.breath_phase * 3) * 2
        self.canvas.create_oval(self.x-core_size, self.y-core_size,
                               self.x+core_size, self.y+core_size,
                               outline='#FF5555', width=2)
    
    def draw_trail(self):
        """绘制轨迹"""
        if len(self.trail_positions) < 2:
            return
        
        for i in range(len(self.trail_positions) - 1):
            alpha = i / len(self.trail_positions)
            width = 2 * (1 - alpha)
            
            x1, y1 = self.trail_positions[i]
            x2, y2 = self.trail_positions[i+1]
            
            # 速度相关颜色
            hue = (self.speed * 10 + i * 0.1) % 1.0
            r = int(255 * (0.5 + 0.5 * math.sin(hue * math.pi * 2)))
            g = int(255 * (0.5 + 0.5 * math.sin((hue + 0.333) * math.pi * 2)))
            b = int(255 * (0.5 + 0.5 * math.sin((hue + 0.667) * math.pi * 2)))
            color = f'#{r:02X}{g:02X}{b:02X}'
            
            self.canvas.create_line(x1, y1, x2, y2,
                                   fill=color, width=width,
                                   capstyle='round')
    
    def draw_particles(self):
        """绘制粒子"""
        for p in self.particles:
            life_ratio = p['life'] / 30
            size = p['size'] * life_ratio
            
            self.canvas.create_oval(p['x']-size, p['y']-size,
                                   p['x']+size, p['y']+size,
                                   fill=p['color'], outline='')
    
    def draw_projectiles(self):
        """绘制弹丸"""
        for proj in self.launch_system['projectiles']:
            size = proj['size']
            color = proj['color']
            
            self.canvas.create_oval(proj['x']-size, proj['y']-size,
                                   proj['x']+size, proj['y']+size,
                                   fill=color, outline='#FFFFFF', width=1)
            
            # 尾迹
            self.canvas.create_line(proj['x']-proj['vx']*2, proj['y']-proj['vy']*2,
                                   proj['x'], proj['y'],
                                   fill=color, width=1)
    
    def draw_units(self):
        """绘制分离单位"""
        for unit in self.separation_system['deployed_units']:
            size = unit['size']
            color = unit['color']
            
            # 单位主体
            if unit['type'] == '侦察机':
                # 三角形
                points = [
                    unit['x'], unit['y']-size,
                    unit['x']+size, unit['y']+size,
                    unit['x']-size, unit['y']+size
                ]
                self.canvas.create_polygon(points, fill=color, outline='#FFFFFF', width=1)
            else:
                # 圆形
                self.canvas.create_oval(unit['x']-size, unit['y']-size,
                                       unit['x']+size, unit['y']+size,
                                       fill=color, outline='#FFFFFF', width=1)
            
            # 状态指示
            if unit['state'] == 'attacking':
                self.canvas.create_text(unit['x'], unit['y']-size-10,
                                       text='⚔', fill='#FF5555',
                                       font=('Arial', 10))
            elif unit['state'] == 'defending':
                self.canvas.create_text(unit['x'], unit['y']-size-10,
                                       text='🛡', fill='#4488FF',
                                       font=('Arial', 10))
            
            # 健康条
            health_ratio = unit['health'] / unit['max_health']
            bar_width = size * 2 * health_ratio
            bar_color = '#FF0000' if health_ratio < 0.3 else '#FFAA00' if health_ratio < 0.6 else '#88FF88'
            self.canvas.create_rectangle(unit['x']-size, unit['y']-size-6,
                                         unit['x']-size+bar_width, unit['y']-size-3,
                                         fill=bar_color)
    
    def draw_scan_particles(self):
        """绘制扫描粒子"""
        for p in self.detection_system['scan_particles']:
            size = p['size'] * (p['life'] / 40)
            self.canvas.create_oval(p['x']-size, p['y']-size,
                                   p['x']+size, p['y']+size,
                                   fill=p['color'], outline='')
    
    def draw_ui(self):
        """绘制UI"""
        # 左侧：状态面板
        self.draw_status_panel()
        
        # 右侧：控制面板
        self.draw_control_panel()
        
        # 底部：制造面板
        self.draw_manufacturing_panel()
        
        # 顶部：通讯面板
        self.draw_communication_panel()
        
        # 数据日志
        self.draw_data_log()
    
    def draw_status_panel(self):
        """绘制状态面板"""
        x, y = 20, 20
        
        # 背景
        self.canvas.create_rectangle(x-10, y-10, x+200, y+180,
                                    fill='#112233', outline='#446688', width=2)
        
        # 标题
        self.canvas.create_text(x, y, text="系统状态",
                               fill='#88CCFF', font=('Arial', 12, 'bold'),
                               anchor='w')
        y += 25
        
        # 发射能量
        energy = self.launch_system['energy']
        self.canvas.create_rectangle(x, y, x+100, y+12,
                                    fill='#334455', outline='')
        self.canvas.create_rectangle(x, y, x+energy, y+12,
                                    fill='#FF5555', outline='')
        self.canvas.create_text(x, y+6, text="发射能量",
                               fill='#FFFFFF', font=('Arial', 8), anchor='w')
        self.canvas.create_text(x+110, y+6, text=f"{energy:.0f}/100",
                               fill='#FF5555', font=('Arial', 8))
        y += 20
        
        # 材料库存
        self.canvas.create_text(x, y, text="材料库存",
                               fill='#88CCFF', font=('Arial', 10, 'bold'),
                               anchor='w')
        y += 20
        
        for attr, data in self.attributes.items():
            amount = self.manufacturing['materials'].get(attr, 0)
            if amount > 0:
                abbr = data['abbr']
                self.canvas.create_text(x, y, text=f"{abbr}: {amount}",
                                       fill=data['color'], font=('Arial', 9),
                                       anchor='w')
                y += 16
        
        # 威胁等级
        if self.detection_system['threat_level'] > 0:
            y += 10
            threat_color = '#FF5555' if self.detection_system['threat_level'] > 50 else '#FFAA00'
            self.canvas.create_text(x, y, text=f"威胁等级: {self.detection_system['threat_level']}",
                                   fill=threat_color, font=('Arial', 10, 'bold'),
                                   anchor='w')
    
    def draw_control_panel(self):
        """绘制控制面板"""
        x, y = 980, 20
        
        # 背景
        self.canvas.create_rectangle(x-10, y-10, x+210, y+250,
                                    fill='#221133', outline='#8844CC', width=2)
        
        # 标题
        self.canvas.create_text(x+100, y, text="控制系统",
                               fill='#CC88FF', font=('Arial', 12, 'bold'))
        y += 25
        
        # 控制按钮
        controls = [
            ("发射能量弹 (左键)", "发射"),
            ("启动扫描 (右键)", "扫描"),
            ("通讯广播 (C)", "通讯"),
            ("制造物品 (M)", "制造"),
            ("分离单位 (D)", "分离"),
            ("集群集结 (S)", "集群"),
            ("切换阵型 (1-4)", "阵型"),
            ("系统重置 (R)", "重置")
        ]
        
        for i, (text, action) in enumerate(controls):
            btn_y = y + i * 28
            
            # 按钮背景
            color = '#88FF88' if action in ['发射', '扫描'] else '#88CCFF' if action in ['通讯', '制造'] else '#FF8888'
            self.canvas.create_rectangle(x, btn_y, x+180, btn_y+24,
                                        fill=color, outline='#FFFFFF', width=1)
            
            # 按钮文字
            self.canvas.create_text(x+90, btn_y+12, text=text,
                                   fill='#000000', font=('Arial', 9))
    
    def draw_manufacturing_panel(self):
        """绘制制造面板"""
        x, y = 20, 550
        
        # 背景
        self.canvas.create_rectangle(x-10, y-10, x+300, y+230,
                                    fill='#223311', outline='#668844', width=2)
        
        # 标题
        self.canvas.create_text(x, y, text="制造系统",
                               fill='#88FF88', font=('Arial', 12, 'bold'),
                               anchor='w')
        y += 25
        
        # 制造队列
        if self.manufacturing['crafting_queue']:
            self.canvas.create_text(x, y, text="制造队列:",
                                   fill='#88CCFF', font=('Arial', 10, 'bold'),
                                   anchor='w')
            y += 20
            
            for item in self.manufacturing['crafting_queue']:
                progress = item['progress'] / item['total_time']
                bar_width = 120 * progress
                
                self.canvas.create_rectangle(x, y, x+120, y+8,
                                            fill='#444444', outline='')
                self.canvas.create_rectangle(x, y, x+bar_width, y+8,
                                            fill=item['color'], outline='')
                
                self.canvas.create_text(x, y+10, text=item['name'],
                                       fill='#FFFFFF', font=('Arial', 9),
                                       anchor='w')
                
                percent = int(progress * 100)
                self.canvas.create_text(x+130, y+4, text=f"{percent}%",
                                       fill=item['color'], font=('Arial', 8))
                
                y += 25
        else:
            self.canvas.create_text(x, y, text="无制造项目",
                                   fill='#888888', font=('Arial', 10),
                                   anchor='w')
            y += 20
        
        # 蓝图列表
        y += 10
        self.canvas.create_text(x, y, text="可用蓝图:",
                               fill='#88CCFF', font=('Arial', 10, 'bold'),
                               anchor='w')
        y += 20
        
        blueprints = list(self.manufacturing['blueprints'].items())[:3]  # 显示前3个
        for name, blueprint in blueprints:
            # 检查材料是否足够
            can_craft = True
            for material, amount in blueprint.items():
                if material in self.attributes:
                    if self.manufacturing['materials'][material] < amount:
                        can_craft = False
                        break
            
            color = blueprint.get('color', '#FFFFFF')
            text_color = color if can_craft else '#888888'
            
            # 蓝图条目
            self.canvas.create_text(x, y, text=name,
                                   fill=text_color, font=('Arial', 9),
                                   anchor='w')
            
            # 材料需求
            mats_text = ""
            for material, amount in blueprint.items():
                if material in self.attributes:
                    mats_text += f"{material[:1]}{amount} "
            
            self.canvas.create_text(x+80, y, text=mats_text,
                                   fill=text_color, font=('Arial', 8))
            
            y += 18
    
    def draw_communication_panel(self):
        """绘制通讯面板"""
        x, y = 350, 20
        
        # 背景
        self.canvas.create_rectangle(x-10, y-10, x+300, y+120,
                                    fill='#332211', outline='#CC9966', width=2)
        
        # 标题
        self.canvas.create_text(x, y, text="通讯系统",
                               fill='#FFCC88', font=('Arial', 12, 'bold'),
                               anchor='w')
        y += 25
        
        # 最近消息
        if self.communication['messages']:
            last_msg = list(self.communication['messages'])[-1]
            msg_text = f"{last_msg['sender']}: {last_msg['message']}"
            
            # 限制长度
            if len(msg_text) > 30:
                msg_text = msg_text[:27] + "..."
            
            self.canvas.create_text(x, y, text=msg_text,
                                   fill='#FFFF88', font=('Arial', 10),
                                   anchor='w')
            y += 20
            
            # 信号强度
            strength = self.communication['signal_strength']
            self.canvas.create_rectangle(x, y, x+100, y+8,
                                        fill='#444444', outline='')
            self.canvas.create_rectangle(x, y, x+strength, y+8,
                                        fill='#FFFF88', outline='')
            self.canvas.create_text(x+110, y+4, text=f"{strength}%",
                                   fill='#FFFF88', font=('Arial', 8))
        else:
            self.canvas.create_text(x, y, text="无通讯消息",
                                   fill='#888888', font=('Arial', 10),
                                   anchor='w')
    
    def draw_data_log(self):
        """绘制数据日志"""
        x, y = 350, 150
        
        # 背景
        self.canvas.create_rectangle(x-10, y-10, x+300, y+100,
                                    fill='#111122', outline='#446688', width=2)
        
        # 标题
        self.canvas.create_text(x, y, text="数据日志",
                               fill='#88CCFF', font=('Arial', 12, 'bold'),
                               anchor='w')
        y += 25
        
        # 最近日志
        recent_logs = list(self.data_log)[-3:]  # 显示最近3条
        for i, log in enumerate(recent_logs):
            log_text = log['message']
            if len(log_text) > 25:
                log_text = log_text[:22] + "..."
            
            self.canvas.create_text(x, y + i*20, text=log_text,
                                   fill='#FFFFFF', font=('Arial', 9),
                                   anchor='w')
    
    def animate(self):
        """主动画循环"""
        try:
            # 更新系统
            self.update_systems()
            
            # 清除画布
            self.canvas.delete("all")
            
            # 绘制所有内容
            self.draw_background()
            self.draw_scene_objects()
            self.draw_trail()
            self.draw_particles()
            self.draw_scan_particles()
            self.draw_projectiles()
            self.draw_units()
            self.draw_knight()
            self.draw_ui()
            
            # 继续动画
            self.window.after(30, self.animate)
        except Exception as e:
            print(f"动画错误: {e}")
            # 继续动画以防止程序崩溃
            self.window.after(30, self.animate)

# 运行程序
if __name__ == "__main__":
    try:
        app = UltimatePixelKnightV3()
    except Exception as e:
        print(f"启动错误: {e}")
        import traceback
        traceback.print_exc()
