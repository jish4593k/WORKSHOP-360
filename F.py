import scrapy
import torch
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from tkinter import Tk, Label, PhotoImage

class BricksetItem(scrapy.Item):
    name = scrapy.Field()
    pieces = scrapy.Field()
    minifigs = scrapy.Field()
    image = scrapy.Field()

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'

            item = BricksetItem()
            item['name'] = brickset.css(NAME_SELECTOR).extract_first()
            item['pieces'] = brickset.xpath(PIECES_SELECTOR).extract_first()
            item['minifigs'] = brickset.xpath(MINIFIGS_SELECTOR).extract_first()
            item['image'] = brickset.css(IMAGE_SELECTOR).extract_first()

            # PyTorch Tensor Operations (Dummy Example)
            tensor_result = torch.tensor([1, 2, 3]) * 2
            item['tensor_result'] = tensor_result.tolist()

            # Seaborn Plot (Dummy Example)
            self.create_seaborn_plot()

            yield item

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def create_seaborn_plot(self):
        data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        sns.histplot(data, bins=5, kde=False)
        plt.title('Seaborn Histogram Example')
        plt.xlabel('Value')
        plt.ylabel('Frequency')

        # Save the Seaborn plot as an image
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Convert the image to base64 for embedding in HTML
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        # Display the Seaborn plot using Tkinter
        self.display_seaborn_plot(img_base64)

    def display_seaborn_plot(self, img_base64):
        root = Tk()
        root.title("Seaborn Plot Display")

        # Convert base64 to PhotoImage
        img_data = base64.b64decode(img_base64)
        img = PhotoImage(data=img_data)

        # Display the image in a Label
        label = Label(root, image=img)
        label.image = img
        label.pack()

        root.mainloop()
