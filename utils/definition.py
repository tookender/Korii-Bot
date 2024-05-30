from bs4 import BeautifulSoup, Tag

from bot import Korii


async def get_word_details(bot: Korii, word):
    url = f"https://www.thefreedictionary.com/{word}"
    request = await bot.session.get(url)
    content = await request.text()

    soup = BeautifulSoup(content, "html.parser")

    syllable = "Unknown"
    pronunciation = "Unknown"
    word_type = "Unknown"
    etymology = ""
    definitions = []
    definition_section = soup.find("div", {"id": "Definition"})

    if definition_section and isinstance(definition_section, Tag):
        for item in definition_section.find_all("section"):
            if item["data-src"] and item["data-src"] == "hm":
                for h2 in item.find_all("h2"):
                    syllable = h2.text.strip()

                for span in item.find_all("span", class_="pron"):
                    pronunciation = span.text.strip()

                for pseg in item.find_all("div", class_="pseg"):
                    word_type = pseg.find("i").text.strip()
                    for div2 in pseg.find_all("div", class_="ds-list"):
                        definitions.append(div2.text.strip())

                for etyseg in item.find_all("div", class_="etyseg"):
                    etymology = etyseg.text.strip()

    return {
        "syllable": syllable,
        "pronunciation": pronunciation,
        "word_type": word_type,
        "definitions": definitions,
        "etymology": etymology,
    }
