# 手柄震动联动 / Rumble Shock

**语言 / Language：** [中文](#-中文版本) | [English](#-english-version)

---

## 中文版本

> 手柄一震动，郊狼就放电。

通过监听游戏经 **XInput** 发送给手柄的震动信号，实时联动 DGHub，驱动 DG-Lab 设备输出，实现沉浸式反馈。

### 插件简介

本插件会挂钩游戏进程中的 `XInputSetState`，实时获取左右马达震动强度，并按你配置的规则映射为电击强度与波形，通过 DGHub 发送给已连接的 DG-Lab 设备。

**一句话效果：**  
游戏手柄震动 → 插件检测 → DGHub 触发 → 郊狼放电。

### 快速开始

#### 1. 下载与解压

本项目采用分卷压缩上传，请下载以下文件并放在同一文件夹：

- `手柄震动联动.7z.001`
- `手柄震动联动.7z.002`
- `手柄震动联动.7z.003`

使用常见压缩软件（7-Zip、Bandizip、WinRAR 等）解压即可。

> 如果解压遇到问题，可使用附带的 `手柄震动联动.exe` 解压程序辅助解压。

#### 2. 导入插件

解压完成后，找到 **`main.zip`**（插件本体），打开 **DGHub** → 插件中心 → 外部插件 → 导入该 zip 即可。

#### 3. 基本配置

1. 在插件配置页填写要监听的**游戏进程名**
2. 确认游戏使用 **XInput** 手柄输入
3. **禁用 Steam 输入**（重要）
4. 选择输出通道、强度模式、波形预设等参数

> 配置如遇问题，请优先查看 DGHub **运行日志**，确认无报错后再重启插件。  
> **注意：插件运行时无法修改配置，请先停止插件再调整。**

### 兼容说明

- 理论上支持所有通过 **XInput** 控制手柄震动的游戏
- 实际兼容性因游戏实现而异，需自行验证
- 必须使用支持 XInput 的手柄，并关闭 Steam Input

#### 已验证兼容游戏

| 游戏 | 进程名 |
|------|--------|
| 星际拓荒 (Outer Wilds) | `OuterWilds.exe` |
| 死亡搁浅 导演剪辑版 | `ds.exe` |

> 若以上游戏使用时无效果，请检查：  
> 1. 进程名是否填写正确  
> 2. 是否已禁用 Steam 输入  
> 3. 手柄是否走 XInput

### 前置软件

| 软件 | 说明 | 链接 |
|------|------|------|
| **DGHub** | 插件运行与设备控制中枢 | [http://www.dghub.top/](http://www.dghub.top/) |
| **DG-Lab** | 官方设备与生态 | [https://dungeon-lab.cn/](https://dungeon-lab.cn/) |

### 主要功能

- 实时监听 XInput 手柄震动
- 支持 A / B / 双通道输出
- 可配置强度映射、冷却、持续时间
- 支持强度回落 / 永久叠加模式
- 运行日志中文输出，方便排查
- 支持自定义波形预设

### 注意事项

1. 请通过 DGHub 启动本插件，不要单独运行 exe
2. 修改进程名后建议重启插件
3. 插件运行期间请勿修改配置
4. 本插件仅做本地信号映射，不修改游戏文件

### 源码说明

本插件源代码位于 **源代码分支**。  
**使用插件无需下载源码。**

请转到最新版本对应分支下载正式发布包。

### 免责声明

本插件仅供学习与个人娱乐使用。  
请确保在合法、安全的前提下使用相关设备，注意电流强度与使用时长，避免意外伤害。

---

**[回到顶部](#手柄震动联动--rumble-shock)** · [切换到 English](#-english-version)

---

## English Version

> Controller rumbles → Coyote shocks.

This plugin hooks the game’s XInput vibration calls, maps rumble intensity in real time, and triggers DG-Lab devices through DGHub.

### Introduction

The plugin intercepts `XInputSetState` in the target game process, reads left/right motor intensity, converts it according to your settings, and sends trigger commands to DGHub.

**One-line summary:**  
Game controller rumble → Plugin detects → DGHub triggers → Device output.

### Quick Start

#### 1. Download & Extract

This project is uploaded as a split archive. Please download all parts and put them in the same folder:

- `手柄震动联动.7z.001`
- `手柄震动联动.7z.002`
- `手柄震动联动.7z.003`

Extract with 7-Zip, Bandizip, WinRAR, or similar tools.

> If extraction fails, use the included `手柄震动联动.exe` helper.

#### 2. Import Plugin

After extraction, locate **`main.zip`** (the plugin package).  
Open **DGHub** → Plugin Center → External Plugins → Import the zip.

#### 3. Basic Setup

1. Enter the target **game process name** in the plugin settings
2. Make sure the game uses **XInput**
3. **Disable Steam Input** (important)
4. Configure channel, strength mode, preset, etc.

> If something goes wrong, check the DGHub **runtime log** first, then restart the plugin.  
> **Note: Settings cannot be changed while the plugin is running. Stop it before editing.**

### Compatibility

- In theory, any game that drives controller rumble via **XInput** is supported
- Real-world compatibility varies by game implementation
- Use an XInput-compatible controller and disable Steam Input

#### Verified Games

| Game | Process |
|------|---------|
| Outer Wilds | `OuterWilds.exe` |
| Death Stranding Director's Cut | `ds.exe` |

> If these games don’t work, please check:  
> 1. Process name is correct  
> 2. Steam Input is disabled  
> 3. Controller is using XInput

### Requirements

| Software | Description | Link |
|----------|-------------|------|
| **DGHub** | Plugin host & device control | [http://www.dghub.top/](http://www.dghub.top/) |
| **DG-Lab** | Official devices & ecosystem | [https://dungeon-lab.cn/](https://dungeon-lab.cn/) |

### Features

- Real-time XInput rumble monitoring
- A / B / Both channel output
- Configurable intensity mapping, cooldown, duration
- Rollback / Permanent strength modes
- Chinese runtime logs for easier debugging
- Custom waveform presets

### Notes

1. Always start the plugin via DGHub; do not run the exe directly
2. Restart the plugin after changing the process name
3. Do not change settings while the plugin is running
4. This plugin only maps signals locally and does not modify game files

### Source Code

Source code is available on the **source branch**.  
**You do not need the source code to use the plugin.**

Please switch to the latest release branch to download the official package.

### Disclaimer

This plugin is for learning and personal entertainment only.  
Use related devices legally and safely. Mind intensity and duration to avoid injury.

---

**[Back to top](#手柄震动联动--rumble-shock)** · [切换到 中文](#-中文版本)

---

**手柄震动联动 / Rumble Shock**  
让每一次震动都有反馈 · Every rumble deserves feedback