
from PIL import Image, ImageDraw, ImageFont
idea = "Cover for \nYoutube video \nabout Python"
background_image = "images/image.webp"

# Load the background image
background = Image.open(background_image)

# Initialize the drawing context with the background as canvas
draw = ImageDraw.Draw(background)

# Define the text to add and the font
text = idea
font = ImageFont.truetype("arial.ttf", size=45)

# Define the position for the text
text_position = (100, 100)

# Add text to image
draw.text(text_position, text, font=font, fill="white")

# Save the edited image
background.save("youtube_cover_python.png")
