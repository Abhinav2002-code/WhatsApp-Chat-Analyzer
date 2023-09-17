from collections import Counter

import pandas as pd
import advertools as adv
from urlextract import URLExtract
from wordcloud import WordCloud



def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    num_msg = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())
    num_words = len(words)

    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))
    nums_links = len(links)

    return num_msg, num_words, num_media, nums_links


def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={
            'index': 'percent',
            'users': 'Name',
            'count': 'Percent(%)'
        }
    )
    return x, df


def create_word_cloud(selected_user, df):
    # df = df[df['messages'] != '<Media omitted>']

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'You deleted this message\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']
    # temp = temp[temp['messages'] != selected_user + ' deleted this message']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('english_stop.txt', 'r', encoding='utf-8')
    stopWords = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'You deleted this message\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']
    # temp = temp[temp['messages'] != selected_user + ' deleted this message']

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    emoji_summary = adv.extract_emoji(df['messages'])
    emoji_df = pd.DataFrame(emoji_summary['top_emoji'])[0:10]

    return emoji_df


def monthly_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    daily = df.groupby('only_date').count()['messages'].reset_index()
    return daily
