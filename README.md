# Alwaysdata 每月随机自动续期

自动登录 Alwaysdata 面板完成续期，并在每次运行成功后将下个月的触发时间随机写回工作流文件，避免固定时间被检测。

---

## 变量配置

所有变量均在仓库的 **Settings → Secrets and variables → Actions → Secrets** 中添加。

| 变量名 | 必填 | 说明 |
|---|---|---|
| `ALWAYSDATA_USER` | ✅ | Alwaysdata 登录用户名（邮箱） |
| `ALWAYSDATA_PASS` | ✅ | Alwaysdata 登录密码 |
| `TG_BOT_TOKEN` | ❌ | Telegram Bot Token，用于运行结果通知，不填则跳过通知 |
| `TG_CHAT_ID` | ❌ | Telegram Chat ID，与 `TG_BOT_TOKEN` 配套使用 |
| `REPO_TOKEN` | ❌ |  |


---

## 必填项说明

### `ALWAYSDATA_USER`

Alwaysdata 账号的登录邮箱。

```
example@gmail.com
```

### `ALWAYSDATA_PASS`

Alwaysdata 账号的登录密码，明文填入 Secret 即可，GitHub 会自动加密存储。

---

## 可选项说明

### `TG_BOT_TOKEN` 和 `TG_CHAT_ID`

用于在续期成功或失败后向 Telegram 发送通知。两个变量需要同时填写才能生效，缺少任意一个则不发送通知。

获取方式：

1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)，发送 `/newbot` 创建 Bot，获得 `TG_BOT_TOKEN`
2. 向 [@userinfobot](https://t.me/userinfobot) 发送任意消息，获得自己的 `TG_CHAT_ID`

---

## 权限要求

工作流需要以下仓库权限（已在 `workflow` 文件顶部声明，无需手动操作）：

```yaml
permissions:
  contents: write   # 用于将随机 Cron 写回工作流文件
  actions: write    # 用于触发工作流
```

如果仓库设置了 **Actions 写权限限制**，需前往 **Settings → Actions → General → Workflow permissions**，选择 **Read and write permissions**。

---

## 运行方式

- **自动运行**：每月按工作流文件中的随机 Cron 时间触发，每次运行后自动更新下月时间
- **手动运行**：进入仓库 **Actions** 页面，选择该工作流，点击 **Run workflow**
