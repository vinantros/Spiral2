from imaginepy import Imagine, Style, Ratio
from io import BytesIO

def imagine(prompt):
    """
    Generate an image based on the given prompt using the Imagine library. 
    
    Args:
    prompt (str): The text prompt to use for generating the image.
    
    Returns:
    BytesIO: A file containing the generated image data, stored in memory. None is returned if there was an error while generating or upscaling the image.
    """
    imagine = Imagine()

    img_data = imagine.sdprem(
        prompt=prompt,
        style=Style.IMAGINE_V4_Beta,
        ratio=Ratio.RATIO_16X9
    )

    if img_data is None:
        print("An error occurred while generating the image.")
        return

    img_data = imagine.upscale(image=img_data)

    if img_data is None:
        print("An error occurred while upscaling the image.")
        return

    try:
        # Use BytesIO to store the image data in memory
        img_file = BytesIO(img_data)
        return img_file
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")