import requests
import os

# 你提供的最新数据源
ISP_DATA = {
    "ISP_Telecom": {
        "url": "https://metowolf.github.io/iplist/data/isp/chinatelecom.txt",
        "comment": "中国电信"
    },
    "ISP_Unicom": {
        "url": "https://metowolf.github.io/iplist/data/isp/chinaunicom.txt",
        "comment": "中国联通"
    },
    "ISP_Mobile": {
        "url": "https://metowolf.github.io/iplist/data/isp/chinamobile.txt",
        "comment": "中国移动"
    }
}

def generate_rsc():
    for list_name, info in ISP_DATA.items():
        try:
            print(f"正在从 {info['url']} 获取 {info['comment']} 数据...")
            # 增加 timeout 防止网络僵死
            response = requests.get(info['url'], timeout=30)
            response.raise_for_status()
            
            ips = response.text.strip().split('\n')
            filename = f"{list_name}.rsc"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # 写入 ROS 脚本头部
                f.write("/ip firewall address-list\n")
                # 清理旧数据，防止重复。注意：这里 list 名称使用的是 ISP_Telecom 等。
                f.write(f"remove [find list=\"{list_name}\"]\n")
                
                for ip in ips:
                    ip = ip.strip()
                    if ip:
                        # 格式示例：add list=ISP_Telecom address=1.2.3.4 comment="中国电信"
                        f.write(f"add list=\"{list_name}\" address={ip} comment=\"{info['comment']}\"\n")
            
            print(f"✅ 成功生成 {filename}，共计 {len(ips)} 条网段。")
            
        except Exception as e:
            print(f"❌ 处理 {list_name} 时发生错误: {e}")

if __name__ == "__main__":
    generate_rsc()
