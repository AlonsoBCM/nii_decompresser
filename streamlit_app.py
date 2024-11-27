import streamlit as st
import nibabel as nib
import numpy as np
from PIL import Image
import random

# Configuración de la aplicación
st.title("Procesador de Archivos .nii")

# Subir archivo .nii
uploaded_file = st.file_uploader("Sube un archivo .nii", type=["nii"])

if uploaded_file is not None:
    st.write("Archivo subido con éxito. Procesando...")

    # Cargar el archivo .nii
    nii_data = nib.load(uploaded_file)
    images = nii_data.get_fdata()

    st.write(f"Dimensiones del archivo: {images.shape}")

    # Seleccionar una imagen aleatoria del .nii
    slice_index = random.randint(0, images.shape[2] - 1)
    st.write(f"Mostrando una imagen aleatoria: índice {slice_index}")

    # Convertir la imagen seleccionada en un formato visualizable
    random_image = images[:, :, slice_index].astype(np.uint8)
    pil_image = Image.fromarray(random_image)
    st.image(pil_image, caption=f"Imagen del índice {slice_index}", use_column_width=True)

    # Botón para descargar la imagen seleccionada
    if st.button("Descargar esta imagen como .png"):
        pil_image.save("random_image.png")
        with open("random_image.png", "rb") as f:
            st.download_button("Haz clic aquí para descargar la imagen", f, file_name="random_image.png")
