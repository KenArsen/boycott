import glob
import os

from PIL import Image


class ImagesHandler:
    def __init__(self, path_image_directory, BASEWIDTH=800):
        """
        :BASEWIDTH - необходимая ширина картинки (по умолчанию 800px)
        :param path_image_directory: путь к папке (например, 'media/products/logos/foods/*')
        """
        self.path_image_directory = path_image_directory
        self.BASEWIDTH = BASEWIDTH

    def process_images(self) -> None:
        """Обрабатывает все изображения в указанной папке."""
        paths = self._load_file_paths()
        for path_current_img in paths:
            adapt_directory = self._create_new_adapt_directory(path_current_img)
            self._prepare_img(path_current_img, adapt_directory)

    def _load_file_paths(self) -> list:
        """Загружает все пути к изображениям в папке."""
        return glob.glob(self.path_image_directory)

    def _create_new_adapt_directory(self, path: str) -> str:
        """Создает папку 'compressed' внутри текущей папки с изображениями."""
        dir_path = os.path.dirname(os.path.realpath(path))
        new_directory = os.path.join(dir_path, "compressed")

        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)
        return new_directory

    def _prepare_img(self, path_current_img: str, adapt_directory: str) -> None:
        """Открывает изображение, сжимает и сохраняет."""
        with Image.open(path_current_img) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            if img.size[0] > self.BASEWIDTH:
                img = self._cut_image(img)

            filename = os.path.basename(path_current_img)
            self._compress_image(adapt_directory, filename, img)

    def _cut_image(self, image: Image.Image) -> Image.Image:
        """Обрезает изображение с сохранением пропорций."""
        wpercent = self.BASEWIDTH / float(image.width)
        hsize = int(float(image.height) * wpercent)
        return image.resize((self.BASEWIDTH, hsize), Image.Resampling.LANCZOS)

    def _compress_image(
        self, adapt_directory: str, filename: str, img: Image.Image
    ) -> None:
        """Сжимает изображение и сохраняет его в WebP."""
        filename = os.path.splitext(filename)[0]  # Убираем расширение
        adapt_path = os.path.join(adapt_directory, f"{filename}.webp")

        img.save(adapt_path, "WEBP", quality=80, method=6)
        print(f"✅ Сжато: {adapt_path}")


# 🔹 Использование:
handler = ImagesHandler("media/products/logos/medicine/*")
handler.process_images()
