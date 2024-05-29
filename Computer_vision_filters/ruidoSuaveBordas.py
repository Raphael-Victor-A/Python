import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from skimage import io, filters
from skimage.filters import sobel, roberts, laplace
from skimage.color import rgb2gray
from skimage.util import random_noise
import numpy as np


def apply_noise(image, noise_type, kernel_size=None):
    if noise_type == 'Gaussian':
        return random_noise(image, mode='gaussian')

    elif noise_type == "Salt & Pepper":
        row, col = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        coords = np.array(coords)
        coords[0, coords[0] >= row] = row - 1
        coords[1, coords[1] >= col] = col - 1
        out[coords[0], coords[1]] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        coords = np.array(coords)
        coords[0, coords[0] >= row] = row - 1
        coords[1, coords[1] >= col] = col - 1
        out[coords[0], coords[1]] = 0
        return out

    elif noise_type == "Poisson":
        if kernel_size is None:
            kernel_size = 15 # Valor padrão se o tamanho do kernel não for fornecido
        scale_factor = 10 # Ajuste este valor para aumentar o grau de ruído
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * scale_factor / kernel_size, size=image.shape) / float(vals)
        return noisy

    else:
        print(f'Noise type {noise_type} not implemented')
        return image



def apply_smoothing(image, smoothing_type, kernel_size):
    if smoothing_type == "Gaussian":
        kernel = cv2.getGaussianKernel(kernel_size, 0)
        kernel = np.outer(kernel, kernel.transpose())
        return cv2.filter2D(image, -1, kernel)

    elif smoothing_type == "Median":
        normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        uint8_image = normalized_image.astype(np.uint8)
        median_result = cv2.medianBlur(uint8_image, kernel_size)
        return median_result

    elif smoothing_type == "Average":
        return cv2.blur(image, (kernel_size, kernel_size))

    else:
        print(f'Smoothing type {smoothing_type} not implemented')
        return image


def apply_edge_detection(image, edge_detection_type):
    if edge_detection_type == "Sobel":
        # Definindo os kernels Sobel para detecção de bordas
            sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) #convolução
            sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        # Aplicando os kernels Sobel usando filter2D
            grad_x = cv2.filter2D(image, -1, sobel_x)
            grad_y = cv2.filter2D(image, -1, sobel_y)
        
        # Calculando a magnitude do gradiente
            magnitude = np.sqrt(grad_x**2 + grad_y**2)
      
        

            return magnitude

    elif edge_detection_type == "Roberts":
        return roberts(image)

    elif edge_detection_type == "Laplace":
      normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
      uint8_image = normalized_image.astype(np.uint8)
      lap = cv2.Laplacian(uint8_image, cv2.CV_16S, ksize=5)
      
      return lap

    else:
        print(f'Edge detection type {edge_detection_type} not implemented')
        return image


def display_image(image):
    # Convertendo a imagem para o formato correto para exibição
    cv2.imwrite('imagemProcessada.png', image)
    image = Image.fromarray((image * 255).astype(np.uint8))  # Convertendo para 8 bits
    # Mostrando a imagem em uma janela tkinter
    
    image.show()


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        # Carregando a imagem inicial
        self.image = None
        self.load_image_button = tk.Button(root, text="Carregar Imagem", command=self.load_image)
        self.load_image_button.pack(pady=10)

        # Opções de processamento
        self.processing_options = {
            "Noise": ["Gaussian", "Salt & Pepper", "Poisson"],
            "Smoothing": ["Gaussian", "Median", "Average"],
            "Edge Detection": ["Sobel", "Roberts", "Laplace"]
        }

        self.selected_processing_options = {
            "Noise": tk.StringVar(),
            "Smoothing": tk.StringVar(),
            "Edge Detection": tk.StringVar()
        }

        self.create_processing_options()

        # Botão de processamento
        self.process_button = tk.Button(root, text="Processar Imagem", command=self.process_image)
        self.process_button.pack(pady=10)

    def create_processing_options(self):
        for option, values in self.processing_options.items():
            frame = tk.LabelFrame(self.root, text=option)
            frame.pack(padx=10, pady=5, fill="both", expand="yes")

            option_menu = tk.OptionMenu(frame, self.selected_processing_options[option], *values)
            option_menu.pack()

    def load_image(self):
        filename = filedialog.askopenfilename(title="Selecione uma imagem",
                                              filetypes=(("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp"),
                                                         ("Todos os Arquivos", "*.*")))
        if filename:
            self.image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    def process_image(self):
        if self.image is None:
            messagebox.showerror("Erro", "Por favor, carregue uma imagem primeiro!")
            return

    # Obtendo as opções selecionadas
        noise_option = self.selected_processing_options["Noise"].get()
        smoothing_option = self.selected_processing_options["Smoothing"].get()
        edge_detection_option = self.selected_processing_options["Edge Detection"].get()

    # Aplicando o processamento de imagem
        processed_image = self.image.copy()

    # Aplicar ruído
        if noise_option == "Poisson":
            processed_image = apply_noise(processed_image, noise_option, kernel_size=5) # Ajuste o kernel_size conforme necessário
        else:
            processed_image = apply_noise(processed_image, noise_option)

        display_image(processed_image)

    # Aplicar suavização
        processed_image = apply_smoothing(processed_image, smoothing_option, kernel_size=51) # Ajuste o kernel_size conforme necessário
        display_image(processed_image)

    # Aplicar detecção de borda
        processed_image = apply_edge_detection(processed_image, edge_detection_option)

    # Exibindo a imagem processada
        display_image(processed_image)


def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
