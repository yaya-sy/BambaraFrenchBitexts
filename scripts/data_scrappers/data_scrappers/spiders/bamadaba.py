import re
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "bamadaba"
    alphabet = ["a", "b", "c", "d", "e", "ɛ", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "ɲ", "ŋ", "o",
                "ɔ", "p", "r", "s","t", "u", "w", "x", "y", "z"]
    start_urls = [f"http://cormand.huma-num.fr/Bamadaba/lexicon/{letter}.htm" for letter in alphabet]

    def get_translation_definitions(self, response):
        """
        Iterates over the word entries of the dictionnary
        and retrieves the examples of bambara sentences
        using these words and the french translations of these sentences.
        """
        languages = {"Exe": "bambara", "GlFr": "french"}
        # p.lxP2 is for the word entry in the dictionnary
        for entry in response.css("p.lxP2"):
            last_tag = None
            sentences = {"bambara": [], "french": []}
            for span in entry.css("span"):
                # we are only interested by the french and bambara sentences.
                if span.attrib["class"] not in ["Exe", "GlFr"]:
                    continue
                # if the first example is french, it's probably just the translation
                # of the bambara word rather than a translation of a bambara sentence example.
                if last_tag == None and span.attrib["class"] == "GlFr":
                    continue
                last_tag = span.attrib["class"]
                sentences[languages[last_tag]].append(span.css(f"span.{last_tag}::text").get().strip())
            # if we have don't have any examples
            if not sentences["bambara"] or not sentences["french"]:
                continue
            # sometimes the examples retrived are not aligned... we have to solve this problem.
            if len(sentences["bambara"]) != len(sentences["french"]):
                continue
            yield sentences
    
    def get_translation_audios(self, response):
        """Get the translations in the audio examples"""
        sentences = {"bambara" : [], "french" : []}
        for audio_example in response.css("div.maud small"):
            audio_capture = audio_example.css("text").getall()
            if not audio_capture:
                continue
            # a remove the note
            if "ↈ" in audio_capture:
                audio_capture.remove("ↈ")
            # TODO: remove the grammatical description of the example
            # we have to check by and to remove all the grammatical description...
            # just removing the last element is not suffiscient
            poped = audio_capture.pop(-1)
            if not audio_capture:
                continue
            # TODO: sometimes we have more than one example, or different 
            # formulations of bambara sentence translated once into french, vice-vers.
            # We have to solve this.

            # TODO: if we only have one element, the bambara sentence in the french\
            # sentence are separated by a "-", "-/-" or just a space with citation marks ("‘", "«")
            # we
            if len(audio_capture) == 1:
                continue
            if len(audio_capture) == 2:
                bambara, french = audio_capture
                sentences["bambara"].append(bambara)
                sentences["french"].append(french)
            
            if len(audio_capture) == 3:
                # TODO: Here we have to check many things and to solve them
                continue
        return sentences

    def parse(self, response):
        with open("../../data/bamadaba/french.txt", "a+") as french_file :
            with open("../../data/bamadaba/bambara.txt", "a+") as bambara_file :
                for sentences in self.get_translation_definitions(response):
                    french_file.write("\n".join(sentences["french"]))
                    bambara_file.write("\n".join(sentences["bambara"]))
                audio_bambara_sentences, audio_bambara_sentences = self.get_translation_audios(response)
                bambara_file.write("\n".join(audio_bambara_sentences))
                french_file.write("\n".join(audio_bambara_sentences))
