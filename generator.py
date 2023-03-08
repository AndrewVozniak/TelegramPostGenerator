import openai
import telebot
import urllib
import os

openai.api_key = "key"
bot = telebot.TeleBot('token')


def generate(topic):
    try:
        text = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate text about {topic} around 1000 symbols on Russian language and add logic end",
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        text = text.choices[0].text.strip()

        image = openai.Image.create(
            model="image-alpha-001",
            prompt=topic,
            n=1,
            size="1024x1024"
        )

        image_url = image['data'][0]['url']

        print(text)
        print(f"""
        -----------------
        IMG: {image_url}
        """)

        return text, image_url
    except:
        generate(topic)


@bot.message_handler(content_types=["text"])
def startMSG(message):
    bot.send_message(message.chat.id, "Введи тему поста:")
    bot.register_next_step_handler(message, generateStep)

def generateStep(message):
    text, image_url = generate(message.text)

    urllib.request.urlretrieve(image_url, "image.jpg")
    
    bot.send_photo(message.chat.id, open("image.jpg", "rb"))
    bot.send_message(message.chat.id, text)

    os.remove("image.jpg")

    startMSG(message)

if __name__ == '__main__':
    bot.infinity_polling()