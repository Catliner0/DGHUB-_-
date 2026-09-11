import asyncio
import json
import os
import time
import threading
import frida
import websockets

# ====================== 默认配置 ======================
config = {
    "min_rumble": 800,          # 最小震动阈值
    "cooldown": 0.45,           # 冷却时间（秒）
    "duration": 0.65,           # 持续时间（秒）
    "strength_scale": 75,       # 强度缩放比例
    "min_level": 20,            # 最小电击强度
    "max_level": 95,            # 最大电击强度
    "use_max_motor": True,      # 是否取左右马达最大值
    "channel": "both",          # a / b / both
    "strength_mode": "rollback",# rollback / permanent
    "action": "both",           # both / strength / waveform
    "preset": "CS2-受伤",       # 波形预设
    "process_name": "OuterWilds.exe",
}

ws = None
loop = None
last_time = 0
last_time_lock = threading.Lock()
device_connected = True


async def send_log(level: str, message: str):
    """发送中文日志到 DGHub 运行日志"""
    if not ws:
        return
    try:
        await ws.send(json.dumps({
            "op": "log",
            "level": level,
            "message": message
        }))
    except Exception:
        pass


async def report_status(text: str):
    """上报状态"""
    if not ws:
        return
    try:
        await ws.send(json.dumps({
            "op": "status",
            "fields": {"display_status": text}
        }))
    except Exception:
        pass


async def trigger_shock(level: int):
    """向当前默认设备发送电击"""
    if not ws or not device_connected:
        return
    try:
        payload = {
            "op": "trigger",
            "action": config.get("action", "both"),
            "delta_pct": int(level),
            "strength_mode": config.get("strength_mode", "rollback"),
            "duration_s": float(config.get("duration", 0.65)),
            "preset": config.get("preset", "CS2-受伤"),
            "channel": config.get("channel", "both"),
            "label": "手柄震动 " + str(level) + "%"
        }
        await ws.send(json.dumps(payload))

        mode = "回落" if config.get("strength_mode") == "rollback" else "永久叠加"
        msg = "触发电击 +" + str(level) + "% | 通道:" + str(config.get("channel")) + " | 模式:" + mode
        await send_log("info", msg)
        print("[" + time.strftime("%H:%M:%S") + "] " + msg)
    except Exception as e:
        await send_log("error", "发送失败: " + str(e))
        print("发送失败: " + str(e))


def on_message(message, data):
    """收到 Frida 传来的震动数据"""
    global last_time

    if message.get("type") != "send":
        return

    payload = message.get("payload") or {}
    left = int(payload.get("left", 0))
    right = int(payload.get("right", 0))

    if config.get("use_max_motor", True):
        intensity = max(left, right)
    else:
        intensity = (left + right) // 2

    if intensity < int(config.get("min_rumble", 800)):
        return

    with last_time_lock:
        now = time.time()
        if now - last_time < float(config.get("cooldown", 0.45)):
            return
        last_time = now

    raw_level = int(intensity / 65535.0 * float(config.get("strength_scale", 75)))
    min_level = int(config.get("min_level", 20))
    max_level = int(config.get("max_level", 95))
    level = max(min_level, min(max_level, raw_level))

    if loop and loop.is_running():
        log_msg = "检测到震动 左=" + str(left) + " 右=" + str(right) + " -> 强度" + str(level) + "%"
        asyncio.run_coroutine_threadsafe(send_log("info", log_msg), loop)
        asyncio.run_coroutine_threadsafe(trigger_shock(level), loop)


def start_frida():
    """启动 Frida 监听手柄震动"""
    process_name = config.get("process_name", "OuterWilds.exe")
    print("正在附加到 " + process_name + " ...")

    try:
        session = frida.attach(process_name)
    except Exception as e:
        print("Frida 附加失败: " + str(e))
        if loop and loop.is_running():
            asyncio.run_coroutine_threadsafe(send_log("error", "Frida 附加失败: " + str(e)), loop)
            asyncio.run_coroutine_threadsafe(report_status("附加失败"), loop)
        return

    script = session.create_script("""
    function tryHook(name) {
        const mod = Process.findModuleByName(name);
        if (!mod) return false;
        let addr = null;
        try {
            addr = mod.findExportByName("XInputSetState") || mod.getExportByName("XInputSetState");
        } catch (e) {}
        if (!addr) return false;
        console.log("[+] Hooked " + name);
        Interceptor.attach(addr, {
            onEnter(args) {
                try {
                    const vib = args[1];
                    if (vib.isNull()) return;
                    send({left: vib.readU16(), right: vib.add(2).readU16()});
                } catch (e) {}
            }
        });
        return true;
    }

    const versions = ["xinput1_4.dll","xinput1_3.dll","xinput9_1_0.dll","XInput1_4.dll","XInput1_3.dll"];
    let ok = false;
    for (const dll of versions) {
        if (tryHook(dll)) { ok = true; break; }
    }
    console.log(ok ? "[+] 监听成功" : "[-] 未找到 XInputSetState");
    """)
    script.on("message", on_message)
    script.load()
    print("Frida 已启动")

    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(send_log("info", "Frida 已附加到 " + process_name), loop)
        asyncio.run_coroutine_threadsafe(report_status("正在监听 " + process_name), loop)

    while True:
        time.sleep(1)


async def main():
    global ws, loop, device_connected
    loop = asyncio.get_running_loop()

    host = os.environ.get("DGHUB_HOST", "127.0.0.1")
    port = os.environ.get("DGHUB_PORT")
    token = os.environ.get("DGHUB_TOKEN")

    if not port or not token:
        print("缺少环境变量 DGHUB_PORT 或 DGHUB_TOKEN")
        print("请通过 DGHub 启动本插件")
        return

    uri = "ws://" + str(host) + ":" + str(port) + "/ws/plugin?token=" + str(token)
    print("正在连接 DGHub: " + uri)

    async with websockets.connect(uri) as websocket:
        ws = websocket

        await ws.send(json.dumps({
            "op": "hello",
            "token": token,
            "manifest": {
                "id": "rumble_shock",
                "name": "手柄震动联动",
                "version": "1.5.0",
                "sdk": "1"
            }
        }))

        ack = json.loads(await ws.recv())
        if not ack.get("accepted"):
            print("握手失败: " + str(ack))
            return

        print("插件已连接 DGHub")
        await send_log("info", "插件已连接，等待配置")
        await report_status("已连接，等待配置")

        frida_started = False

        async for msg in ws:
            try:
                data = json.loads(msg)
            except Exception:
                continue

            op = data.get("op")

            if op == "stop":
                print("收到停止指令，退出")
                await send_log("info", "收到停止指令，插件退出")
                break

            elif op == "config":
                config.update(data.get("data", {}))
                print("收到全量配置")
                await send_log("info", "收到全量配置")
                if not frida_started:
                    frida_started = True
                    threading.Thread(target=start_frida, daemon=True).start()

            elif op == "config_changed":
                key = data.get("key")
                value = data.get("value")
                if key in config:
                    config[key] = value
                    await send_log("info", "配置已更新: " + str(key) + " = " + str(value))
                    if key == "process_name":
                        await send_log("warning", "进程名已修改，请重启插件后生效")
                        await report_status("进程名已改，请重启插件")

            elif op == "device_info":
                device_connected = bool(data.get("connected", False))
                status = "设备已连接" if device_connected else "设备未连接"
                await send_log("info", status)
                await report_status(status)

            elif op == "ping":
                try:
                    await ws.send(json.dumps({"op": "pong", "t": data.get("t")}))
                except Exception:
                    pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("插件已停止")