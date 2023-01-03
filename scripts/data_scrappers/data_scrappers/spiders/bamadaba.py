import re
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "bamadaba"
    alphabet = ["a", "b", "c", "d", "e", "ɛ", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "ɲ", "ŋ", "o",
                "ɔ", "p", "r", "s","t", "u", "w", "x", "y", "z"]
    start_urls = [f"http://cormand.huma-num.fr/Bamadaba/lexicon/{letter}.htm" for letter in alphabet]

    def get_translation_definitions(self, response, bambara_file, french_file):
        """
        Iterates over the word entries of the dictionnary
        and retrieves the examples of bambara sentences
        using these words and the french translations of these sentences.
        """
        files = {"bambara": bambara_file, "french": french_file}
        languages = {"Exe" : "bambara", "GlFr" : "french"}
        grammar_pattern = r"voyelles|voyelle|Verbes|personnels|Mots|infinitif|subjonctif|Construction"
        # p.lxP2 is for the word entry in the dictionnary
        for entry in response.css("p.lxP2,p.lxP"):
            last_tag = None
            sentences = {"bambara": [], "french": []}
            for span in entry.css("span"):
                # we are only interested by the french and bambara sentences.
                if "id" in span.attrib:
                    word = span.css("*::text").get()
                    id = span.attrib["id"]
                if span.attrib["class"] not in ["Exe", "GlFr"]:
                    continue
                # if the first example is french, it's probably just the translation
                # of the bambara word rather than a translation of a bambara sentence example.
                if last_tag == None and span.attrib["class"] == "GlFr":
                    continue
                last_tag = span.attrib["class"]
                for sentence in span.css(f"span.{last_tag} *::text").getall():
                    if re.findall(grammar_pattern, sentence):
                        continue
                    sentences[languages[last_tag]].append(sentence)
            # if we have don't have any examples
            if not sentences["bambara"] or not sentences["french"]:
                continue
            # sometimes the examples retrived are not aligned... we have to solve this problem.
            if len(sentences["bambara"]) != len(sentences["french"]):
                continue
            bambara_sentences = "\n".join(sentences["bambara"])
            french_sentences = "\n".join(sentences["french"])
            files["bambara"].write(bambara_sentences + "\n")
            files["french"].write(french_sentences + "\n")

    def get_translation_audios(self, response, bambara_file, french_file):
        """Get the translations in the audio examples."""
        sentences = {"bambara" : [], "french" : []}
        french_bambara_separator = r"\- \'|\- \‘|\- \«| ‘| \'| «"
        grammar_pattern = r"voyelles|voyelle|Verbes|personnels|Mots|infinitif|subjonctif|Construction"
        for audio_example in response.css("div.maud small"):
            audio_capture = audio_example.css("*::text").getall()
            if not audio_capture:
                continue
            # a remove the note
            if "ↈ" in audio_capture:
                audio_capture.remove("ↈ")
            if not audio_capture:
                continue
            # if the bambara sentence and its thranslation are in the same string
            if len(audio_capture) == 1:
                example = audio_capture[0]
                separated = re.split(french_bambara_separator, example)
                if len(separated) != 2:
                    continue
                bambara, french = separated[0].strip(), separated[1].strip()
                if re.search(grammar_pattern, french) or re.search(grammar_pattern, bambara):
                    continue
                sentences["bambara"].append(bambara)
                sentences["french"].append(french)

            elif len(audio_capture) == 2:
                bambara, french = audio_capture
                if re.search(french_bambara_separator, bambara):
                    separated = re.split(french_bambara_separator, bambara)
                    if len(separated) != 2:
                        continue
                    bambara, french = separated
                if re.search(grammar_pattern, french) or re.search(grammar_pattern, bambara):
                    continue
                sentences["bambara"].append(bambara.strip())
                sentences["french"].append(french.strip())
            
            # the last element is just a grammatical description
            elif len(audio_capture) == 3:
                bambara, french, _ = audio_capture
                if re.findall(grammar_pattern, french) or re.findall(grammar_pattern, bambara):
                    continue
                sentences["bambara"].append(bambara.strip())
                sentences["french"].append(french.strip())
            else:
                # maybe we can try to retrieve some examples here...
                continue
        french_file.write("\n".join(sentences["french"]))
        bambara_file.write("\n".join(sentences["bambara"]))

    def parse(self, response):
        with open("../../data/bamadaba/french.txt", "a+") as french_file :
            with open("../../data/bamadaba/bambara.txt", "a+") as bambara_file :
                self.get_translation_definitions(response, bambara_file, french_file)
                self.get_translation_audios(response, bambara_file, french_file)
