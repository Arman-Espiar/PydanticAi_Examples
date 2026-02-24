from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent

# استفاده از Enum استاتیک (تولید شده توسط generate_static_enum.py)
# این روش به IDE اجازه می‌دهد تا IntelliSense/Autocomplete را پشتیبانی کند
from ollama_models_static import OllamaModels

class AgentCreator:
    """
    کلاس سازنده ایجنت‌های PydanticAI با استفاده از مدل‌های Ollama
    
    ویژگی‌ها:
    ۱. دریافت لیست مدل‌ها به صورت Enum برای جلوگیری از خطای تایپی
    ۲. مقداردهی اولیه مدل با استفاده از OpenAIChatModel و تنظیم پرووایدر Ollama
    ۳. ارائه متدی برای ساخت نمونه‌های مختلف Agent با system_prompt‌های متفاوت
    ۴. امکان استفاده از سرور Ollama سفارشی با تنظیم base_url
    
    مزایای استفاده از کلاس:
    - مدل فقط یک بار ساخته می‌شود و برای چندین ایجنت استفاده می‌شود (کارایی بهتر)
    - قابلیت گسترش و افزودن متدهای جدید در آینده
    - تست‌پذیری بالا و امکان mock کردن dependencies
    """
    def __init__(
        self, 
        model_choice: OllamaModels,
        base_url: str = 'http://localhost:11434/v1'
    ) -> None:
        """
        مقداردهی اولیه سازنده ایجنت
        
        Args:
            model_choice: مدل Ollama انتخابی از Enum مدل‌های موجود
            base_url: آدرس پایه سرور Ollama (پیش‌فرض: localhost روی پورت ۱۱۴۳۴)
        """
        # ساخت مدل با استفاده از پرووایدر Ollama
        self.model: OpenAIChatModel = OpenAIChatModel(
            model_name=model_choice.value,
            provider=OllamaProvider(base_url=base_url),
        )

    def build_agent(self, system_prompt: str | None = None) -> Agent:
        """
        ساخت و بازگرداندن یک نمونه جدید از Agent
        
        این متد از مدل مشترک ذخیره شده در کلاس استفاده می‌کند،
        بنابراین می‌توانید چندین ایجنت با system_prompt‌های متفاوت
        و بدون ساخت مجدد مدل بسازید.
        
        Args:
            system_prompt: دستورالعمل سیستمی برای ایجنت (اختیاری)
                          این پرامپت رفتار و نقش ایجنت را مشخص می‌کند
        
        Returns:
            Agent: نمونه جدید از ایجنت PydanticAI با مدل و پرامپت تنظیم شده
        
        Example:
            >>> creator = AgentCreator(OllamaModels.LLAMA2)
            >>> translator = creator.build_agent("شما یک مترجم حرفه‌ای هستید")
            >>> summarizer = creator.build_agent("شما یک خلاصه‌نویس هستید")
        """
        return Agent(model=self.model, system_prompt=system_prompt)


if __name__ == "__main__":
    print("Cannot use directly, use the example_ollama.py file")
    
