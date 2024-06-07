import cv2
import numpy as np


def apply_threshold(image_path, threshold):
    # 이미지 읽기 (컬러 이미지로 읽기)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("이미지를 읽을 수 없습니다. 경로를 확인하세요.")

    # 이미지 밝기 계산 (RGB -> GRAY 변환)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 밝기 임계값 적용
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # 마스크를 컬러 채널에 맞게 변경
    mask_3channel = cv2.merge([mask, mask, mask])

    # 원본 이미지에서 어두운 픽셀을 검정색으로 변경
    result = cv2.bitwise_and(image, mask_3channel)

    return result


# image_path = 'Mel_VAD_TTS_record.jpg'
# threshold = 100  # 밝기 임계값
# result_image = apply_threshold(image_path, threshold)
#
# output_path = 'result_image.jpg'
# cv2.imwrite(output_path, result_image)
