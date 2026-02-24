"""
ماژول برای دریافت لیست مدل‌های Ollama و تبدیل آن‌ها به Enum
"""

import requests
from enum import Enum
from typing import Type
from functools import lru_cache


@lru_cache(maxsize=128)
def fetch_ollama_models(base_url: str = "http://localhost:11434") -> tuple[str, ...]:
    """
    دریافت لیست مدل‌های موجود از Ollama (با cache برای جلوگیری از API call‌های اضافی)
    
    Args:
        base_url: آدرس پایه سرور Ollama (پیش‌فرض: http://localhost:11434)
    
    Returns:
        تاپلی از نام مدل‌های موجود (tuple برای hashable بودن در cache)
    
    Raises:
        requests.RequestException: در صورت بروز خطا در ارتباط با سرور
    
    Note:
        نتایج این تابع cache می‌شوند. برای پاک کردن cache از fetch_ollama_models.cache_clear() استفاده کنید.
    """
    try:
        # ارسال درخواست به endpoint مدل‌های Ollama
        response = requests.get(f"{base_url}/api/tags")
        response.raise_for_status()
        
        # استخراج نام‌های مدل از پاسخ JSON
        data = response.json()
        models = [model["name"] for model in data.get("models", [])]
        
        # تبدیل به tuple برای hashable بودن در cache
        return tuple(models)
    except requests.RequestException as e:
        raise Exception(f"خطا در دریافت مدل‌ها از Ollama: {e}")


def create_ollama_models_enum(
    models: list[str] | None = None,
    enum_name: str = "OllamaModels"
) -> Type[Enum]:
    """
    ساخت یک Enum از لیست مدل‌های Ollama
    
    Args:
        models: لیست نام مدل‌ها (در صورت None، به صورت خودکار از Ollama دریافت می‌شود)
        enum_name: نام Enum مورد نظر (پیش‌فرض: OllamaModels)
    
    Returns:
        کلاس Enum شامل تمام مدل‌های موجود
    
    Example:
        >>> Models = create_ollama_models_enum()
        >>> print(Models.LLAMA2.value)
        'llama2'
    """
    # اگر لیست مدل‌ها داده نشده، از Ollama دریافت کن
    if models is None:
        models = fetch_ollama_models()
    
    # ساخت دیکشنری برای Enum
    # نام مدل را به فرمت uppercase و با جایگزینی کاراکترهای غیرمجاز تبدیل می‌کنیم
    enum_dict = {}
    for model in models:
        # تبدیل نام مدل به فرمت مناسب برای نام Enum
        # مثلاً "llama2:latest" به "LLAMA2_LATEST"
        enum_key = model.upper().replace(":", "_").replace("-", "_").replace(".", "_")
        enum_dict[enum_key] = model
    
    # ساخت Enum به صورت dynamic
    return Enum(enum_name, enum_dict)


def clear_models_cache() -> None:
    """
    پاک کردن cache مدل‌های ذخیره شده
    
    از این تابع زمانی استفاده کنید که می‌خواهید لیست مدل‌ها را از Ollama مجدداً دریافت کنید
    (مثلاً بعد از نصب یا حذف مدل جدید)
    
    Example:
        >>> clear_models_cache()
        >>> OllamaModels = get_ollama_models_enum()  # لیست جدید را از Ollama می‌گیرد
    """
    fetch_ollama_models.cache_clear()


def get_ollama_models_enum(base_url: str = "http://localhost:11434") -> Type[Enum]:
    """
    تابع کمکی برای دریافت مستقیم Enum مدل‌های Ollama
    
    Args:
        base_url: آدرس پایه سرور Ollama
    
    Returns:
        کلاس Enum شامل تمام مدل‌های موجود در Ollama
    
    Example:
        >>> OllamaModels = get_ollama_models_enum()
        >>> for model in OllamaModels:
        >>>     print(f"{model.name} -> {model.value}")
    """
    models = fetch_ollama_models(base_url)
    return create_ollama_models_enum(models)


if __name__ == "__main__":
    # مثال استفاده
    try:
        # دریافت Enum مدل‌های Ollama
        OllamaModels = get_ollama_models_enum()
        
        print("مدل‌های موجود در Ollama:")
        print("-" * 50)
        
        # نمایش تمام مدل‌ها
        for model in OllamaModels:
            print(f"{model.name:30} -> {model.value}")
        
        print("\n" + "=" * 50)
        print(f"تعداد کل مدل‌ها: {len(OllamaModels)}")
        
    except Exception as e:
        print(f"خطا: {e}")
