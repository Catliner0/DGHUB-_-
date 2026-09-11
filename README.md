# 手柄震动联动 / Rumble Shock

> 手柄一震动，郊狼就放电。  
> Controller rumbles → Coyote shocks.

通过监听游戏经 **XInput** 发送给手柄的震动信号，实时联动 DGHub，驱动 DG-Lab 设备输出，实现沉浸式反馈。

This plugin hooks the game’s XInput vibration calls, maps rumble intensity in real time, and triggers DG-Lab devices through DGHub.

---

## 插件简介 / Introduction

本插件会挂钩游戏进程中的 `XInputSetState`，实时获取左右马达震动强度，并按你配置的规则映射为电击强度与波形，通过 DGHub 发送给已连接的 DG-Lab 设备。

The plugin intercepts `XInputSetState` in the target game process, reads left/right motor intensity, converts it according to your settings, and sends trigger commands to DGHub.

**一句话效果 / One-line summary：**  
游戏手柄震动 → 插件检测 → DGHub 触发 → 郊狼放电。  
Game controller rumble → Plugin detects → DGHub triggers → Device output.

---

## 快速开始 / Quick Start

### 1. 下载与解压 / Download & Extract

本项目采用分卷压缩上传，请下载以下文件并放在同一文件夹：

Please download all parts and put them in the same folder:

- `手柄震动联动.7z.001`
- `手柄震动联动.7z.002`
- `手柄震动联动.7z.003`

使用常见压缩软件（7-Zip、Bandizip、WinRAR 等）解压即可。

Extract with 7-Zip, Bandizip, WinRAR, or similar tools.

> 如果解压遇到问题，可使用附带的 `手柄震动联动.exe` 解压程序辅助解压。  
> If extraction fails, use the included `手柄震动联动.exe` helper.

### 2. 导入插件 / Import Plugin

解压完成后，找到 **`main.zip`**（插件本体），打开 **DGHub** → 插件中心 → 外部插件 → 导入该 zip。

After extraction, locate **`main.zip`** (the plugin package). Open **DGHub** → Plugin Center → External Plugins → Import the zip.

### 3. 基本配置 / Basic Setup

1. 在插件配置页填写要监听的**游戏进程名**  
   Enter the target **game process name** in the plugin settings.
2. 确认游戏使用 **XInput** 手柄输入  
   Make sure the game uses **XInput**.
3. **禁用 Steam 输入**（重要）  
   **Disable Steam Input** (important).
4. 选择输出通道、强度模式、波形预设等参数  
   Configure channel, strength mode, preset, etc.

> 配置如遇问题，请优先查看 DGHub **运行日志**，确认无报错后再重启插件。  
> If something goes wrong, check the DGHub **runtime log** first, then restart the plugin.  
>  
> **注意：插件运行时无法修改配置，请先停止插件再调整。**  
> **Note: Settings cannot be changed while the plugin is running. Stop it before editing.**

---

## 兼容说明 / Compatibility

- 理论上支持所有通过 **XInput** 控制手柄震动的游戏  
  In theory, any game that drives controller rumble via **XInput** is supported.
- 实际兼容性因游戏实现而异，需自行验证  
  Real-world compatibility varies by game implementation.
- 必须使用支持 XInput 的手柄，并关闭 Steam Input  
  Use an XInput-compatible controller and disable Steam Input.

### 已验证兼容游戏 / Verified Games

| 游戏 / Game | 进程名 / Process |
|-------------|------------------|
| 星际拓荒 (Outer Wilds) | `OuterWilds.exe` |
| 死亡搁浅 导演剪辑版 (Death Stranding Director's Cut) | `ds.exe` |

> 若以上游戏使用时无效果，请检查：  
> If these games don’t work, please check:  
> 1. 进程名是否填写正确 / Process name is correct  
> 2. 是否已禁用 Steam 输入 / Steam Input is disabled  
> 3. 手柄是否走 XInput / Controller is using XInput

---

## 前置软件 / Requirements

| 软件 / Software | 说明 / Description | 链接 / Link |
|-----------------|--------------------|-------------|
| **DGHub** | 插件运行与设备控制中枢<br>Plugin host & device control | [http://www.dghub.top/](http://www.dghub.top/) |
| **DG-Lab** | 官方设备与生态<br>Official devices & ecosystem | [https://dungeon-lab.cn/](https://dungeon-lab.cn/) |

---

## 主要功能 / Features

- 实时监听 XInput 手柄震动  
  Real-time XInput rumble monitoring
- 支持 A / B / 双通道输出  
  A / B / Both channel output
- 可配置强度映射、冷却、持续时间  
  Configurable intensity mapping, cooldown, duration
- 支持强度回落 / 永久叠加模式  
  Rollback / Permanent strength modes
- 运行日志中文输出，方便排查  
  Chinese runtime logs for easier debugging
- 支持自定义波形预设  
  Custom waveform presets

---

## 注意事项 / Notes

1. 请通过 DGHub 启动本插件，不要单独运行 exe  
   Always start the plugin via DGHub; do not run the exe directly.
2. 修改进程名后建议重启插件  
   Restart the plugin after changing the process name.
3. 插件运行期间请勿修改配置  
   Do not change settings while the plugin is running.
4. 本插件仅做本地信号映射，不修改游戏文件  
   This plugin only maps signals locally and does not modify game files.

---

## 源码说明 / Source Code

本插件源代码位于 **源代码分支**。  
Source code is available on the **source branch**.

**使用插件无需下载源码。**  
**You do not need the source code to use the plugin.**

请转到最新版本对应分支下载正式发布包。  
Please switch to the latest release branch to download the official package.

---

## 免责声明 / Disclaimer

本插件仅供学习与个人娱乐使用。  
This plugin is for learning and personal entertainment only.

请确保在合法、安全的前提下使用相关设备，注意电流强度与使用时长，避免意外伤害。  
Use related devices legally and safely. Mind intensity and duration to avoid injury.

---

**手柄震动联动 / Rumble Shock**  
让每一次震动都有反馈 · Every rumble deserves feedback