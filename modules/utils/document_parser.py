
import easyocr
import cv2
import pytesseract


class OCRProcessor:
    def __init__(self, use_easyocr=False, lang='eng'):
        """
        Initializes the OCR Processor.
        :param use_easyocr: If True, uses EasyOCR instead of Tesseract.
        :param lang: Language for OCR (default is English).
        """
        self.use_easyocr = use_easyocr
        self.lang = lang
        self.reader = easyocr.Reader([lang]) if use_easyocr else None

    def preprocess_image(self, image_path):
        """Preprocess image to enhance OCR accuracy."""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def extract_text(self, image_path, config: str = ''):
        """Extracts text from an image using OCR."""
        image = self.preprocess_image(image_path)

        if self.use_easyocr:
            results = self.reader.readtext(image)
            return " ".join([text[1] for text in results])
        else:
            config_map ={
                'OSD': '--psm 0',
                'Auto segmentation + OSD': '--psm 1',
                'Auto segmentation - OSD/OCR': '--psm 2',
                'Auto segmentation + OCR': '--psm 3',
                'Single Column Multi-size Text': '--psm 4',
                'Vertical Text': '--psm 5',
                'Text Block': '--psm 6',
                'Single Line': '--psm 7',
                'Single Word': '--psm 8',
                'Single Word in Circle': '--psm 9',
                'Single Character': '--psm 10',
                'Sparse Text': '--psm 11',
                'Sparse Text + OSD': '--psm 12',
                'Raw Line': '--psm 13',
            }
            return pytesseract.image_to_string(image, lang=self.lang, config=config_map[config])
