from imaginepy import Imagine, Style, Ratio

def imagine(prompt):
    imagine = Imagine()

    img_data = imagine.sdprem(
        prompt=prompt,
        style=Style.ANIME_V2,
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
        with open("example.jpeg", mode="wb") as img_file:
            pic = img_file.write(img_data)
            return pic
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")