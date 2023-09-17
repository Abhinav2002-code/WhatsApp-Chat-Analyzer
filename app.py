import matplotlib.pyplot as plt
import streamlit as st

import helper
import preprocessor

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)

    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Individual Users", user_list)

    if st.sidebar.button("Analyze"):

        st.title("TOP STATISTICS")

        num_msg, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(num_links)

        st.title("Monthly Stats")
        monthly_stats = helper.monthly_stats(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_stats['time'], monthly_stats['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Stats")
        daily_stats = helper.daily_stats(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_stats['only_date'], daily_stats['messages'], color= 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        if selected_user == "Overall":
            st.title('Most Busy USERS')

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("Word Cloud")
        im = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(im)
        st.pyplot(fig)

        st.title("Most 20 Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emojis_used = helper.emoji_helper(selected_user, df)

        with col1:
            st.dataframe(emojis_used)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emojis_used[1], labels=emojis_used[0])
            st.pyplot(fig)
