import cv2
import os
import random
import tkinter as tk
from tkinter import filedialog
import random

class BoxEditor:
    def __init__(self, image_path, label_path):
        try:
            self.image_path = image_path
            self.image = cv2.imread(image_path)
            print(image_path)
            print(self.image.shape[0])
            y = self.image.shape[0]
            y = y/2
            print(y)
            x = self.image.shape[1]
            x = x/2
            print(x)
            self.image = cv2.resize(self.image, (int(x)+50, int(y)+50))
            self.original_image = self.image.copy()
            self.zoom_scale = 1.0
            self.pan_x, self.pan_y = 0, 0

        except:
            self.image = None
            print("Image Not Found")
        self.label_path = label_path
        self.boxes = self.load_labels(label_path)
        self.selected_box = 0 if self.boxes else None
        self.dragging = False
        self.resizing = False
        self.drawing = False
        self.start_point = None
        self.class_ids = self.load_class_ids()
        self.colors = self.load_colors()

    def load_labels(self, label_path):
        boxes = []
        try:
            with open(label_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    cls = int(parts[0])
                    x, y, w, h = map(float, parts[1:])
                    boxes.append([cls, x, y, w, h])
        except Exception as e:
            print(f"Error loading labels: {e}")
        return boxes

    def load_class_ids(self):
        class_ids = []
        try:
            with open("class_id_list.txt", "r") as file:
                class_ids = [int(line.strip()) for line in file]
        except Exception as e:
            print(f"Error loading class IDs: {e}")
        return class_ids

    def load_colors(self):
        colors = {}
        try:
            with open("colors.txt", "r") as file:
                for line in file:
                    parts = line.strip().split()
                    cls = int(parts[0])
                    r, g, b = map(int, parts[1:])
                    colors[cls] = (r, g, b)
        except Exception as e:
            print(f"Error loading colors: {e}")
        return colors

    def draw_boxes(self, clsOut=None):
        for i, (cls, x, y, w, h) in enumerate(self.boxes):
            if cls != 23:
                x1, y1 = int((x - w / 2) * self.image.shape[1]), int((y - h / 2) * self.image.shape[0])
                x2, y2 = int((x + w / 2) * self.image.shape[1]), int((y + h / 2) * self.image.shape[0])
                color = self.colors.get(cls, (0, 0, 255))
                if i == self.selected_box:
                    color = (0, 255, 0)
                cv2.rectangle(self.image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(self.image, f"{cls}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def zoom(self, scale):
        self.zoom_scale = max(0.1, min(10, self.zoom_scale * scale))  
        height, width = self.original_image.shape[:2]
        new_size = (int(width * self.zoom_scale), int(height * self.zoom_scale))
        self.image = cv2.resize(self.original_image, new_size)

        self.pan_x = max(0, min(self.pan_x, new_size[0] - width))
        self.pan_y = max(0, min(self.pan_y, new_size[1] - height))

        self.image = self.image[self.pan_y:self.pan_y + height, self.pan_x:self.pan_x + width]

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.resizing:
                self.resizing = False
                self.dragging = False
                return

            if self.drawing:
                self.start_point = (x, y)
                return

            for i, (cls, bx, by, bw, bh) in enumerate(self.boxes):
                x1, y1 = int((bx - bw / 2) * self.image.shape[1]), int((by - bh / 2) * self.image.shape[0])
                x2, y2 = int((bx + bw / 2) * self.image.shape[1]), int((by + bh / 2) * self.image.shape[0])
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.selected_box = i
                    self.dragging = True
                    break

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging and self.selected_box is not None:
                cls, bx, by, bw, bh = self.boxes[self.selected_box]
                self.boxes[self.selected_box] = [cls, (x + self.pan_x) / self.image.shape[1], (y + self.pan_y) / self.image.shape[0], bw, bh]

            if self.resizing and self.selected_box is not None:
                cls, bx, by, bw, bh = self.boxes[self.selected_box]
                x1, y1 = int((bx - bw / 2) * self.image.shape[1]), int((by - bh / 2) * self.image.shape[0])
                self.boxes[self.selected_box] = [cls, bx, by, (x - x1) / self.image.shape[1],
                                                 (y - y1) / self.image.shape[0]]

            if self.drawing and self.start_point is not None:
                img_copy = self.image.copy()
                end_point = (x, y)
                x1, y1 = self.start_point
                x2, y2 = end_point
                cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.imshow("Image", img_copy)

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            if self.drawing and self.start_point is not None:
                end_point = (x, y)
                x1, y1 = self.start_point
                x2, y2 = end_point
                cls = 0
                bx, by = (x1 + x2) / 2 / self.image.shape[1], (y1 + y2) / 2 / self.image.shape[0]
                bw, bh = abs(x2 - x1) / self.image.shape[1], abs(y2 - y1) / self.image.shape[0]
                self.boxes.append([cls, bx, by, bw, bh])
                self.start_point = None
                self.drawing = False
                self.resizing = False

            if self.resizing:
                self.resizing = False

    def save_labels(self):
        try:
            with open(self.label_path, "w") as file:
                for cls, x, y, w, h in self.boxes:
                    file.write(f"{cls} {x} {y} {w} {h}\n")
        except Exception as e:
            print(f"Error saving labels: {e}")

    def run(self):
        clsOut = None
        flg = 0
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.on_mouse)
        while True:
            try:
                img_copy = self.image.copy()
                self.draw_boxes(clsOut)
                cv2.imshow("Image", self.image)
            except Exception as e:
                print(f"Error displaying image: {e}")
                break
            key = cv2.waitKey(1)
            self.image = img_copy

            if key == ord('s'):
                self.save_labels()
            elif key == ord('e'):
                return 1
            elif key == ord('d'):
                return -2
            elif key == ord('r'):
                return -1
            elif key == ord('w'):
                self.resizing = True
            elif key == ord('a'):
                self.drawing = True
            elif ord('0') <= key <= ord('9'):
                if flg == 1:
                    cv2.destroyWindow(f"{clsOut}")
                clsOut = key - ord('0')
                try:
                    class_image = cv2.imread(f"mapping/{clsOut}.jpg")
                    if class_image is None:
                        raise ValueError(f"Class image not found for class {clsOut}")
                    cv2.imshow(f'{clsOut}', class_image)
                    flg = 1
                except Exception as e:
                    print(f"Error displaying class image: {e}")
                    return 0
            elif key == ord('q'):
                if self.selected_box is not None:
                    del self.boxes[self.selected_box]
                    self.selected_box = None

            elif key == ord('z'):
                if self.selected_box is not None:
                    cls, x, y, w, h = self.boxes[self.selected_box]
                    new_cls = cls + 1
                    self.boxes[self.selected_box] = [new_cls, x, y, w, h]

            elif key == ord('x'):
                if self.selected_box is not None:
                    cls, x, y, w, h = self.boxes[self.selected_box]
                    if cls == 0:
                        continue
                    new_cls = cls - 1
                    self.boxes[self.selected_box] = [new_cls, x, y, w, h]
            elif key == ord('c'):
                self.zoom(1.1)

            elif key == ord('f'):
                self.zoom(0.9)

            elif key == ord('v'):
                self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
                
            elif key == ord('b'):
                try:
                    if os.path.exists(self.label_path):
                        os.remove(self.label_path)
                        print(f"Deleted label file: {self.label_path}")
                            
                    if os.path.exists(self.image_path):
                        os.remove(self.image_path)
                        print(f"Deleted image file: {self.image_path}")         
                    return 1
                except Exception as e:
                    print(f"Error deleting files: {e}")
                    break
            elif key== ord("t"):
                try:
                    cls, x, y, w, h = self.boxes[self.selected_box]
                    new_cls = 9
                    self.boxes[self.selected_box] = [new_cls, x, y, w, h]
                except:
                    print("select box")

def select_folders():
    root = tk.Tk()
    root.withdraw()
    image_folder = filedialog.askdirectory(title="Select Image Folder")
    label_folder = filedialog.askdirectory(title="Select Label Folder")
    return image_folder, label_folder

def create_colors_file(class_id_file, colors_file):
    try:
        with open(class_id_file, "r") as class_file, open(colors_file, "w") as color_file:
            for line in class_file:
                class_id = line.strip()
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                color_file.write(f"{class_id} {r} {g} {b}\n")
        print(f"Colors file '{colors_file}' created successfully.")
    except Exception as e:
        print(f"Error creating colors file: {e}")
def main():
    create_colors_file("class_id_list.txt", "colors.txt")
    folder_path, label_folder_path = select_folders()
    if not folder_path or not label_folder_path:
        print(f"You did not choose image or label folder")
        return

    image_files = os.listdir(folder_path)

    i = 0
    while i < len(image_files):
        print(i)
        image_file = image_files[i]
        image_path = os.path.join(folder_path, image_file)
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(label_folder_path, label_file)
        editor = BoxEditor(image_path, label_path)
        result = editor.run()

        if result == -2 and i != 0:
            i -= 1
        elif result == -1:
            print("QUIT")
            break
        elif result == 1:
            i += 1
        else:
            print("ERROR")
            break

if __name__ == "__main__":
    main()
