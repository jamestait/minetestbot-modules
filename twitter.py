#!/usr/bin/env python
"""
twitter.py - Phenny Twitter Module
Copyright 2012, Sean B. Palmer, inamidst.com
Modified by sfan5 2012
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, time
import web

r_username = re.compile(r'^@[a-zA-Z0-9_]{1,15}$')
r_link = re.compile(r'^https?://twitter.com/\S+$')
r_p = re.compile(r'(?ims)(<p class="js-tweet-text.*?</p>)')
r_tag = re.compile(r'(?ims)<[^>]+>')
r_anchor = re.compile(r'(?ims)(<a.*?</a>)')
r_expanded = re.compile(r'(?ims)data-expanded-url=["\'](.*?)["\']')
r_whiteline = re.compile(r'(?ims)[ \t]+[\r\n]+')
r_breaks = re.compile(r'(?ims)[\r\n]+')

def entity(*args, **kargs):
   return web.entity(*args, **kargs)

def decode(html):
   return web.r_entity.sub(entity, html)

def expand(tweet):
   def replacement(match):
      anchor = match.group(1)
      for link in r_expanded.findall(anchor):
         return link
      return r_tag.sub('', anchor)
   return r_anchor.sub(replacement, tweet)

def read_tweet(url):
   bytes, sc = web.get(url)
   bytes = str(bytes, 'utf-8')
   shim = '<div class="content clearfix">'
   if shim in bytes:
      bytes = bytes.split(shim, 1).pop()

   for text in r_p.findall(bytes):
      text = expand(text)
      text = r_tag.sub('', text)
      text = text.strip()
      text = r_whiteline.sub(' ', text)
      text = r_breaks.sub(' ', text)
      return decode(text)
   return "Sorry, couldn't get a tweet from %s" % url

def format(tweet, username):
   return '%s (@%s)' % (tweet, username)

def user_tweet(username):
   tweet = read_tweet('https://twitter.com/' + username + "?" + str(time.time()))
   return format(tweet, username)

def id_tweet(tid):
   link = 'https://twitter.com/twitter/status/' + tid
   headers, status = web.head(link)
   if status == 301:
      if not "Location" in headers:
         return "Sorry, couldn't get a tweet from %s" % link
      url = headers["Location"]
      username = url.split('/')[3]
      tweet = read_tweet(url)
      return format(tweet, username)
   return "Sorry, couldn't get a tweet from %s" % link

def twitter(phenny, input):
   arg = input.group(2)
   if not arg:
      return phenny.reply("Give me a link, a @username, or a tweet id")

   arg = arg.strip()
   log.log("event", "%s queried Twitter for '%s'" % (log.fmt_user(input), arg), phenny)
   if arg.isdigit():
      phenny.say(id_tweet(arg))
   elif r_username.match(arg):
      phenny.say(user_tweet(arg[1:]))
   elif r_link.match(arg):
      username = arg.split('/')[3]
      tweet = read_tweet(arg)
      phenny.say(format(tweet, username))
   else: phenny.reply("Give me a link, a @username, or a tweet id")

twitter.commands = ['tw', 'twitter']
twitter.thread = True

if __name__ == '__main__':
   print(__doc__)
