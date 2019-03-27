import json
import requests


def b_in():
	r = requests.get("https://newsapi.org/v2/top-headlines?sources=business-insider&apiKey=42037ac8c6be43eeb214e4f0fae0a896")
	f = r.json()

	b_in_arts = []
	for a in f["articles"]:
		b_in_arts.append([a['title'], a["content"][:-13], a["url"], a['urlToImage']])

	return(b_in_arts[:2])

def bloom():
	r = requests.get("https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=42037ac8c6be43eeb214e4f0fae0a896")
	f = r.json()
	bloom_arts = []
	for a in f["articles"]:
		bloom_arts.append([a['title'], a["content"][:-13], a["url"]])
	return(bloom_arts[:4])

def fin_t():
	r = requests.get("https://newsapi.org/v2/top-headlines?sources=financial-times&apiKey=42037ac8c6be43eeb214e4f0fae0a896")
	f = r.json()
	fin_t_arts = []
	for a in f["articles"]:
		fin_t_arts.append([a['title'], a["content"][:-13], a["url"]])
	return(fin_t_arts[:4])
