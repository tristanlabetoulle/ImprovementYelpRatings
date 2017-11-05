import json

# Store business ids in toronto
business_ids = set()

# Business
print("Business...")
with open("../data/filtered/business.json", "w") as filtered_business_file:
  for l in open("../data/dataset/business.json", "r"):    
    business = json.loads(l)
    if business["city"] == "Toronto":
      json.dump(business, filtered_business_file)
      filtered_business_file.write("\n")
      business_ids.add(business["business_id"])

# Store users who either commented or gave a tip on a business
user_ids = set()

# Review
print("Review...")
with open("../data/filtered/review.json", "w") as filtered_review_file:
  for l in open("../data/dataset/review.json", "r"):    
    review = json.loads(l)
    if review["business_id"] in business_ids:
      json.dump(review, filtered_review_file)
      filtered_review_file.write("\n")
      user_ids.add(review["business_id"])

# Tip
print("Tip...")
with open("../data/filtered/tip.json", "w") as filtered_tip_file:
  for l in open("../data/dataset/tip.json", "r"):    
    tip = json.loads(l)
    if tip["business_id"] in business_ids:
      json.dump(tip, filtered_tip_file)
      filtered_tip_file.write("\n")
      user_ids.add(tip["user_id"])

# User
print("User...")
with open("../data/filtered/user.json", "w") as filtered_user_file:
  for l in open("../data/dataset/user.json", "r"):    
    user = json.loads(l)
    if user["user_id"] in user_ids:
      json.dump(user, filtered_user_file)
      filtered_user_file.write("\n")

# Ignore photos and check-in


