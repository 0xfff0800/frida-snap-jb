# frida-snap-jb

Snapchat media and message dumper using Frida on jailbroken iOS
Researched and built by 0xfff0800 (FaLaH) — https://t.me/xfff0800

![frida-snap-jb](https://l.top4top.io/p_3799n34vr1.jpeg)

Description
-----------

This tool uses Frida dynamic instrumentation to hook into Snapchat on a
jailbroken iPhone and silently capture images, videos, voice notes, and
chat text messages at runtime — with NO screenshot notification sent to
the other party.

It works by intercepting Objective-C methods that Snapchat uses internally
to load and read media, bypassing the app-level save restrictions entirely.


Requirements
------------

    Jailbroken iPhone with Frida server installed and running
    USB cable connected to your Mac

    pip install frida-tools


How to Use
----------

Step 1 : Install Frida server on your jailbroken device
         (available via Cydia or Sileo — search for "Frida")

Step 2 : Start Frida server on the device

Step 3 : Connect the device to your Mac via USB

Step 4 : Run:

    python3 frida-snap.py

Step 5 : Open Snapchat on the device and browse chats

Step 6 : Images, videos, and voice notes are saved silently to:

    ~/Desktop/downloaded_snapchat/

    No notification is sent to the other party.

Step 7 : Text messages are printed live in the terminal


What Gets Captured
------------------

    Images       — Snaps and media loaded in memory (saved as .jpg)
    Videos       — Media files from Snapchat cache (saved as .mov)
    Voice notes  — Audio files intercepted via file path hooks
    Text         — Chat messages from SCMessagingText


Legal Disclaimer
----------------

This tool is provided for EDUCATIONAL and SECURITY RESEARCH purposes ONLY.

- Do NOT use this tool on devices you do not own.
- Do NOT use this tool to capture or save content shared by others
  without their explicit written consent.
- Unauthorized interception of private communications is a criminal
  offense under applicable law (CFAA, CMA, and local equivalents).
- The author holds NO responsibility for any misuse, damage, or legal
  consequences resulting from the use of this tool.
- By using this tool, you agree that you are solely responsible for
  your own actions.


Author
------

0xfff0800 / FaLaH
Telegram : https://t.me/xfff0800
