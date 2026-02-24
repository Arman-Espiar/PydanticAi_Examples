"""
Enum استاتیک مدل‌های Ollama

**هشدار:** این فایل به صورت خودکار توسط اسکریپت generate_static_enum.py تولید شده است.
این فایل را به صورت دستی ویرایش نکنید!

برای به‌روزرسانی بعد از نصب مدل جدید:
    python generate_static_enum.py

تاریخ تولید: 2026-02-06 14:05:17
تعداد مدل‌ها: 8
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
    FUNCTIONGEMMA_LATEST = "functiongemma:latest"
    GEMMA3_12B = "gemma3:12b"
    GEMMA3PERSIAN_OPTIMIZED_LATEST = "gemma3persian-optimized:latest"
    HF_CO_TENCENT_HY_MT1_5_1_8B_GGUF_Q8_0 = "hf.co/tencent/HY-MT1.5-1.8B-GGUF:Q8_0"
    MSHOJAEI77_GEMMA3PERSIAN_TOOLS_LATEST = "mshojaei77/gemma3persian-tools:latest"
    MSHOJAEI77_GEMMA3PERSIAN_LATEST = "mshojaei77/gemma3persian:latest"
    TRANSLATEGEMMA_FAIR_LATEST = "translategemma-fair:latest"
    TRANSLATEGEMMA_LATEST = "translategemma:latest"
