import cv2
import pytesseract


class OCRExtractor:
    def __init__(self, lang='eng'):
        """
        Initializes the OCR Processor.
        :param lang: Language for OCR (default is English).
        """
        self.lang = lang

    def preprocess_image(self, image_path):
        """Preprocess image to enhance OCR accuracy."""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def extract_text(self, image_path, config: str = ''):
        """Extracts text from an image using OCR."""
        image = self.preprocess_image(image_path)

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

