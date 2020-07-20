import jieba
from wordcloud import ImageColorGenerator, WordCloud
from matplotlib import pyplot as plt
import numpy as np
import PIL

with open('data/评论.txt','r',encoding='utf-8') as f:
    text=f.read()
cutted_text=jieba.cut(text,cut_all=False)
word=' '.join(cutted_text)


#生成词云
wordcloud=WordCloud(
    scale=4,
    background_color='white',
    max_words=200, #最大显示的词数
    font_path="simkai.ttf",
    width=1200,height=1200,
    min_font_size=20,
).generate(word)


plt.imshow(wordcloud)
plt.axis('off')
plt.savefig("data/clound.png",dpi=300)
plt.show()