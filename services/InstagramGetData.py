


def getApiData(jsondata):

    import json
    
    bytes_data = jsondata.getvalue()

    data = json.loads(bytes_data)
    
    posts = data['graphql']['user']['edge_owner_to_timeline_media']['count']

    followers = data['graphql']['user']['edge_followed_by']['count']

    following = data['graphql']['user']['edge_follow']['count']

    bio_length = len(data['graphql']['user']['biography'])
    
    has_pic = True if data['graphql']['user']['profile_pic_url_hd'] != None else False

    has_link = True if data['graphql']['user']['external_url'] != None else False

    post_caption_counter = 0
    post_counter = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        if len(edges['node']['edge_media_to_caption']['edges']) > 0:
            post_caption_counter += len(edges['node']['edge_media_to_caption']['edges'][0]['node']['text'])
        post_counter += 1
    
    post_caption_average = round(post_caption_counter / post_counter) if post_counter > 0 else 0

    post_caption_counter_less_equal_3 = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        if len(edges['node']['edge_media_to_caption']['edges']) > 0:

            if len(edges['node']['edge_media_to_caption']['edges'][0]['node']['text']) <= 3:
                post_caption_counter_less_equal_3 += 1

    # Percentage of posts that are not an image
    posts_not_image = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        if edges['node']['__typename'] != 'GraphImage':
            posts_not_image += 1

    percentage_posts_not_image = posts_not_image / (posts * 100) if post_counter > 0 else 0

    # Taxa de engajamento
    total_likes = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        total_likes += edges['node']['edge_liked_by']['count']

    like_engagement_rate = total_likes / followers

    # Taxa de engajamento comentários
    total_comments = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        total_comments += edges['node']['edge_media_to_comment']['count']

    comment_engagement_rate = total_comments / followers

    # Porcentagem de posts com tag de localização
    posts_with_location = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        if edges['node']['location'] != None:
            posts_with_location += 1

    percentage_posts_with_location = posts_with_location / (posts * 100) if post_counter > 0 else 0

    # Hashtag use rate
    total_hashtags = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        if len(edges['node']['edge_media_to_caption']['edges']) > 0:
            total_hashtags += edges['node']['edge_media_to_caption']['edges'][0]['node']['text'].count('#')

    hashtag_use_rate = total_hashtags / posts if post_counter > 0 else 0


    # Palavras comerciais
    comercial_words_list = ["regrann", "contest", "repost", "giveaway", "mention", "share", "give away", "quiz", ]
    comercial_words_counter = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        for word in comercial_words_list:
            if len(edges['node']['edge_media_to_caption']['edges']) > 0:
                if word in edges['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                    comercial_words_counter += 1
    
    comercial_words_rate = comercial_words_counter / posts if post_counter > 0 else 0

    # palavras chaves seguidores
    followers_words_list = ["follow", "like", "folback", "follback", "f4f"]
    followers_words_counter = 0
    for edges in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        for word in followers_words_list:
            if len(edges['node']['edge_media_to_caption']['edges']) > 0:
                if word in edges['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                    followers_words_counter += 1

    followers_words_rate = followers_words_counter / posts if post_counter > 0 else 0

    return (posts, followers, following, bio_length, int(has_pic), int(has_link), post_caption_average, post_caption_counter_less_equal_3, percentage_posts_not_image, like_engagement_rate, comment_engagement_rate, percentage_posts_with_location, hashtag_use_rate, comercial_words_rate, followers_words_rate)


def getUsername(jsondata):
    import json
    
    bytes_data = jsondata.getvalue()

    data = json.loads(bytes_data)

    return data['graphql']['user']['username']