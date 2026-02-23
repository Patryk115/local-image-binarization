# Local Image Binarization

A desktop application for advanced grayscale image processing. It allows users to perform various thresholding operations (both global and local) on loaded images. 

Binarization, also known as thresholding, involves converting a grayscale image into a binary image, where pixels take one of two values: black (0) or white (255). The goal of this operation is to simplify the image, which is a crucial preprocessing step in Computer Vision (e.g., it facilitates OCR text recognition, edge detection, or object segmentation).

Unlike global binarization, **local binarization** applies different thresholds to different parts of the image. It is particularly effective for photographs with uneven lighting or highly complex backgrounds, where applying a single global threshold would lead to the loss of important details.

---

## Application Preview

![Local Image Binarization - GUI](<img width="1754" height="973" alt="image" src="https://github.com/user-attachments/assets/8d14167d-83ec-4c59-98c6-8d91d16039ee" />)

---

## Key Features

* **Real-time analysis:** Automatic generation and display of histograms for both the input and output images, making it easier to evaluate the effectiveness of the chosen method.
* **Flexibility and parameterization:** The user has full control over algorithm parameters, such as window size (for local methods), threshold offset, or manually entered values for global methods.
* **Responsive interface:** The application automatically adjusts the layout, font scale, and label width to the window size.
* **Bilingual:** Built-in, instant switching between Polish and English throughout the entire interface.
* **Exception handling (UX):** Safeguards preventing program crashes (e.g., blocking saving before processing, validation of entered numerical data, verification of supported file formats).
* **Data export:** Ability to save the processed image directly to `.png` or `.jpg` formats.

---

## Implemented Algorithms

The application provides 6 different image segmentation methods, allowing the user to select the appropriate technique for a specific photo:

### 1. Global Binarization (1-threshold)
A basic technique where a single common threshold is applied to the entire image. For each pixel, its intensity value (0-255) is checked. If it is greater than or equal to the set threshold value, the pixel becomes white; otherwise, it becomes black. Highly effective with uniform lighting.

### 2. Global Binarization (2-thresholds)
An extension of the single-threshold method allowing the extraction of a specific intensity range. Pixels whose values fall between the defined lower and upper thresholds receive the maximum value (white), while everything else is suppressed (black).

### 3. Local Otsu Method
An adaptive approach to binarization. The image is divided into smaller blocks of a selected size (e.g., 16x16, 32x32). For each block, the algorithm automatically calculates the optimal threshold, maximizing inter-class variance and minimizing intra-class variance.

### 4. Sauvola Method
An advanced adaptive technique that takes into account local image properties. In the application, it is based on the `cv2.adaptiveThreshold` function using a Gaussian filter, which assigns higher weights to pixels closer to the center of the analyzed window. This allows for very precise extraction of, for example, fine text from a noisy background.

### 5. Local Binarization with Average
A local window of selected dimensions is defined for each pixel, and its average intensity is calculated. The threshold for the analyzed pixel is exactly this calculated average. If the pixel is brighter than its immediate surroundings, it becomes white.

### 6. Local Binarization with Offset
An extension of the average method. After calculating the local average for a given window, the threshold is additionally modified by adding or subtracting an `offset` value. This gives the user extra control over the sensitivity of the local algorithm.

---

## Technologies and Tools

The project was developed entirely in **Python 3**. The following libraries were used to build the mechanics and the GUI:
* **OpenCV (`cv2`) & NumPy** – The main computational engine for matrix processing, algorithm implementation, and image manipulation.
* **Tkinter** – A built-in Python library used to create a lightweight, native graphical user interface (GUI).
* **Matplotlib** – Used for rendering analytical charts (intensity histograms).
* **Pillow (PIL)** – Ensures efficient conversion of OpenCV matrix formats to image formats compatible with the Tkinter interface.

---

## Project Structure

* **Local Image Binarization**
  * `Obrazy/` - Directory containing sample test images
  * `Wynikowe obrazy/` - Default directory for saved, generated binary images
  * `main.py` - Main file containing the application's source code
  * `requirements.txt` - File containing the list of required Python dependencies
  * `.gitignore` - Configuration file for Git
  * `README.md` - Project documentation

---

## Installation and Usage (For Developers)

The application can be easily run locally by installing the required libraries.

**Step 1:** Clone this repository to your local machine:
> `git clone https://github.com/YourUsername/repository-name.git`

**Step 2:** Navigate to the downloaded project folder and install the required packages (using a virtual environment is recommended):
> `pip install -r requirements.txt`

**Step 3:** Run the main Python script:
> `python main.py`
