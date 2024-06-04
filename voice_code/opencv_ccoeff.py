import cv2

def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"이미지가 존재하지 않습니다: {image_path}")
    return img
def compare_image(img1_path,img2_path):
    img1 = load_image(img1_path)
    img2 = load_image(img2_path)
    print(img1_path)
    result = cv2.matchTemplate(img2,img1, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    print(max_val)
    return max_val



if __name__ == "__main__":
    compare_image("Mel_VAD_TTS_record.jpg", "Mel_VAD_record.jpg")