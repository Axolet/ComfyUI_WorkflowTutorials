import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
import re

# Read the comments from the Excel file
comments_df = pd.read_excel('reddit_data.xlsx')

# Concatenate all the comments into a single string
text = ' '.join(comments_df['Content'].astype(str))
# Remove stopwords from the text
text = ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])
# Convert to lowercase and remove punctuation
text = re.sub(r'[^\w\s]', '', text.lower())

# Create a word cloud
wordcloud = WordCloud(width=800, height=400,
                      background_color='white',
                      colormap='viridis',
                      max_words=50,
                      min_font_size=10,
                      max_font_size=200).generate(text)

# Display the word cloud
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

# Save the word cloud to a file
wordcloud.to_file("reddit_data_wordcloud.png")