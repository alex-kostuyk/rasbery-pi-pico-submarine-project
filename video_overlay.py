import subprocess

capture_type = "dshow"#"v4l2"
capture_size = "640x480"
input_device = 'video = "USB2.0 PC CAMERA"'
drawtext = []
drawbox = []
options = ['']
filters = []

input_file = "telemetry.json"
drawtext.append(f"drawtext=textfile={input_file}")
color = "white"
alpha = 0.1
drawtext.append(f"fontcolor={color}@{alpha}")
font_size = 30
drawtext.append(f"fontsize={font_size}")
drawtext.append("box=1")
box_color = "black"
box_alpha = 0.4
drawtext.append(f"boxcolor={box_color}@{box_alpha}")
drawtext.append("x=w-tw:y=h-th")

capture_format = "yuv420p"
options.append(f"format={capture_format}")

filters.append("xv")

name = "Clownboat"

ffmpeg_cmd = "ffmpeg " + "-f " + capture_type + " -video_size " + capture_size + \
    " -i " + input_device + ' -vf "' + ":".join(drawtext) + \
    ",".join(options) + '"' + ' -f ' + "".join(filters) + " " + name
print(ffmpeg_cmd)

try:
    subprocess.run(ffmpeg_cmd, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print("Error running FFmpeg command:", e)