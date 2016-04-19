import wordcloud
import numpy as np
from os import path
from PIL import Image
from wordcloud import ImageColorGenerator
from wordcloud import WordCloud as wc

d = path.dirname("__file__")

def make_wc(dict, maskpath="", colours=False):


	if (maskpath):
		word_mask = np.array(Image.open(path.join(d, maskpath)))
		wordcloud = wc(background_color="white", mask=word_mask)

		wordcloud.generate_from_frequencies(dict)

		if (colours):
			image_colours = ImageColorGenerator(word_mask)
			wordcloud.recolor(color_func=image_colours)
	else:
		wordcloud = wc(width=1200, height=800).generate_from_frequencies(dict)
	


	return wordcloud


