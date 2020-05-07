#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, json, gzip, csv
import pandas as pd
import pprint

# Amazon Dataset
datasets = [
    "All_Beauty_5.json.gz",
    "AMAZON_FASHION_5.json.gz",
    "Appliances_5.json.gz",
    "Arts_Crafts_and_Sewing_5.json.gz",
    "Automotive_5.json.gz",
    "Books_5.json.gz",
    "CDs_and_Vinyl_5.json.gz",
    "Cell_Phones_and_Accessories_5.json.gz",
    "Clothing_Shoes_and_Jewelry_5.json.gz",
    "Digital_Music_5.json.gz",
    "Electronics_5.json.gz",
    "Gift_Cards_5.json.gz",
    "Grocery_and_Gourmet_Food_5.json.gz",
    "Home_and_Kitchen_5.json.gz",
    "Industrial_and_Scientific_5.json.gz",
    "Kindle_Store_5.json.gz",
    "Luxury_Beauty_5.json.gz",
    "Magazine_Subscriptions_5.json.gz",
    "Movies_and_TV_5.json.gz",
    "Musical_Instruments_5.json.gz",
    "Office_Products_5.json.gz",
    "Patio_Lawn_and_Garden_5.json.gz",
    "Pet_Supplies_5.json.gz",
    "Prime_Pantry_5.json.gz",
    "Software_5.json.gz",
    "Sports_and_Outdoors_5.json.gz",
    "Tools_and_Home_Improvement_5.json.gz",
    "Toys_and_Games_5.json.gz",
    "Video_Games_5.json.gz"
]

threshold = 100000
for dataset in datasets:
    # Open gzip files
    file = gzip.open(dataset, 'r')
    reviews = []
    for _ in range(threshold):
        line = file.readline()
        if not line: break
        review = json.loads(line.strip())
        reviews.append(review)
    file.close()

    # Filter only those with reviewText, and overall.
    filtered_reviews = []
    for review in reviews:
        try:
            text = review['reviewText']
            rating = review['overall']
            filtered_reviews.append((text, rating))
        except KeyError:
            continue

    # Save into csv
    name = "output/" + dataset.split(".")[0] + "(" + str(len(reviews)) + ").csv"
    output = open(name, "w", newline="")
    writer = csv.writer(output)
    writer.writerow(filtered_reviews)
    output.close()
