# hnpy  
*a Hacker News API wrapper written in Python*

[![Build Status](https://travis-ci.org/jarhill0/hnpy.svg?branch=master)](https://travis-ci.org/jarhill0/hnpy)
[![Coverage Status](https://coveralls.io/repos/github/jarhill0/hnpy/badge.svg?branch=master)](https://coveralls.io/github/jarhill0/hnpy?branch=master)

---

## Purpose

This was written with the goal of sticking close to the API in terms of naming and structure, but with the added 
benefits that come with using Python objects.

## Installation

Use one of the following, depending on how your system is configured:

```shell
pip install hnpy
pip3 install hnpy
python3 -m pip install hnpy
```

## Usage

Create an instance of the main class like this:

```python
import hnpy

hn = hnpy.HackerNews()
```


### Items

If you know an item's ID, you can access it like this:

```python
post = hn.item(8863)
```

An Item can be one of five types: "job", "story", "comment", "poll", or "pollopt." You can determine its type by 
accessing `post.type`.

Item objects are loaded lazily, meaning they only make network requests when information that they don't already have 
is needed.

Items can be checked for equality against other Items or against the ID in `int` or `str` form.

Items have various attributes which depend on their type. You can use `hasattr()` to programmatically determine 
whether a certain Item has an attribute or not. More on attributes [here](https://github.com/HackerNews/API#items). 
Attribute names in hnpy are copied from field names in the API.

Items have five special attributes: 

Attribute name | Explanation
---|---
content | The "meat" of the Item — `text`, `url`, or `title`, with a fallback to an empty string if none exist.
link | URL to access the Item.
parent | Item that this one replies to (not always present).
poll | Item of type `poll` that this one belongs to (only present on `pollopt` Items).
by | User who created this Item.

The `link` and `content` attributes are noted here because the API does not directly provide them, so they are not 
documented elsewhere. The `parent`, `poll` and `by` attributes are noted because they contain fully-featured, 
lazily-loaded Items as opposed to just the IDs that the API responds with. The rest of an Items attributes are 
delivered in the same format that they are received from the API. 

The attributes can be accessed like so:

```python
post.content
post.link
post.parent
post.poll
post.by
```

Items also have 2 special methods which iterate and deliver Items. Each takes an optional `limit=` parameter which 
defaults to 25. 

Method name | Use
---|---
kids() | Iterate over the comments that reply to this Item.
parts() | Iterate over the options of this Item (only present on `poll` types).

The methods can be used like this:

```python
for kid in post.kids(limit=5):
    print(kid.content)
for opt in post.parts():
    print(opt.content)
```


### Listings

You can use hnpy to view the following listings provided by Hacker News:

- Top (this is the view shown on the homepage of Hacker News)
- Best
- New
- Ask HN Stories
- Show HN Stories
- Job Stories

Just like the special methods of an Item, these methods of a HackerNews object take an optional `limit=` parameter. 
They iterate over the specified listing, yielding lazy Items as they go. 

Example:

```python
for post in hn.best(limit=5):
    print(post.link)
```

The method names are:

- `top()`
- `best()`
- `new()`
- `ask()`
- `show()`
- `jobs()`


### Users

A User can be created from a user's name using the `HackerNews.user()` method:

```python
user = hn.user('jl')
```

Besides the attributes [noted in the Hacker News API documentation](https://github.com/HackerNews/API#users), Users 
contain the following attributes and methods:

Attribute/method name | Purpose
---|---
link | A URL to view the User's profile online.
submitted() | Iterate over Items created by the user, with optional `limit=` parameter. 


### Misc

The HackerNews object has a method `updates()` which returns an Updates object, which has iterating methods just like 
those of other objects (optional `limit=` parameter, objects yielded) which give the most recently changed item and 
profiles (more info [here](https://github.com/HackerNews/API#changed-items-and-profiles)). Its two methods are 
`items()` and `profiles()`.

The HackerNews object also has a method `max_item()` which returns a lazy version of the newest Item. 

## Credits

This package came originally from my [A Bot](https://github.com/jarhill0/abot) project. It was adapted to support 
lazy loading of objects, and as a consequence has only four classes (HackerNews, Item, User, Updates), rather than 
having a class for every type of Item with a complex inheritance model. This version also supports Users and Updates, 
which the old version did not. 

This package was inspired by the Python Reddit API Wrapper aka PRAW
([docs](https://praw.readthedocs.io/en/latest/)/[source](https://github.com/praw-dev/praw/)) in its use of objects 
and iteration methods and `limit=` parameters.