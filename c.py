import frida
import sys
import time

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        left = payload['left']
        right = payload['right']
        index = payload['index']
        print(f"[{time.strftime('%H:%M:%S')}] 手柄 {index} | 左马达: {left:5d} ({left/65535:.3f}) | 右马达: {right:5d} ({right/65535:.3f})")
    elif message['type'] == 'error':
        print(f"JS错误: {message.get('description', message)}")

def main():
    process_name = "ds.exe"   # 确认进程名正确

    try:
        session = frida.attach(process_name)
    except frida.ProcessNotFoundError:
        print(f"找不到进程: {process_name}")
        print("请先启动游戏，然后重新运行此脚本")
        return
    except Exception as e:
        print(f"附加失败: {e}")
        return

    # ===== 兼容 Frida 16 和 17+ 的脚本 =====
    script_code = """
    const xinputVersions = [
        "xinput1_4.dll",
        "xinput1_3.dll",
        "xinput9_1_0.dll",
        "XInput1_4.dll",
        "XInput1_3.dll",
        "xinput1_2.dll",
        "xinput1_1.dll"
    ];

    let hooked = false;

    for (const dll of xinputVersions) {
        try {
            const mod = Process.findModuleByName(dll);
            if (!mod) continue;

            // 新写法：从 Module 对象上找导出（Frida 17+ 必须这样）
            let addr = null;
            if (typeof mod.findExportByName === 'function') {
                addr = mod.findExportByName("XInputSetState");
            } else if (typeof mod.getExportByName === 'function') {
                addr = mod.getExportByName("XInputSetState");
            } else {
                // 兼容极老版本
                addr = Module.findExportByName(dll, "XInputSetState");
            }

            if (addr) {
                console.log("[+] 找到 " + dll + " -> XInputSetState @ " + addr);

                Interceptor.attach(addr, {
                    onEnter: function(args) {
                        const userIndex = args[0].toInt32();
                        const vibPtr = args[1];

                        const leftMotor  = vibPtr.readU16();
                        const rightMotor = vibPtr.add(2).readU16();

                        send({
                            index: userIndex,
                            left: leftMotor,
                            right: rightMotor
                        });
                    }
                });

                hooked = true;
                break;
            }
        } catch (e) {
            console.log("尝试 " + dll + " 时出错: " + e);
        }
    }

    if (!hooked) {
        console.log("[-] 未找到任何 XInputSetState");
        console.log("可能原因：");
        console.log("1. 游戏开启了 Steam Input（推荐强制关闭）");
        console.log("2. 游戏使用了其他输入方式");
        console.log("3. 进程架构不匹配（32/64位）");
    } else {
        console.log("[+] Hook 成功，等待震动数据...");
    }
    """

    script = session.create_script(script_code)
    script.on('message', on_message)
    script.load()

    print("开始监听震动数据... 按 Ctrl+C 退出")
    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        print("\n已停止")

if __name__ == "__main__":
    main()