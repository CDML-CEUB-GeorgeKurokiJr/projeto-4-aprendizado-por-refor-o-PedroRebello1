import os
import glob
from PIL import Image, ImageDraw

def add_progress_bar(image: Image.Image, current_frame: int, total_frames: int, bar_height: int = 5, bar_color: str = "red") -> Image.Image:
    """
    Desenha uma barra de progresso na parte inferior da imagem.
    """
    img_copy = image.copy().convert("RGB")
    width, height = img_copy.size
    draw = ImageDraw.Draw(img_copy)
    
    # Calcula a largura da barra proporcional ao quadro atual
    if total_frames > 1:
        progress_ratio = current_frame / (total_frames - 1)
    else:
        progress_ratio = 1.0
        
    bar_width = int(width * progress_ratio)
    
    # Desenha o retângulo [x0, y0, x1, y1]
    draw.rectangle([0, height - bar_height, bar_width, height], fill=bar_color)
    
    return img_copy

def create_gif_from_images(input_pattern: str, output_filename: str, frame_duration_ms: int = 150) -> bool:
    """
    Cria um arquivo GIF animado com uma barra de progresso a partir de uma série de imagens.
    """
    try:
        file_list = glob.glob(input_pattern)

        if not file_list:
            print(f"Erro: Nenhum arquivo encontrado com o padrão '{input_pattern}'.")
            return False

        file_list.sort()
        print(f"Encontrados {len(file_list)} arquivos. Adicionando barra de progresso...")

        # Carrega e processa todas as imagens
        total_frames = len(file_list)
        processed_images = []
        
        for i, file_path in enumerate(file_list):
            with Image.open(file_path) as img:
                processed_img = add_progress_bar(img, i, total_frames, bar_height=3, bar_color="#00FF00")
                processed_images.append(processed_img)

        # Salva o arquivo final
        processed_images[0].save(
            output_filename,
            save_all=True,
            append_images=processed_images[1:],
            duration=frame_duration_ms,
            loop=0
        )

        print(f"Sucesso: GIF salvo como '{output_filename}'.")
        return True

    except Exception as e:
        print(f"Erro ao processar as imagens: {e}")
        return False

if __name__ == "__main__":
    padrao_arquivos = "./samples_only/samples_epoch_*.png"
    nome_saida = "animacao_epochs_com_progresso.gif"
    duracao_quadro = 100
    
    create_gif_from_images(padrao_arquivos, nome_saida, duracao_quadro)