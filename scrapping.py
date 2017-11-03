import json
import urllib2
import time




# 1183362 users in full dataset - need ur help!
# 295840 * 4 = 1183360
# 0: 0
# 2: 295840
# 3: 591680
# 4: 887520
# change this as well as lines 15-16 (where to store, where to load..) 
user_skip = 0




user_count = user_skip
with open("../data/profile_pics.txt", "a") as prof_pics:
  with open("../data/dataset/user.json", "r") as users:

    # skip first users
    for i in range(user_skip): users.readline()

    # all other users
    for l in users:
      time.sleep(2)

      # download page
      user = json.loads(l)
      uid = user["user_id"]
      url = "https://www.yelp.com/user_details?userid=" + uid
      response = urllib2.urlopen(url)
      html = response.read()

      # find photos
      photo_section = html.find(
          "<div class=\"photo-slideshow photo-slideshow--full-width " +
          "photo-slideshow--rounded js-photo-slideshow-user-details\">")
      if photo_section > 0:
        prof_pics.write(uid + " ")
        count = 0

        # get url of each photos
        img_index = photo_section
        while img_index > 0:
          img_index = html.find("<img ", img_index)
          img_end = html.find(">", img_index)
          img_data = html[img_index:img_end]

          # break if no alt tag: users with no pictures have no 'alt'
          alt_index = img_data.find("alt=\"") + 5
          if alt_index == -1: break

          # break if we reached a photo with a alt tag that's not a profile pic
          # Find first word of the pseudo of the user (we only have the first
          # word in our dataset)
          alt_end = min(img_data.find(" ", alt_index),
                        img_data.find("\"", alt_index))
          pseudo = img_data[alt_index:alt_end]
          if pseudo != user["name"]: break

          # src, has the url to download
          src_index = img_data.find("src=\"") + 5
          src_end = img_data.find("\"", src_index)
          photo_url = img_data[src_index:src_end]

          # write url in file
          prof_pics.write(photo_url + " ")
          count += 1

          # skip this pictures
          img_index = img_end + 1

        # write newline for next user
        prof_pics.write("\n")
        user_count += 1
        print("%s %i photo%s (user count: %i)"
              % (user["name"], count, "s" if count > 1 else "", user_count))



