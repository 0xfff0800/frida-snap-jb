import frida
import sys
import os
from datetime import datetime

# ============================================================
#   Reverse Engineered by  0xfff0800 = FaLaH
#   Telegram Channel : https://t.me/xfff0800
# ============================================================
#
#   HOW TO USE :
#
#   Requirements:
#     - Jailbroken iPhone with Frida server running
#     - Install Python library : pip install frida-tools
#     - Connect device via USB cable
#
#   1. Start Frida server on the jailbroken device
#   2. Connect device via USB
#   3. Run :  python3 frida-snap.py
#   4. Open Snapchat on the device and browse chats
#   5. Images, videos, and voice notes will be saved silently
#      with NO notification sent to the other party
#   6. Saved files location :  ~/Desktop/downloaded_snapchat/
#   7. Captured text messages will be printed in the terminal
#
# ============================================================
#
#   WARNING — LEGAL DISCLAIMER :
#
#   This tool is provided for EDUCATIONAL and SECURITY RESEARCH
#   purposes ONLY.
#
#   - Do NOT use this tool on devices you do not own.
#   - Do NOT use this tool to capture or save content shared by
#     others without their explicit written consent.
#   - Unauthorized interception of private communications is a
#     criminal offense under applicable law (CFAA, CMA, and
#     local equivalents).
#   - The author (0xfff0800 / FaLaH) holds NO responsibility
#     for any misuse, damage, or legal consequences resulting
#     from the use of this tool.
#   - By using this tool, you agree that you are solely
#     responsible for your own actions.
#
# ============================================================

# Preparing the save folder
SAVE_DIR = os.path.expanduser("~/Desktop/downloaded_snapchat")
os.makedirs(SAVE_DIR, exist_ok=True)

# Register to prevent duplication
pulled_files = set()

JSCODE = """
var seenTexts = new Set();
var seenImages = new Set();

function safeHook(className, methodName, callbacks) {
  var cls = ObjC.classes[className];
  if (!cls) return;
  var method = cls[methodName];
  if (!method) return;
  Interceptor.attach(method.implementation, callbacks);
}

safeHook("UIImage", "+ imageWithData:", {
  onEnter(args) {
    try {
      var data = new ObjC.Object(args[2]);
      var len = data.length();

      if (len > 30000) { 
        var buffer = data.bytes().readByteArray(len);
        if (!seenImages.has(len)) {
            seenImages.add(len);
            send({type: "SAVE_DATA", ext: "jpg", length: len}, buffer);
            console.log("[IMAGE CAPTURED] Size: " + len);
        }
      }
    } catch(e){}
  }
});

safeHook("NSData", "+ dataWithContentsOfFile:", {
  onEnter(args) {
    try {
      var path = new ObjC.Object(args[2]).toString();
      if (path.includes("SCPersistentMedia") || path.includes("media_cache")) {
          var ext = path.toLowerCase().includes(".mov") ? "mov" : "jpg";
          send({type: "FILE_FOUND", path: path, ext: ext});
      }
    } catch(e){}
  }
});

safeHook("AVAsset", "+ assetWithURL:", {
  onEnter(args) {
    try {
      var url = new ObjC.Object(args[2]).toString();
      if (url.startsWith("file:///")) {
          var path = url.replace("file://", "");
          send({type: "FILE_FOUND", path: path, ext: "mov"});
      }
    } catch(e){}
  }
});

function readFileHandler(message) {
    if (message.type === 'read_file') {
        var path = message.path;
        var ext = message.ext;
        try {
            var fileData = ObjC.classes.NSData.dataWithContentsOfFile_(path);
            if (fileData) {
                var len = fileData.length();
                var buffer = fileData.bytes().readByteArray(len);
                send({type: "SAVE_DATA", ext: ext, length: len}, buffer);
            }
        } catch(e) {}
    }
    recv('read_file', readFileHandler);
}
recv('read_file', readFileHandler);

safeHook("SCMessagingText", "- text", {
  onLeave(retval) {
    try {
      var text = new ObjC.Object(retval).toString();
      if (text && !seenTexts.has(text)) {
        seenTexts.add(text);
        send({type: "TEXT", data: text});
      }
    } catch(e) {}
  }
});
"""

def on_message(message, data):
    if message["type"] == "send":
        payload = message["payload"]
        t = payload["type"]
        
        if t == "FILE_FOUND":
            path = payload["path"]
            ext = payload["ext"]
            if path not in pulled_files:
                pulled_files.add(path)
                script.post({'type': 'read_file', 'path': path, 'ext': ext})

        elif t == "SAVE_DATA":
            ext = payload.get("ext", "bin")
            timestamp = datetime.now().strftime("%H%M%S_%f")
            filename = f"dump_{timestamp}.{ext}"
            filepath = os.path.join(SAVE_DIR, filename)
            
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"🔓 [SUCCESS] SAVE DONE  {ext}: {filename}")

        elif t == "TEXT":
            print(f"💬 [TEXT] {payload.get('data')}")

def main():
    global script
    try:
        device = frida.get_usb_device()
        pid = device.spawn(["com.toyopagroup.picaboo"])
        session = device.attach(pid)
        script = session.create_script(JSCODE)
        script.on("message", on_message)
        script.load()
        device.resume(pid)
        print(f"SAVE PATH : {SAVE_DIR}")
        sys.stdin.read()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()