import io
import torch
import logging
import numpy as np
from matplotlib import pyplot as plt
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import streamlit as st

# Suppress unnecessary warnings
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

class DetrObjectDetection:
    def __init__(self, model_name="facebook/detr-resnet-50", threshold=0.9):
        # Load the pretrained DETR model and processor
        self.processor = DetrImageProcessor.from_pretrained(model_name)
        self.model = DetrForObjectDetection.from_pretrained(model_name)
        self.threshold = threshold

        # COCO_CLASSES for mapping detected labels to human-readable names
        self.COCO_CLASSES = [
            "__background__", "person", "bicycle", "car", "motorcycle", "airplane", "bus",
            "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
            "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
            "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
            "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
            "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
            "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
            "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
            "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
            "toilet", "TV", "laptop", "mouse", "remote", "keyboard", "cell phone",
            "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock",
            "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
        ]

    def load_image(self, uploaded_file):
        # Open the image and convert it to RGB
        self.raw_image = uploaded_file
        self.image = uploaded_file.convert("RGB")
        return self.image

    def preprocess_image(self):
        # Preprocess the image
        self.inputs = self.processor(images=self.image, return_tensors="pt")
        return self.inputs

    def run_inference(self):
        # Perform inference
        self.model.eval()
        with torch.no_grad():
            self.outputs = self.model(**self.inputs)
        return self.outputs

    def process_outputs(self):
        # Process model outputs
        target_sizes = torch.tensor([self.image.size[::-1]])  # Original image size (H, W)
        self.results = self.processor.post_process_object_detection(self.outputs, target_sizes=target_sizes, threshold=self.threshold)
        return self.results

    def print_results(self):
        # Print detected objects with labels, scores, and bounding boxes
        for result in self.results:
            logging.info("Detected objects:")
            for score, label, box in zip(result["scores"], result["labels"], result["boxes"]):
                class_name = self.COCO_CLASSES[label]  # Get the class name
                logging.info(f"Class: {class_name}, Score: {score:.2f}, Box: {box.tolist()}")

    def visualise_prediction(self, results):
        """
        Generate and return the image with bounding boxes and labels.
        Overlay the bounding boxes on top of the original image.
        """
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.imshow(self.image)  # Display the original image
        color_map = {}

        # Iterate over the results and draw bounding boxes and labels
        for result in results:
            keep = result["scores"] > self.threshold
            boxes = result["boxes"][keep].tolist()
            scores = result["scores"][keep].tolist()
            labels = result["labels"][keep].tolist()

            for score, (xmin, ymin, xmax, ymax), label in zip(scores, boxes, labels):
                class_name = self.COCO_CLASSES[label]
                if label not in color_map:
                    color_map[label] = np.random.rand(3)

                # Draw bounding box
                ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, color=color_map[label], linewidth=3))
                ax.text(xmin, ymin, f"{class_name}: {score:.2f}", fontsize=15, bbox=dict(facecolor="yellow", alpha=0.5))

        # Hide axes for better visualization
        ax.axis("off")

        # Save the plot to a buffer and return as a PIL image
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        labeled_image = Image.open(buf)
        plt.close(fig)  # Close the figure to release resources
        return labeled_image

    def detect_objects(self, uploaded_file):
        self.load_image(uploaded_file)
        self.preprocess_image()
        self.run_inference()
        self.process_outputs()
        labeled_image = self.visualise_prediction(self.results)

        return labeled_image, self.results