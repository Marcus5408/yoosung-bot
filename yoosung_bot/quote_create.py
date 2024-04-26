from io import BytesIO
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from super_image import EdsrModel, ImageLoader


def create_image(pfp_url: str, username: str, discriminator: str, message: str):
    # Create a new black canvas
    canvas = Image.new("RGB", (1920, 1080), color="black")

    # get PFP from Discord and scale
    response = requests.get(pfp_url)
    pfp = Image.open(requests.get(pfp_url, stream=True).raw)

    ratio = 1080 / pfp.height
    model = EdsrModel.from_pretrained("eugenesiow/edsr-base", scale=ratio)
    inputs = ImageLoader.load_image(pfp)
    preds = model(inputs)

    ImageLoader.save_image(preds, "./tmp/scaled_pfp.png")
    ImageLoader.save_compare(inputs, preds, "./scaled_2x_compare.png")

    # Open the upscaled image
    scaled_image = Image.open("./tmp/scaled_pfp.png")

    # pfp = Image.open("./yoosung_bot/dokja.jpg") # Test PFP
    # scaled_image = pfp.resize((1080, 1080))

    # Paste the upscaled image on the left side
    canvas.paste(scaled_image, (-180, 0))

    # Apply gradient
    gradient = Image.open("./yoosung_bot/gradient.png")
    canvas.paste(gradient, (0, 0), mask=gradient)

    # Wrap message to max of 40 chars
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("./fonts/FOT-Rodin Pro DB.otf", 48)
    wrapped_text = textwrap.wrap(message, width=40)
    if discriminator[0] == "0":
        discriminator = ""
    else:
        discriminator = f"#{discriminator}"
    final_text = (
        '"'
        + "\n".join(wrapped_text)
        + f"\"\n\n- @{username}{discriminator}, {datetime.now().strftime('%Y')}"
    )

    # Calculate dimensions of a line of text
    line_dimensions = font.getbbox("hg" * 20)
    line_height = line_dimensions[3]
    line_width = line_dimensions[2]

    # Calculate coordinates for centering the text
    x = (canvas.width - line_width) / 2
    y = (canvas.height - (line_height * (len(wrapped_text) + 2))) / 2

    # Draw each line of wrapped text on the canvas
    line_x = x
    for line in final_text.split("\n"):
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        line_x = ((canvas.width - line_width) / 2) + 350
        draw.text((line_x, y), line, fill="white", font=font)
        y += line_height

    # Save the final image
    canvas.save("./tmp/output_image.jpg")

    return "./tmp/output_image.jpg"


# Testing function call
create_image(
    "https://cdn.discordapp.com/avatars/378650582639968276/58329e5647731e7b6f1e9a241a8e39af.png?size=1024",
    "Carmiscious",
    "400",
    "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway, because bees don't care what humans think is impossible.",
)
