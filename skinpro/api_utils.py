import time
import requests
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

API_SKINCARE_URL = (
    "https://api-inference.huggingface.co/models/varun1505/face-characteristics"
)
API_GENDER_URL = "https://api-inference.huggingface.co/models/Leilab/gender_class"
headers = {"Authorization": "Bearer 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"}


def query(file):
    with open(file, "rb") as f:
        data = f.read()
    skinres = requests.post(API_SKINCARE_URL, headers=headers, data=data)
    genres = requests.post(API_GENDER_URL, headers=headers, data=data)
    
    time.sleep(7)
    # preprosessing data
    gen_res_data = genres.json()

    skin_res_data = [
        {
            k: v * 10 if isinstance(v, (int, float)) else v
            for k, v in reversed(item.items())
        }
        for item in skinres.json()
    ]

    if gen_res_data[0]["label"] == "men":
        gen_res = "man"
    else:
        gen_res = "woman"

    # time.sleep(7)
    return {"skinres": skin_res_data, "genres": gen_res}

def generate_summary(results):
    # Use OpenAI GPT-3 to generate a summary
    # Replace the prompt and adjust parameters based on your needs
    prompt = "Generate a comprehensive and personalized skin prescription about me based on the following skin analysis results: [Include relevant details about the analysis, such as skin type, specific concerns, and any identified characteristics]. Provide recommendations for skincare products, routines, and lifestyle adjustments to improve overall skin health. Consider factors like hydration, exfoliation, sun protection, and specific treatments for targeted concerns. Be detailed and tailored to the individual's unique skin needs." + "comprehensive analysis of the individual's skin type and concerns. Consider addressing specific issues such as hydration levels, inflammation, acne, fine lines, uneven skin tone, or other identified characteristics. Provide tailored recommendations for morning and evening skincare routines, including cleansers, moisturizers, serums, and targeted treatments. Emphasize factors like sun protection, lifestyle adjustments, and potential irritants to avoid. Aim for a holistic approach, taking into account the unique needs of the individual for improved overall skin health."+ "try to make the summary big"+ str(results)
    response  = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": prompt}],
        max_tokens=100,  # Adjust as needed
        n=1,
        temperature = 0.5,
    )
    return response.choices[0].message.content