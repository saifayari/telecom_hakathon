import os
from PIL import Image
import numpy as np

def examine_checkerboard(image_path):
    im = Image.open(image_path)
    # Check top-left 32x32 patch
    crop = im.crop((0, 0, 64, 64))
    arr = np.array(crop)
    print(f"File: {os.path.basename(image_path)}")
    print("Min color:", np.min(arr, axis=(0, 1)))
    print("Max color:", np.max(arr, axis=(0, 1)))
    print("Mean color:", np.mean(arr, axis=(0, 1)).astype(int))
    # Unique colors in the top-left 32x32
    uniq = np.unique(arr.reshape(-1, 3), axis=0)
    print(f"Num unique colors in 64x64 corner: {len(uniq)}")
    # Print the most frequent colors
    colors, counts = np.unique(arr.reshape(-1, 3), return_counts=True, axis=0)
    top_indices = np.argsort(-counts)[:5]
    for idx in top_indices:
        print(f"  Color {colors[idx]} count: {counts[idx]}")

examine_checkerboard(r"art (2)\art\agent_new\Gemini_Generated_Image_8ezuri8ezuri8ezu (1).jpg")
examine_checkerboard(r"art (2)\art\monsters\Gemini_Generated_Image_a7f8nwa7f8nwa7f8.jpg")
examine_checkerboard(r"art (2)\art\Drone\Gemini_Generated_Image_4ti7g44ti7g44ti7.jpg")
examine_checkerboard(r"art (2)\art\Gun\Gemini_Generated_Image_1tg6gq1tg6gq1tg6.jpg")
examine_checkerboard(r"art (2)\art\monsters\Gemini_Generated_Image_gbfa28gbfa28gbfa.jpg")
