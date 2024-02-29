import dis
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap

def create_image(pfp_url: str, username: str, discriminator: str,message: str):
    # download the pfp from discord
    # response = requests.get(pfp_url)
    # pfp = Image.open(BytesIO(response.content))

    # Load the original image
    pfp = Image.open("./yoosung_bot/dokja.jpg")

    # Upscale the image to 1080p
    scaled_image = pfp.resize((1080, 1080))

    # Create a black canvas
    canvas = Image.new("RGB", (1920, 1080), color="black")

    # Paste the upscaled image on the left side
    canvas.paste(scaled_image, (-180, 0))

    # Add dip-to-black on the right on top of the image
    # Load the gradient image
    gradient = Image.open("./yoosung_bot/gradient.png")

    # Overlay the gradient image on the canvas
    canvas.paste(gradient, (0, 0), mask=gradient)

    # add black
    # black_area_width = 1920 - scaled_image.width
    # black_area = Image.new("RGB", (black_area_width, 1080), color="black")
    # canvas.paste(black_area, (scaled_image.width, 0))

    # Add custom text to the right side
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("./fonts/FOT-Rodin Pro DB.otf", 48)  # Choose your font and size
    # Wrap the text by word with a maximum of 80 characters per line
    wrapped_text = textwrap.wrap(message, width=40)
    if discriminator[0] == "0":
        discriminator = ""
    else:
        discriminator = f"#{discriminator}"
    final_text = "\"" + "\n".join(wrapped_text) + f"\"\n\n- @{username}{discriminator}, 2023"

    # Calculate the height of each line based on the font size
    line_dimensions = font.getbbox("hg" * 20)
    line_height = line_dimensions[3]
    line_width = line_dimensions[2]

    # Calculate the starting x-coordinate for the text to be centered horizontally
    x = ((canvas.width - line_width) / 2)

    # Calculate the starting y-coordinate for the text to be centered vertically
    y = (canvas.height - (line_height * (len(wrapped_text) + 2))) / 2

    # Calculate the starting x-coordinate for each line to be centered horizontally
    line_x = x

    # Draw each line of wrapped text on the canvas
    for line in final_text.split('\n'):
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        line_x = ((canvas.width - line_width) / 2) + 350
        draw.text((line_x, y), line, fill="white", font=font)
        y += line_height

    # Save the final image
    canvas.save("./tmp/output_image.jpg")

    # Show the image (optional)
    canvas.show()

    return "./tmp/output_image.jpg"

# create_image("https://cdn.discordapp.com/avatars/378650582639968276/58329e5647731e7b6f1e9a241a8e39af.png", 
#              "Carmiscious",
#              "0",
#              "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway, because bees don't care what humans think is impossible.")