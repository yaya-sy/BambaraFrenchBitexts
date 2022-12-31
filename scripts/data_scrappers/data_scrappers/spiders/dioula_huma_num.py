import scrapy

class QuotesSpider(scrapy.Spider):
    name = "dioula_huma_num"
    start_urls = [
            "http://ellaf.huma-num.fr/f%ce%adn-min-kos%c9%94n-sa-b%e1%bd%b2-jie-ra-pourquoi-le-serpent-vit-dans-leau-de-nos-jours/",
            "http://ellaf.huma-num.fr/toriri-b%c9%9bmari-saraga-sogo-b%c9%94-surugu-ninden-fila-kuman-to-yi-la-ceremonie-de-sacrifice-des-grenouilles-et-le-double-langa/",
            "http://ellaf.huma-num.fr/ole-koson-m%c9%94g%c9%94-ye-e-t%c9%94g%c9%94-nyan-pourquoi-il-faut-faire-attention-a-sa-reputation/",
            "http://ellaf.huma-num.fr/fin-mi-kos%e2%86%84n-ba-ye-buwo-k%ce%ad-wasawasa-pourquoi-les-crottes-de-chevre-sont-rondes/",
            "http://ellaf.huma-num.fr/fin-mi-kos%c9%94n-surugu-ye-siran-kanganan-ny%ce%adn-pourquoi-lhyene-a-t-elle-peur-du-varan-deau/",
            "http://ellaf.huma-num.fr/surugu-bannan-saraga-b%c9%94-man-a-ka-a-k%c9%94-ye-un-marabout-predit-a-hyene-que-sil-ne-faisait-pas-de-sacrifice-il-subirait-une/",
            "http://ellaf.huma-num.fr/ole-koson-ni-e-ka-se-mg-ra-ye-tm-fan-biy-ra-ka-ko-k-a-ra-voi/",
        ]

    def parse(self, response):
        title_dioula, title_french = response.css("h1.entry-title::text").get().split("/")
        title_dioula, title_french = title_dioula.strip(), title_french.strip()
        with open(f"../../data/ellaf.huma-num.fr/dioula.txt", "a+") as dioula_file:
            with open(f"../../data/ellaf.huma-num.fr/french.txt", "a+") as french_file:
                french_file.write(f"{title_french}\n")
                dioula_file.write(f"{title_dioula}\n")
                for aligned_text in response.css('div.entry-content table'):
                    for utterance_pair in aligned_text.css("tbody tr"):
                        paired_utterance = utterance_pair.css("td")
                        dioula_utterance = paired_utterance[0].css("p *::text").get()
                        french_utterance = paired_utterance[1].css("p *::text").get()
                        if french_utterance is None:
                            french_utterance = paired_utterance[1].css("td::text").get()
                        if dioula_utterance is None:
                            dioula_utterance = paired_utterance[0].css("td::text").get()
                        if not any([french_utterance, dioula_utterance]):
                            continue
                        dioula_file.write(f"{dioula_utterance}\n")
                        french_file.write(f"{french_utterance}\n")