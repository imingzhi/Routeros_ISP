import requests

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

def generate_combined_rsc():
    filename = "ISP.rsc"
    print(f"开始生成合并文件: {filename}")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 1. 写入脚本头部（整个文件只需要一行）
            f.write("/ip firewall address-list\n")
            
            # 2. 遍历每个运营商
            for list_name, info in ISP_DATA.items():
                print(f"正在获取 {info['comment']} 的数据...")
                try:
                    response = requests.get(info['url'], timeout=30)
                    response.raise_for_status()
                    ips = response.text.strip().split('\n')
                    
                    # 3. 先写入删除该运营商旧数据的命令，确保不重复
                    f.write(f"remove [find list=\"{list_name}\"]\n")
                    
                    # 4. 逐行写入 IP 条目
                    count = 0
                    for ip in ips:
                        ip = ip.strip()
                        if ip:
                            f.write(f"add list=\"{list_name}\" address={ip} comment=\"{info['comment']}\"\n")
                            count += 1
                    print(f"✅ {info['comment']} 处理完成，共 {count} 条。")
                    
                except Exception as e:
                    print(f"❌ 获取 {info['comment']} 失败: {e}")
                    
        print(f"\n✨ 所有数据已成功整合至 {filename}")

    except Exception as e:
        print(f"❌ 写入文件时发生致命错误: {e}")

if __name__ == "__main__":
    generate_combined_rsc()
