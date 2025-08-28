import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract
import pyttsx3
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import offline
import online

def display_image(cv_img):
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_img)
    img = img.resize((300, 300))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img

def voice(text_img,m):
    gray = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    # engine = pyttsx3.init()

    # engine.setProperty('rate', 150)

    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)
    #print(text)
    # engine.say(text)
    # engine.runAndWait()
    if m==1:
        offline.questions(text)
    else:
        online.generate_one_word_questions(text)
       



selected_image = None  
cap = None 

def upload_image():
    global selected_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        selected_image = cv2.imread(file_path)
        display_image(selected_image)
        root.update()
        voice(selected_image,1)

def upload_image_online():
    global selected_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        selected_image = cv2.imread(file_path)
        display_image(selected_image)
        root.update()
        voice(selected_image,2)

def click_by_camera():
    global cap, camera_window, camera_label

    camera_window = tk.Toplevel(root)
    camera_window.title("Camera Preview")

    camera_label = tk.Label(camera_window)
    camera_label.pack()

    capture_btn = tk.Button(camera_window, text="Capture", command=capture_frame)
    capture_btn.pack(pady=5)

    cap = cv2.VideoCapture(1)
    update_video_frame()

def update_video_frame():
    global cap, camera_label

    ret, frame = cap.read()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

    if camera_window.winfo_exists():
        camera_label.after(10, update_video_frame)
    else:
        cap.release()

def capture_frame():
    global selected_image, cap
    ret, frame = cap.read()
    if ret:
        selected_image = frame
        display_image(selected_image)
        root.update()
        voice(selected_image)
        messagebox.showinfo("Image Captured", "Image has been captured successfully.")
        cap.release()
        camera_window.destroy()

# Main GUI
root = tk.Tk()
root.title("Image Selector")
root.geometry("700x850")

tk.Label(root, text="Select or Capture an Image", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Upload Image", command=upload_image, width=20, height=2, bg="lightblue").pack(pady=10)
tk.Button(root, text="Click by Camera", command=click_by_camera, width=20, height=2, bg="lightgreen").pack(pady=10)
tk.Button(root, text="Online Question Generation", command=upload_image_online, width=20, height=2, bg="orange").pack(pady=10)
image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()
