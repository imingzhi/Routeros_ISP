import requests
import time

# 数据源配置
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

def generate_isp_rsc():
    filename = "ISP.rsc"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 获取当前北京时间
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    print(f"[{update_time}] 开始生成合并文件...")

    # 使用 Session 提高效率
    session = requests.Session()
    session.headers.update(headers)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 1. 写入文件注释头
            f.write(f"# Generated on {update_time}\n")
            f.write("# This script will auto-remove old entries and add new ones\n\n")
            
            # 2. 写入主指令
            f.write("/ip firewall address-list\n")
            
            total_count = 0
            
            for list_name, info in ISP_DATA.items():
                print(f"正在抓取 {info['comment']}...")
                try:
                    response = session.get(info['url'], timeout=20)
                    response.raise_for_status()
                    
                    ips = [line.strip() for line in response.text.split('\n') if line.strip()]
                    
                    if not ips:
                        print(f"⚠️ 警告: {info['comment']} 获取的数据为空，跳过该运营商。")
                        continue
                        
                    # 写入该运营商的清理指令
                    f.write(f"\n# --- {info['comment']} START ---\n")
                    f.write(f"remove [find list=\"{list_name}\"]\n")
                    
                    # 批量写入添加指令
                    for ip in ips:
                        f.write(f"add list=\"{list_name}\" address={ip} comment=\"{info['comment']}\"\n")
                    
                    count = len(ips)
                    total_count += count
                    print(f"✅ {info['comment']} 完成: {count} 条条目。")
                    
                except Exception as e:
                    print(f"❌ {info['comment']} 抓取失败: {e}")
            
            f.write(f"\n# Total entries: {total_count}\n")
            print(f"\n✨ 生成成功！总条目: {total_count}。文件: {filename}")

    except Exception as e:
        print(f"🔥 写入文件时发生致命错误: {e}")

if __name__ == "__main__":
    generate_isp_rsc()
