import json
import os
import shutil

# Категории для фильтрации
cat_data = [
    "0e66115c-9b5e-482b-a0d7-cdb05eeeb41e",
    "18090415-9db0-430d-ada7-a0a2492cb175",
    "46c1d713-3878-45b2-a723-a46d59ecd223",
    "5f094711-7354-4486-8364-3a41dfea0be5",
    "65c78212-c110-42b7-82d1-35439836812d",
    "821e87d7-b671-4f1c-bb83-14ac59689401",
    "8a3d6f31-8371-4dc7-8e7f-d9f9775516d2",
    "8a738b29-80c9-46de-952c-68bff27b2002",
    "aa40d1f1-5ccd-4ffa-9052-326015a76c59",
    "d8cf1304-3c9c-409a-bf5b-7bc3739e939a",
]

cat_data_dict = {
    "0e66115c-9b5e-482b-a0d7-cdb05eeeb41e": "accessories",
    "18090415-9db0-430d-ada7-a0a2492cb175": "hygienic-cosmetics",
    "46c1d713-3878-45b2-a723-a46d59ecd223": "clothes",
    "5f094711-7354-4486-8364-3a41dfea0be5": "home-appliances",
    "65c78212-c110-42b7-82d1-35439836812d": "sports-equipment",
    "821e87d7-b671-4f1c-bb83-14ac59689401": "cosmetics",
    "8a3d6f31-8371-4dc7-8e7f-d9f9775516d2": "foods",
    "8a738b29-80c9-46de-952c-68bff27b2002": "chemical-repellents",
    "aa40d1f1-5ccd-4ffa-9052-326015a76c59": "medicine",
    "d8cf1304-3c9c-409a-bf5b-7bc3739e939a": "technology",
}

# Пути к папкам
source_dir = "/Users/kgz/Documents/media"  # Здесь находятся оригинальные изображения
destination_dir = "media/products/"  # Куда копировать с новым именем

# Загрузка исходного JSON
with open("apps/product/fixtures/product.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Преобразование структуры данных
transformed_data = []
for item in data:
    if item["fields"]["category"] in cat_data:
        pk = item["pk"]
        category_slug = cat_data_dict[item["fields"]["category"]]
        old_image_name = item["fields"].get("logo", "")  # Получаем имя файла
        new_image_name = f"products/logos/{category_slug}/{pk}.jpg"  # Используем слаг категории и pk для нового имени

        # Полный путь к файлам
        old_image_path = os.path.join(source_dir, old_image_name)
        new_image_path = os.path.join(destination_dir, new_image_name)

        # Проверяем, существует ли файл и копируем его
        if os.path.isfile(old_image_path):
            os.makedirs(
                os.path.dirname(new_image_path), exist_ok=True
            )  # Создаем каталоги, если их нет
            shutil.copy2(old_image_path, new_image_path)

            # Устанавливаем права доступа -rw-r--r--
            os.chmod(new_image_path, 0o644)
        else:
            print(f"⚠️ Файл {old_image_path} не найден!")

        # Добавляем данные в новый JSON
        transformed_item = {
            "model": "product.product",
            "pk": pk,
            "fields": {
                "category": item["fields"]["category"],
                "name": item["fields"]["brand"],
                "name_en": item["fields"]["brand"],
                "name_ru": item["fields"]["brand"],
                "name_kg": item["fields"]["brand"],
                "description": item["fields"]["description"],
                "description_en": item["fields"]["description_en"],
                "description_ru": item["fields"]["description_ru"],
                "description_kg": item["fields"]["description_kg"],
                "image": new_image_name,  # Добавляем путь к новому файлу
                "is_boycotted": item["fields"]["status"],
                "is_kyrgyz_product": False,
                "alternative_products": item["fields"]["alternatives"],
                "created_at": "2025-01-28T12:00:00Z",
                "updated_at": "2025-01-28T12:00:00Z",
            },
        }
        transformed_data.append(transformed_item)

print(f"✅ Обработано {len(transformed_data)} записей.")

# Сохранение в новый JSON-файл
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(transformed_data, file, ensure_ascii=False, indent=4)

print("✅ Данные успешно преобразованы и сохранены в output.json")
