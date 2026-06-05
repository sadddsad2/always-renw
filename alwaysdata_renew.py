#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
from bs4 import BeautifulSoup

def send_telegram_notification(token, chat_id, message):
    """发送通知到 Telegram Bot"""
    if not token or not chat_id:
        print("⚠️ 未配置 Telegram Token 或 Chat ID，跳过发送电报消息。")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("🚀 电报通知发送成功！")
        else:
            print(f"❌ 电报通知发送失败，状态码: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print(f"💥 发送电报通知时发生异常: {e}")

def alwaysdata_login_api(username, password):
    if not username or not password:
        print("❌ 错误：未配置 Alwaysdata 的账号或密码环境变量！")
        return False

    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,ja-JP;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://admin.alwaysdata.com/login/',
        'Origin': 'https://admin.alwaysdata.com'
    }
    session.headers.update(headers)

    login_url = "https://admin.alwaysdata.com/login/"

    try:
        print("🔄 正在获取 Alwaysdata 登录页 Token...")
        response = session.get(login_url, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if not csrf_token_input:
            print("❌ 未能在页面中找到 csrfmiddlewaretoken。")
            return False
            
        csrf_token = csrf_token_input.get('value')
        print(f"🔑 成功提取 Token: {csrf_token[:8]}...")

        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'login': username,
            'password': password,
            'alive': 'on'
        }

        print("🚀 正在发送 POST 登录请求...")
        login_response = session.post(login_url, data=payload, timeout=15)

        if "sessionid" in session.cookies.get_dict():
            print("✅ Alwaysdata 登录/续期成功！会话已刷新。")
            return True
        else:
            print("❌ 登录失败：未成功获取 sessionid。")
            return False

    except Exception as e:
        print(f"💥 运行期间发生异常: {e}")
        return False

if __name__ == "__main__":
    # 从 GitHub Actions 环境变量中读取凭证
    ALWAYSDATA_USER = os.getenv("ALWAYSDATA_USER")
    ALWAYSDATA_PASS = os.getenv("ALWAYSDATA_PASS")
    
    # 读取 Telegram 配置
    TG_TOKEN = os.getenv("TG_BOT_TOKEN")
    TG_ID = os.getenv("TG_CHAT_ID")
    
    # 隐藏邮箱中间部分，防止日志及电报消息泄露隐私
    masked_user = f"{ALWAYSDATA_USER[:3]}***{ALWAYSDATA_USER[ALWAYSDATA_USER.find('@'):]}" if ALWAYSDATA_USER else "未知账号"

    success = alwaysdata_login_api(ALWAYSDATA_USER, ALWAYSDATA_PASS)
    
    # 根据结果组装电报消息
    if success:
        tg_msg = f"🔔 *Alwaysdata 自动续期通知*\n\n👤 *账号:* `{masked_user}`\n📊 *状态:* ✅ 成功维护登录会话\n⚙️ *运行环境:* GitHub Actions"
        send_telegram_notification(TG_TOKEN, TG_ID, tg_msg)
    else:
        tg_msg = f"🚨 *Alwaysdata 自动续期失败*\n\n👤 *账号:* `{masked_user}`\n📊 *状态:* ❌ 登录失败/Cookie获取异常\n⚠️ *请及时检查 GitHub Actions 运行日志！*"
        send_telegram_notification(TG_TOKEN, TG_ID, tg_msg)
        sys.exit(1) # 如果失败，让 GitHub Actions 报错