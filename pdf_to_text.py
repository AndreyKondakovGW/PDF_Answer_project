from PyPDF2 import PdfReader, PdfWriter
from pix2tex.cli import LatexOCR
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
from PIL import Image
import os
from pdf2image import convert_from_path

MODEL = LatexOCR()

def text_extraction(element):
    line_text = element.get_text()
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    return (line_text, format_per_line)

def crop_image(element, pageObj, page_size):
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1]
    print(f'Image coordinates are {image_left, image_top, image_right, image_bottom}')
    #print(f'Page coordinates are {pageObj.mediabox.lower_left[0],pageObj.mediabox.upper_right[1], pageObj.mediabox.upper_right[0], pageObj.mediabox.lower_left[1]}')
    #page_size = abs(pageObj.mediabox.upper_right[0] - pageObj.mediabox.lower_left[0])*abs(pageObj.mediabox.lower_left[1] - pageObj.mediabox.upper_right[1]) 
    image_size = abs(image_right - image_left)*abs(image_bottom - image_top)

    print(f'Image/page ration is {image_size/float(page_size)}')
    pageObj_clone = pageObj
    offset = 2
    pageObj_clone.mediabox.lower_left = (image_left - offset, image_bottom + offset)
    pageObj_clone.mediabox.upper_right = (image_right + offset, image_top - offset)
    cropped_pdf_writer = PdfWriter()
    cropped_pdf_writer.add_page(pageObj_clone)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)
    return image_size/float(page_size)

def convert_to_images(input_file, output_file = "PDF_image.png"):
    images = convert_from_path(input_file, poppler_path='E:\Programming\poppler-23.11.0\Library\\bin')
    image = images[0]
    #output_file 
    image.save(output_file, "PNG")

def image_to_text(image_path):
    # Read the image
    img = Image.open(image_path)
    # Extract the text from the image
    text = MODEL(img)
    return f'${text}$'

def pdf_to_text(pdf_file):
    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PdfReader(pdf_file)
    text = ""
    images = []
    for pagenum, page in enumerate(extract_pages(pdf_file)):
        pageObj = pdfReader.pages[pagenum]
        page_size = abs(pageObj.mediabox.upper_right[0] - pageObj.mediabox.lower_left[0])*abs(pageObj.mediabox.lower_left[1] - pageObj.mediabox.upper_right[1])
        page_text = [f'\n Page {pagenum+1}: \n']
        print(f'Page {pagenum+1}')
        page_content = []
        page_elements = [(element.y1, element) for element in page._objs]
        page_elements.sort(key=lambda a: a[0], reverse=True)
        num_images = 0
        num_formulas = 0
        if pagenum == 0:
            continue
        for i,component in enumerate(page_elements):
            
            pos= component[0]
            element = component[1]

            print(f'Element {i} at {pos} is {element}')
            if isinstance(element, LTTextContainer):
                (line_text, _) = text_extraction(element)
                page_text.append(line_text)

            if isinstance(element, LTFigure):
                page_image_ratio = crop_image(element, pageObj, page_size)
                if page_image_ratio < 0.08:
                    convert_to_images('cropped_image.pdf')
                    convert_to_images('cropped_image.pdf', f'./formulas/page{pagenum+1}_formula{num_formulas}.png')
                    image_text = '\n' +image_to_text('PDF_image.png') + '\n'
                    num_formulas += 1
                else:
                    convert_to_images('cropped_image.pdf', f'./images/page{pagenum+1}_img{num_images}.png')
                    image_text = f'<img src=./images/page{pagenum+1}_img{num_images}.png>'
                    num_images += 1
                page_text.append(image_text)

            if isinstance(element, LTRect):
                page_content.append('tabel')
        text += '\n'.join(page_text)
    pdfFileObj.close()
    os.remove('cropped_image.pdf')
    os.remove('PDF_image.png')

    return text



if __name__ == "__main__":
    """ pdf_text = pdf_to_text("./pdf_examples/5_Random_processes_2.pdf")
    #save text as md file
    with open('pdf_text.md', 'w', encoding="utf-8") as f:
        f.write(pdf_text) """
    
    img = Image.open("example.png")
    # Extract the text from the image
    text = MODEL(img)
    print(text)
