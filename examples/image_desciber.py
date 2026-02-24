import asyncio

from pydantic_ai import Agent, BinaryContent
from agent_creator_ollama import AgentCreator, OllamaModels


# ۱- ساخت Agent با استفاده از مدل GEMMA3_12B
# توجه: نام‌های enum به صورت UPPERCASE و با _ به جای - و : هستند
agent_creator = AgentCreator(model_choice=OllamaModels.GEMMA3_12B)

# ۲- ساخت Agent با system_prompt برای توصیف تصاویر
image_describer_agent: Agent = agent_creator.build_agent(
    system_prompt="شما یک توصیف‌کننده حرفه‌ای تصاویر هستید. تصاویر را با جزئیات کامل و دقیق توصیف کنید."
)

# ۳- مثال استفاده (می‌توانید این قسمت را uncomment کنید)
async def main():
    # مسیر تصویر مورد نظر (نسبت به فایل فعلی)
    image_path: str = r".\assets\n1.jpg"
    
    # تبدیل تصویر به باینری
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # اجرای agent برای توصیف تصویر
    result = await image_describer_agent.run(
        [
            "این تصویر را توصیف کن",
            BinaryContent(data=image_bytes,media_type="image/jpeg"),
        ]
    )

    print("\n=== توصیف تصویر ===")
    print(result.output)

    #write to text file
    with open("examples/image_desciber.md", "w", encoding="utf-8") as f:
        f.write(result.output)  


if __name__ == "__main__":
    asyncio.run(main())