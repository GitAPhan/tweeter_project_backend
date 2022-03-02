# # format user request output
# def format_user_output(users, is_token_present):
#     ### VERSION 1 ### #
#     if is_token_present:
#         return {
#             "userId": users[0],
#             "email": users[1],
#             "username": users[2],
#             "bio": users[3],
#             "birthdate": users[4],
#             "imageUrl": users[5],
#             "bannerUrl": users[6],
#             "loginToken": users[7],
#         }
#     else:
#         return {
#             "userId": users[0],
#             "email": users[1],
#             "username": users[2],
#             "bio": users[3],
#             "birthdate": users[4],
#             "imageUrl": users[5],
#             "bannerUrl": users[6],
#         }
def format_user_output(user):
    # VERSION 2 
    key_name = {
        0: "userId",
        1: "email",
        2: "username",
        3: "bio",
        4: "birthdate",
        5: "imageUrl",
        6: "bannerUrl",
        7: "loginToken"
    }

    return_payload = {}
    i = 0
    for col in user:        
        return_payload[key_name[i]] = col
        i += 1

    return return_payload

def format_tweet_output(tweet):
    key_name = {
        0: "tweetId",
        1: "userId",
        2: "username",
        3: "content",
        4: "createdAt",
        5: "userImageUrl",
        6: "tweetImageUrl"
    }

    return_payload = {}
    i = 0
    increase = 1
    if len(tweet) == 2:
        increase = 3
    for col in tweet:
        return_payload[key_name[i]] = col
        i += increase
    
    return return_payload

