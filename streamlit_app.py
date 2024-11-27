import streamlit as st
import nibabel as nib
import numpy as np
import os
import zipfile
from PIL import Image, ImageDraw

# Configuración de la aplicación
st.title("Procesador de Imágenes de CT para MedGan")

# Pestañas de la aplicación
tabs = st.tabs(["Descompresión de Archivos .nii", "Recorte de Imagen en Trapecio"])

# Pestaña 1: Descompresión de archivos .nii
with tabs[0]:
    st.header("Descomprimir Archivos .nii")
    uploaded_file = st.file_uploader("Sube un archivo .nii", type=["nii"])
    
    if uploaded_file is not None:
        st.write("Archivo subido con éxito.")
        nii_data = nib.load(uploaded_file)
        images = nii_data.get_fdata()
        
        # Convertir cada imagen del .nii a .png
        temp_folder = "temp_images"
        os.makedirs(temp_folder, exist_ok=True)
        
        st.write("Procesando imágenes...")
        for i in range(images.shape[2]):
            img = Image.fromarray(images[:, :, i].astype(np.uint8))
            img.save(f"{temp_folder}/image_{i}.png")
        
        st.success("Imágenes extraídas y guardadas temporalmente.")
        
        # Opción para descargar todas las imágenes como un archivo .zip
        if st.button("Descargar todas las imágenes como .zip"):
            zip_file = "images.zip"
            with zipfile.ZipFile(zip_file, 'w') as z:
                for file_name in os.listdir(temp_folder):
                    z.write(os.path.join(temp_folder, file_name), arcname=file_name)
            with open(zip_file, "rb") as f:
                st.download_button("Haz clic aquí para descargar el .zip", f, file_name="images.zip")
        
        # Seleccionar una imagen para descargar como .png
        image_index = st.number_input("Selecciona el índice de la imagen para descargar como .png", 0, images.shape[2]-1, 0)
        if st.button("Descargar imagen seleccionada"):
            selected_image = Image.fromarray(images[:, :, int(image_index)].astype(np.uint8))
            selected_image.save("selected_image.png")
            with open("selected_image.png", "rb") as f:
                st.download_button("Haz clic aquí para descargar la imagen .png", f, file_name="selected_image.png")

# Pestaña 2: Recorte de imagen en trapecio
with tabs[1]:
    st.header("Recorte de Imagen en Forma de Trapecio")
    uploaded_image = st.file_uploader("Sube una imagen para recortar", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        # Cargar la imagen y redimensionarla a 256x256
        image = Image.open(uploaded_image).convert("RGB")
        resized_image = image.resize((256, 256))
        st.image(resized_image, caption="Imagen Redimensionada", use_column_width=True)
        
        # Crear un recorte en forma de trapecio
        width, height = resized_image.size
        top_margin = width // 4
        bottom_margin = 0
        
        # Coordenadas del trapecio
        trap_coords = [(bottom_margin, 0), (width - bottom_margin, 0), (width - top_margin, height), (top_margin, height)]
        
        # Crear máscara para el recorte
        mask = Image.new("L", resized_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(trap_coords, fill=255)
        
        # Aplicar la máscara a la imagen
        trapezoid_image = Image.composite(resized_image, Image.new("RGB", resized_image.size, (0, 0, 0)), mask)
        st.image(trapezoid_image, caption="Imagen Recortada en Trapecio", use_column_width=True)
        
        # Descargar la imagen recortada
        if st.button("Descargar imagen recortada"):
            trapezoid_image.save("trapezoid_image.png")
            with open("trapezoid_image.png", "rb") as f:
                st.download_button("Haz clic aquí para descargar la imagen recortada", f, file_name="trapezoid_image.png")
