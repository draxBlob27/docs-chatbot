import cv2
import pytesseract
import spacy
from pdf2image import convert_from_path
import numpy as np
from typing import List, Dict
from PIL import Image

nlp = spacy.load("en_core_web_sm")

def grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def binarization(image: np.ndarray) -> np.ndarray:
    thresh, im_bw = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return im_bw

def noise_removal(image: np.ndarray) -> np.ndarray:
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    if len(newImage.shape) == 3 and newImage.shape[2] == 3:
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    else:
        gray = newImage
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Find largest contour and surround in min area box
    if len(contours) == 0:
        return 0.0
    largestContour = contours[0]
    # print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    (width, height) = minAreaRect[1]

    if width < height:
        angle = angle + 90

    if abs(angle) > 45:  # sanity check, skip clearly wrong angles
        return 0.0

    return -angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    # print(angle)
    return rotateImage(cvImage, -1.0 * angle)

def remove_borders(image):
    contours, heirarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

def preprocess_image(image: np.ndarray) -> np.ndarray:
    deskewed_img = deskew(image)
    gray_image = grayscale(deskewed_img)
    im_bw = binarization(gray_image)
    no_noise = noise_removal(im_bw)
    no_borders = remove_borders(no_noise)
    color = [255, 255, 255]
    top, bottom, left, right = [150]*4
    image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    
    return image_with_border

def ocr_image(image: np.ndarray) -> str:
    processed = preprocess_image(image)
    
    if len(processed.shape) == 2:
        pil_image = Image.fromarray(processed)
    else:
        # Convert BGR (OpenCV) to RGB
        rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)
        
    # display(pil_image)
    text = pytesseract.image_to_string(pil_image)
    return text

def chunking(filepath: str, dpi: int = 300) -> List[Dict]:
    pages = convert_from_path(filepath, dpi=dpi)
    # for img in pages:
    #     display(img)
    result = []
    for page_num, page in enumerate(pages, start = 1):
        img = np.array(page)
        text = ocr_image(img)

        paragraphs = text.split("\n\n")
        for para_num, paragraph in enumerate(paragraphs, start=1):
            if paragraph.strip():
                doc = nlp(paragraph)
                sentences = list(doc.sents)
                for sent_num, sent in enumerate(sentences, start=1):
                    metadata = {
                        "file_name": filepath,
                        "page_number": page_num,
                        "paragraph_number": para_num,
                        "sentence_number": sent_num,
                    }
                    result.append({
                        "text": sent.text.strip(),
                        "metadata": metadata
                    })

    return result


if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) != 2:
        print("Usage: python3 prog.py path/to/file.pdf")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        chunks = chunking(filepath)
        for chunk in chunks:
            print(json.dumps(chunk, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error processing file: {e}")
