import pytesseract
import imutils
import cv2
from difflib import SequenceMatcher


def similar(a, b):
    # return between 0 and 1
    # 1 is identical, 0 is completely different
    return SequenceMatcher(None, a, b).ratio()


def extract_text(img_path, show=False):
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=500, height=500)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    results = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng')

    for i in range(0, len(results["text"])):
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        text = results["text"][i]
        conf = int(results["conf"][i])

        if conf > 0:
            text = "".join(text).strip()
            cv2.rectangle(img,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255), 2)

    if show:
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    return ' '.join([i for i in results['text'] if len(i) > 0])


def actual_text(path):
    lines = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line[3:]      # remove "1: "
            line = line.strip()
            lines.append(line)

    return ' '.join(lines)


# i: 1-21
def comparing(i):
    label = actual_text(f'./training-strips/labels/cartoon{i}.txt')
    ocr = extract_text(f'./training-strips/images/cartoon{i}.png')
    return similar(label, ocr)


if __name__ == "__main__":
    # path = "./training-strips/images/cartoon1.png"
    # t = extract_text(path, show=False)
    # print(t)

    # a = actual_text("./training-strips/labels/cartoon1.txt")
    # print(a)

    accs = []
    for i in range(1, 22):
        acc = comparing(i)
        print(f"cartoon{i}: {acc}")
        accs.append(acc)

    print(f"\naverage: {sum(accs) / len(accs)}")
