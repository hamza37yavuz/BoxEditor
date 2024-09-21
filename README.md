# Bounding Box Editor

## Description
The `BoxEditor` is a Python-based tool that allows users to visualize, edit, and manipulate bounding boxes on images using OpenCV. It loads images and their corresponding YOLO-style label files, allowing you to zoom, pan, draw, resize, and delete bounding boxes on the images. Additionally, it supports displaying a reference image for a selected class and changing the class of the bounding box. 

## Features
- **Load YOLO-style labels**: The labels are formatted as `class_id x_center y_center width height`.
- **Edit bounding boxes**: Select boxes, move, resize, and delete them.
- **Draw new bounding boxes**: Manually create new bounding boxes by clicking and dragging on the image.
- **Zoom and pan**: Zoom in/out of the image for detailed editing.
- **Class display**: View a reference image for a selected class.
- **Save changes**: Save the modified bounding boxes back to the label file.
- **Rotate image**: Rotate the image 90 degrees clockwise.
- **Delete image and label file**: Permanently delete the image and its label file.
  
## Dependencies
- `opencv-python`
- `tkinter`

To install the dependencies, run:
```bash
pip install opencv-python tk
```

## Usage

1. **Class ID and Color Files**: Ensure you have the following two files in your working directory:
   - `class_id_list.txt`: A file containing one class ID per line.
   - `colors.txt`: A file with a color mapping for each class. If this file is not present, the script will generate it automatically using random colors for each class.

2. **Run the program**:
   ```bash
   python your_script_name.py
   ```

3. **Folder Selection**: 
   - When the program starts, you will be prompted to select an image folder and a label folder using the file dialog.

4. **Image Navigation**:
   - The program processes images in the selected folder one by one.
   - After editing the bounding boxes, you can navigate through the images or delete them.

### Keybindings
| Key | Action |
| --- | ------ |
| `s` | Save the current labels to the label file |
| `e` | Move to the next image |
| `d` | Move to the previous image |
| `r` | Quit the program |
| `w` | Resize the selected bounding box |
| `a` | Start drawing a new bounding box |
| `0-9` | Display a reference image for the corresponding class |
| `q` | Delete the selected bounding box |
| `z` | Increase the class ID of the selected bounding box |
| `x` | Decrease the class ID of the selected bounding box |
| `c` | Zoom in on the image |
| `f` | Zoom out of the image |
| `v` | Rotate the image 90 degrees clockwise |
| `b` | Permanently delete the image and label file |
| `t` | Change the selected bounding box class to `9` |

## Customization
- **Color Configuration**: Colors for each class are stored in `colors.txt`. This file can be manually edited or automatically generated by the program if it's missing.
- **Class Images**: Class images can be stored in a `mapping` folder, with each image named as `<class_id>.jpg` (e.g., `0.jpg`, `1.jpg`, etc.). These images are displayed when selecting a class ID.
- This is a customized version. You may need to make some corrections.

## Error Handling
- The program handles missing files, invalid image paths, and faulty label files gracefully by providing error messages and moving to the next image if needed.
