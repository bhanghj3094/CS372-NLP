#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, json, gzip, csv
import pandas as pd
import pprint

# Movie Dataset
datasets = [
    "2012",
    "A Beautiful Mind",
    "Amadeus",
    "Avatar",
    "Clash of the Titans",
    "Les Miserables",
    "Star Wars Episode I - The Phantom Menace",
    "The Expendables I",
    "The Godfather",
    "The Matrix Revolutions",
]

for index, dataset in enumerate(datasets):
    # Open ratings
    file = open(dataset + "/rating.txt", "r")
    ratings = file.readline().strip()
    ratings = ratings[len("rating = "):].replace(", ", "")
    ratings = ratings[2:-2].split()
    file.close()

    # Add reviews for each rating
    reviews = []
    for i in range(len(ratings)):
        file = open(dataset + "/" + str(i+1) + ".txt", "r")
        review = " ".join(file.read().strip().split("\n"))
        reviews.append((review, ratings[i]))
        file.close()

    # Save into csv
    name = "output/" + dataset + "(" + str(len(reviews)) + ").csv"
    output = open(name, "w", newline="")
    writer = csv.writer(output)
    writer.writerow(reviews)
    output.close()
