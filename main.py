import cv2
import pandas as pd

# === Load CSV of known colors ===
csv_path = 'colors.csv'
index = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv(csv_path, names=index, header=None)

# === Globals for mouse click ===
clicked = False
r = g = b = xpos = ypos = 0

# === Get nearest color name ===
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

# === Mouse Callback ===
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = param[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# === Mode: Image or Video ===
mode = input("Enter 'image' or 'video': ").strip().lower()

if mode == "image":
    # === IMAGE MODE ===
    img_path = "sample.jpg"
    img = cv2.imread(img_path)
    img = cv2.resize(img, (800, 600))
    cv2.namedWindow('Color Detector')
    cv2.setMouseCallback('Color Detector', draw_function, param=img)

    while True:
        display = img.copy()
        if clicked:
            color_name = get_color_name(r, g, b)
            text = f"{color_name} R={r} G={g} B={b}"
            center = (400, 50)
            axes = (350, 30)
            cv2.ellipse(display, center, axes, 0, 0, 360, (b, g, r), -1)
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = center[0] - text_size[0] // 2
            text_y = center[1] + text_size[1] // 2
            text_color = (255,255,255) if r+g+b < 400 else (0,0,0)
            cv2.putText(display, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

        cv2.imshow("Color Detector", display)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

elif mode == "video":
    # === VIDEO MODE ===
    video_path = 'video.mp4'  # Change to your actual file name
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    cv2.namedWindow('Color Detector')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (800, 600))
        cv2.setMouseCallback('Color Detector', draw_function, param=resized_frame)
        display = resized_frame.copy()

        if clicked:
            color_name = get_color_name(r, g, b)
            text = f"{color_name} R={r} G={g} B={b}"
            center = (400, 50)
            axes = (350, 30)
            cv2.ellipse(display, center, axes, 0, 0, 360, (b, g, r), -1)
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = center[0] - text_size[0] // 2
            text_y = center[1] + text_size[1] // 2
            text_color = (255,255,255) if r+g+b < 400 else (0,0,0)
            cv2.putText(display, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

        cv2.imshow("Color Detector", display)
        if cv2.waitKey(25) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

else:
    print("Invalid input. Please enter 'image' or 'video'.")
