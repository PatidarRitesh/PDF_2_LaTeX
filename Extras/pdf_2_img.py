

from pdf2image import convert_from_path

def pdf_to_images(pdf_path, image_folder):
    # Convert PDF to list of PIL images
    images = convert_from_path(pdf_path)

    # Create the output folder if it doesn't exist
    os.makedirs(image_folder, exist_ok=True)

    # Save each image to the output folder
    for i, image in enumerate(images):
        image_path = f"{image_folder}/page_{i + 1}.png"
        image.save(image_path, 'PNG')

# Example usage
pdf_path = "/content/path/to/your/file.pdf"
image_folder = "/content/path/to/your/output/folder"

pdf_to_images(pdf_path, image_folder)
