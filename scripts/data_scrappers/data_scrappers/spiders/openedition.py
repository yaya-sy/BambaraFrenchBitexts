import re
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "openedition"

    def start_requests(self):
        urls = {
            "bambara": [f"https://books.openedition.org/demopolis/54{i}" for i in range(1, 7)],
            "french": [f"https://books.openedition.org/demopolis/{i}" for i in range(526, 532)]
            }

        for language in urls:
            for url in urls[language]:
                yield scrapy.Request(url, meta={'language': language})
    
    def remove_successive_spaces(self, text):
        return re.sub(" +", " ", text)

    def parse(self, response):
        language = response.meta.get('language')
        title = response.css('h1.title ::text').get()
        to_exclude = {"legendeillustration", "legendeillustration", "paragraphesansretrait", "separateur"}

        with open(f"../../data/openedition/{language}.txt", "a+") as output_file:
            for text in response.css("div.text.wResizable.medium p, div.text.wResizable.medium h2"):
                if text.attrib["class"] in to_exclude:
                    continue
                text_contents = text.css("*::text").getall()
                paragraph = " ".join(text_contents)
                paragraph = self.remove_successive_spaces(paragraph)
                output_file.write("\n".join([title, paragraph]))

