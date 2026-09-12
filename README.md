# 🎮 手柄震动映射 · Rumble Shock

> 手柄一震动，郊狼就放电。
>
> Controller rumbles → Coyote shocks.

通过监听游戏经 **XInput** 发送给手柄的震动信号，实时联动 **DGHub**，驱动 **DG-Lab** 设备输出，实现沉浸式反馈。

This plugin hooks the game's XInput vibration calls, maps rumble intensity in real time, and triggers DG-Lab devices through DGHub.

---

## 📖 插件简介 · Introduction

本插件会挂钩游戏进程中的 `XInputSetState`，实时获取左右马达震动强度，并按你配置的规则映射为电击强度与波形，通过 DGHub 发送给已连接的 DG-Lab 设备。

The plugin intercepts `XInputSetState` in the target game process, reads left/right motor intensity, converts it according to your settings, and sends trigger commands to DGHub.

**一句话效果 · One-line summary：**

> 游戏手柄震动 → 插件检测 → DGHub 触发 → 郊狼放电
>
> Game controller rumble → Plugin detects → DGHub triggers → Device output.

---

## 🚀 快速开始 · Quick Start

### 1. 下载与解压 · Download & Extract

本项目采用分卷压缩上传，请下载以下文件并放在**同一文件夹**：

Please download **all parts** and put them in the **same folder**:

```
手柄震动联动.7z.001
手柄震动联动.7z.002
手柄震动联动.7z.003
```

使用常见压缩软件（7-Zip、Bandizip、WinRAR 等）解压即可。如果解压遇到问题，可使用附带的 `手柄震动联动.exe` 解压程序辅助解压。

Extract with 7-Zip, Bandizip, WinRAR, or similar tools. If extraction fails, use the included `手柄震动联动.exe` helper.

### 2. 导入插件 · Import Plugin

解压完成后，找到 `main.zip`（插件本体），打开 **DGHub → 插件中心 → 外部插件 → 导入该 zip**。

After extraction, locate `main.zip` (the plugin package). Open **DGHub → Plugin Center → External Plugins → Import the zip**.

### 3. 基本配置 · Basic Setup

1. 在插件配置页填写要监听的游戏进程名
   Enter the target game process name in the plugin settings.
2. 确认游戏使用 XInput 手柄输入
   Make sure the game uses XInput.
3. **禁用 Steam 输入（重要）**
   **Disable Steam Input (important).**
4. 选择输出通道、强度模式、波形预设等参数
   Configure channel, strength mode, preset, etc.

> ⚠️ 配置如遇问题，请优先查看 DGHub 运行日志，确认无报错后再重启插件。
> If something goes wrong, check the DGHub runtime log first, then restart the plugin.

> ⚠️ **插件运行时无法修改配置，请先停止插件再调整。**
> Settings cannot be changed while the plugin is running. Stop it before editing.

---

## 🧩 兼容说明 · Compatibility

- 理论上支持所有通过 XInput 控制手柄震动的游戏
  *In theory, any game that drives controller rumble via XInput is supported.*
- 实际兼容性因游戏实现而异，需自行验证
  *Real-world compatibility varies by game implementation.*
- 必须使用支持 XInput 的手柄，并关闭 Steam Input
  *Use an XInput-compatible controller and disable Steam Input.*

### ✅ 已验证兼容游戏 · Verified Games

| 游戏 · Game | 进程名 · Process |
| :--- | :--- |
| 星际拓荒 (Outer Wilds) | `OuterWilds.exe` |
| 死亡搁浅 导演剪辑版 (Death Stranding Director's Cut) | `ds.exe` |

若以上游戏使用时无效果，请检查：

If these games don't work, please check:

- [ ] 进程名是否填写正确 · Process name is correct
- [ ] 是否已禁用 Steam 输入 · Steam Input is disabled
- [ ] 手柄是否走 XInput · Controller is using XInput

---

## 🛠️ 前置软件 · Requirements

| 软件 · Software | 说明 · Description | 链接 · Link |
| :--- | :--- | :--- |
| **DGHub** | 插件运行与设备控制中枢 · Plugin host & device control | [dghub.top](http://www.dghub.top/) |
| **DG-Lab** | 官方设备与生态 · Official devices & ecosystem | [dungeon-lab.cn](https://dungeon-lab.cn/) |

---

## ✨ 主要功能 · Features

- 🎮 实时监听 XInput 手柄震动
  *Real-time XInput rumble monitoring*
- 📡 支持 A / B / 双通道输出
  *A / B / Both channel output*
- ⚙️ 可配置强度映射、冷却、持续时间
  *Configurable intensity mapping, cooldown, duration*
- 🔁 支持强度回落 / 永久叠加模式
  *Rollback / Permanent strength modes*
- 📝 运行日志中文输出，方便排查
  *Chinese runtime logs for easier debugging*
- 🌊 支持自定义波形预设
  *Custom waveform presets*

---

## 📜 更新日志 · Changelog

### v1.6.0（最新 · Latest）

- 正式将插件中文名称更改为「手柄震动映射」
  *Officially renamed the Chinese plugin name to "手柄震动映射" (Rumble Shock).*
- 更改了启动插件仅会尝试搜索一次进程的效果，现在插件每隔一段时间就会再次尝试搜索进程
  *Changed the one-time process search on startup; now the plugin periodically retries searching for the process.*
- 新增搜索进程功能，帮助你寻找游戏进程名（该功能目前不稳定，仍在测试中）
  *Added a process search feature to help find the game process name (still unstable and in testing).*

### v1.5.0

- 支持双通道切换
  *Added dual-channel switching support.*
- 更加详细的配置项目
  *More detailed configuration options.*
- 完善了 DGHub 运行日志
  *Improved DGHub runtime logs.*

### v1.2.5

- 修复了配置信息无法生效 / 无效的 Bug
  *Fixed a bug where configuration settings were not taking effect.*
- 增加了 DGHub 软件内的运行日志支持
  *Added runtime log support within DGHub.*

### v1.2.0（正式版 · Official Release）

- 支持获取 XInput 向手柄发送的震动信息来联动 DG-Lab 设备
  *Added support for capturing XInput vibration signals to trigger DG-Lab devices.*

### v1.0（测试版 · Beta）

- 可以与 DGHub 握手并控制 DG-Lab 设备
  *Initial handshake with DGHub and basic DG-Lab device control.*

---

## ⚠️ 注意事项 · Notes

- ❌ 请通过 DGHub 启动本插件，**不要单独运行 exe**
  *Always start the plugin via DGHub; do not run the exe directly.*
- 🔄 修改进程名后建议重启插件
  *Restart the plugin after changing the process name.*
- ⏹️ 插件运行期间请勿修改配置
  *Do not change settings while the plugin is running.*
- 🔒 本插件仅做本地信号映射，**不修改游戏文件**
  *This plugin only maps signals locally and does not modify game files.*

---

## 📜 源码说明 · Source Code

本插件源代码位于 `源代码` 分支。使用插件无需下载源码。请转到**最新版本对应分支**下载正式发布包。

Source code is available on the `source` branch. You do not need the source code to use the plugin. Please switch to the **latest release branch** to download the official package.

---

## ⚖️ 免责声明 · Disclaimer

本插件仅供学习与个人娱乐使用。请确保在合法、安全的前提下使用相关设备，注意电流强度与使用时长，避免意外伤害。

This plugin is for learning and personal entertainment only. Use related devices legally and safely. Mind intensity and duration to avoid injury.

---

<p align="center">
  <b>手柄震动映射 · Rumble Shock</b><br>
  让每一次震动都有反馈 · Every rumble deserves feedback
</p>
