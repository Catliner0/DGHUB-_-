import asyncio
import json
import os
import sys
import time
import threading
import frida
import websockets

# ====================== 默认配置 ======================
config = {
    "min_rumble": 800,
    "cooldown": 0.45,
    "duration": 0.65,
    "strength_scale": 75,
    "preset": "CS2-受伤",
    "process_name": "OuterWilds.exe",
}

ws = None
loop = None
last_time = 0
last_time_lock = threading.Lock()
device_connected = True
frida_session = None


async def trigger_shock(level: int):
    if not ws or not device_connected:
        return
    try:
        await ws.send(json.dumps({
            "op": "trigger",
            "action": "both",
            "delta_pct": level,
            "strength_mode": "rollback",
            "duration_s": config["duration"],
            "preset": config["preset"],
            "channel": "both",
            "label": f"手柄震动 {level}%"
        }))
        print(f"[{time.strftime('%H:%M:%S')}] 触发电击 +{level}%")
    except Exception as e:
        print(f"发送失败: {e}")


async def report_status(text: str):
    if not ws:
        return
    try:
        await ws.send(json.dumps({
            "op": "status",
            "fields": {
                "display_status": text
            }
        }))
    except Exception:
        pass


def on_message(message, data):
    global last_time

    if message["type"] != "send":
        return

    left = message["payload"].get("left", 0)
    right = message["payload"].get("right", 0)
    intensity = max(left, right)

    if intensity < config["min_rumble"]:
        return

    with last_time_lock:
        now = time.time()
        if now - last_time < config["cooldown"]:
            return
        last_time = now

    level = min(95, max(20, int(intensity / 65535 * config["strength_scale"])))

    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(trigger_shock(level), loop)


def start_frida():
    global frida_session

    process_name = config.get("process_name", "OuterWilds.exe")
    print(f"正在附加到 {process_name} ...")

    try:
        frida_session = frida.attach(process_name)
    except Exception as e:
        print(f"Frida 附加失败: {e}")
        if loop and loop.is_running():
            asyncio.run_coroutine_threadsafe(
                report_status(f"附加失败: {process_name}"), loop
            )
        return

    script = frida_session.create_script("""
    function tryHook(name) {
        const mod = Process.findModuleByName(name);
        if (!mod) return false;

        let addr = null;
        try {
            addr = mod.findExportByName("XInputSetState") || mod.getExportByName("XInputSetState");
        } catch (e) {}

        if (!addr) return false;

        console.log("[+] Hooked " + name + " @ " + addr);
        Interceptor.attach(addr, {
            onEnter(args) {
                try {
                    const vib = args[1];
                    if (vib.isNull()) return;
                    const left = vib.readU16();
                    const right = vib.add(2).readU16();
                    send({left: left, right: right});
                } catch (e) {}
            }
        });
        return true;
    }

    const versions = [
        "xinput1_4.dll", "xinput1_3.dll", "xinput9_1_0.dll",
        "XInput1_4.dll", "XInput1_3.dll", "xinput1_2.dll", "xinput1_1.dll"
    ];

    let hooked = false;
    for (const dll of versions) {
        if (tryHook(dll)) {
            hooked = true;
            break;
        }
    }

    if (hooked) {
        console.log("[+] 监听成功");
    } else {
        console.log("[-] 未找到 XInputSetState");
    }
    """)

    script.on("message", on_message)
    script.load()
    print("Frida 已启动")

    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(
            report_status(f"已监听 {process_name}"), loop
        )

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
        print("请务必通过 DGHub 主程序启动这个插件！")
        return

    uri = f"ws://{host}:{port}/ws/plugin?token={token}"
    print(f"连接 DGHub: {uri}")

    async with websockets.connect(uri) as websocket:
        ws = websocket

        # 握手
        await ws.send(json.dumps({
            "op": "hello",
            "token": token,
            "manifest": {
                "id": "rumble_shock",
                "name": "手柄震动联动",
                "version": "1.2.0",
                "sdk": "1"
            }
        }))

        ack = json.loads(await ws.recv())
        if not ack.get("accepted"):
            print("握手失败:", ack)
            return

        print("插件已连接 DGHub")
        await report_status("已连接，等待游戏...")

        # 启动 Frida
        t = threading.Thread(target=start_frida, daemon=True)
        t.start()

        # 消息循环
        async for msg in ws:
            try:
                data = json.loads(msg)
            except Exception:
                continue

            op = data.get("op")

            if op == "stop":
                print("收到停止指令，退出")
                break

            elif op == "config":
                new_cfg = data.get("data", {})
                config.update(new_cfg)
                print("收到全量配置:", config)

            elif op == "config_changed":
                key = data.get("key")
                value = data.get("value")
                if key in config:
                    config[key] = value
                    print(f"配置更新: {key} = {value}")

            elif op == "device_info":
                device_connected = bool(data.get("connected", False))
                status = "设备已连接" if device_connected else "设备未连接"
                print(status)
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