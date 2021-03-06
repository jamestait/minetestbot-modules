#!/usr/bin/env python
"""
title.py - Phenny URL Title Module
Copyright 2014, sfan5
"""

import re
import web
import html

r_title = re.compile(r'(?ims)<\s*title[^>]*>(.*?)<\s*/\s*title\s*>')

def title(phenny, input):
	uri = input.group(2)
	if uri:
		uri = uri.strip()
	elif hasattr(phenny.bot, 'last_seen_uri'):
		uri = phenny.bot.last_seen_uri
	else:
		return phenny.reply("Give me an URI..")
	data, sc = web.get(uri, 16384)
	if sc != 200:
		return phenny.say("HTTP error %d" % sc)
	try:
		data = str(data, 'utf-8')
	except UnicodeDecodeError:
		return phenny.say("Doesn't seem to be HTML..")
	m = re.search(r_title, data)
	if not m:
		return phenny.say("No title found.")
	title = m.group(1)
	title = html.unescape(title)
	title = title.strip()
	if len(title) > 150:
		title = title[:150] + "[...]"
	phenny.reply(title)

title.commands = ['title']

def noteuri(phenny, input):
	uri = input.group(1)
	setattr(phenny.bot, 'last_seen_uri', uri)

noteuri.rule = r'.*(https?://[^<> "\x01]+).*'
noteuri.priority = 'low'
noteuri.nohook = True
noteuri.thread = False

if __name__ == '__main__':
	print(__doc__.strip())
