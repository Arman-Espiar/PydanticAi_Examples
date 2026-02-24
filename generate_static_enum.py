"""
اسکریپت تولید خودکار Enum استاتیک برای مدل‌های Ollama

این اسکریپت:
۱. لیست مدل‌های موجود را از Ollama دریافت می‌کند
۲. کد Python برای یک Enum استاتیک تولید می‌کند
۳. فایل ollama_models_static.py را ایجاد/به‌روزرسانی می‌کند

استفاده:
    python generate_static_enum.py

توجه:
    هر بار که مدل جدیدی با `ollama pull` نصب می‌کنید،
    این اسکریپت را دوباره اجرا کنید تا فایل به‌روزرسانی شود.
"""

from pathlib import Path
from datetime import datetime
from ollama_models_enum import fetch_ollama_models


def sanitize_enum_name(model_name: str) -> str:
    """
    تبدیل نام مدل به فرمت مناسب برای نام Enum
    
    Args:
        model_name: نام اصلی مدل (مثلاً "llama2:latest")
    
    Returns:
        نام مناسب برای Enum (مثلاً "LLAMA2_LATEST")
    
    مثال:
        >>> sanitize_enum_name("gemma3:12b")
        'GEMMA3_12B'
        >>> sanitize_enum_name("hf.co/tencent/model:tag")
        'HF_CO_TENCENT_MODEL_TAG'
    """
    # تبدیل به uppercase و جایگزینی کاراکترهای غیرمجاز با _
    return (
        model_name
        .upper()
        .replace(":", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
    )


def generate_enum_code(models: tuple[str, ...]) -> str:
    """
    تولید کد Python برای Enum استاتیک
    
    Args:
        models: تاپل نام‌های مدل
    
    Returns:
        کد Python کامل برای فایل ollama_models_static.py
    """
    # هدر فایل
    header: str = f'''"""
Enum استاتیک مدل‌های Ollama

**هشدار:** این فایل به صورت خودکار توسط اسکریپت generate_static_enum.py تولید شده است.
این فایل را به صورت دستی ویرایش نکنید!

برای به‌روزرسانی بعد از نصب مدل جدید:
    python generate_static_enum.py

تاریخ تولید: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
تعداد مدل‌ها: {len(models)}
"""

from enum import Enum


class OllamaModels(Enum):
    """
    مدل‌های Ollama موجود در سیستم
    
    این Enum به صورت استاتیک تعریف شده تا IDE ها بتوانند
    IntelliSense/Autocomplete را پشتیبانی کنند.
    
    استفاده:
        >>> from ollama_models_static import OllamaModels
        >>> model = OllamaModels.GEMMA3_12B
        >>> print(model.value)
        'gemma3:12b'
    
    توجه:
        - نام‌های Enum: فرمت UPPERCASE با _
        - مقادیر: نام اصلی مدل در Ollama
    """
'''
    
    # تولید خطوط Enum
    enum_lines: list[str] = []
    for model in sorted(models):  # مرتب‌سازی برای خوانایی بهتر
        enum_name = sanitize_enum_name(model)
        # اضافه کردن دو فاصله قبل از = برای زیبایی
        enum_lines.append(f'    {enum_name} = "{model}"')
    
    # ترکیب کل کد
    code: str = header + "\n".join(enum_lines) + "\n"
    
    return code


def write_static_enum_file(output_path: Path, code: str) -> None:
    """
    نوشتن کد تولید شده در فایل
    
    Args:
        output_path: مسیر فایل خروجی
        code: کد Python برای نوشتن
    """
    output_path.write_text(code, encoding="utf-8")
    print(f"✅ فایل با موفقیت ساخته شد: {output_path}")


def main() -> None:
    """تابع اصلی برای اجرای اسکریپت"""
    try:
        print("🔍 در حال دریافت لیست مدل‌ها از Ollama...")
        
        # دریافت لیست مدل‌ها
        models: tuple[str, ...] = fetch_ollama_models()
        
        if not models:
            print("⚠️  هیچ مدلی یافت نشد! مطمئن شوید که Ollama در حال اجرا است.")
            return
        
        print(f"✓ {len(models)} مدل یافت شد")
        
        # تولید کد
        print("\n📝 در حال تولید کد Python...")
        code: str = generate_enum_code(models)
        
        # تعیین مسیر خروجی (همان مسیر این اسکریپت)
        output_path: Path = Path(__file__).parent / "ollama_models_static.py"
        
        # نوشتن فایل
        print(f"\n💾 در حال نوشتن فایل: {output_path.name}")
        write_static_enum_file(output_path, code)
        
        # نمایش لیست مدل‌ها
        print("\n📋 مدل‌های اضافه شده:")
        print("─" * 60)
        for i, model in enumerate(sorted(models), 1):
            enum_name = sanitize_enum_name(model)
            print(f"{i:2d}. {enum_name:35} → {model}")
        
        print("\n" + "=" * 60)
        print(f"✨ تمام! حالا می‌توانید از OllamaModels با IntelliSense استفاده کنید!")
        print("\n💡 نکته: بعد از نصب مدل جدید، این اسکریپت را دوباره اجرا کنید:")
        print("   python generate_static_enum.py")
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        raise


if __name__ == "__main__":
    main()
