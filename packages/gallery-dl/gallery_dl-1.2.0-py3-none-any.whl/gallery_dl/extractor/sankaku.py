# -*- coding: utf-8 -*-

# Copyright 2014-2018 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://chan.sankakucomplex.com/"""

from .common import SharedConfigExtractor, Message
from .. import text, util, exception
from ..cache import cache
import time
import random


class SankakuExtractor(SharedConfigExtractor):
    """Base class for sankaku extractors"""
    basecategory = "booru"
    category = "sankaku"
    filename_fmt = "{category}_{id}_{md5}.{extension}"
    archive_fmt = "{id}"
    cookienames = ("login", "pass_hash")
    cookiedomain = "chan.sankakucomplex.com"
    subdomain = "chan"

    def __init__(self):
        SharedConfigExtractor.__init__(self)
        self.root = "https://" + self.cookiedomain
        self.logged_in = True
        self.start_page = 1
        self.start_post = 0
        self.wait_min = self.config("wait-min", 2)
        self.wait_max = self.config("wait-max", 4)
        if self.wait_max < self.wait_min:
            self.wait_max = self.wait_min

    def items(self):
        self.login()
        yield Message.Version, 1
        yield Message.Directory, self.get_metadata()

        for post_id in util.advance(self.get_posts(), self.start_post):
            self.wait()
            data = self.get_post_data(post_id)
            url = data["file_url"]
            yield Message.Url, url, text.nameext_from_url(url, data)

    def skip(self, num):
        self.start_post += num
        return num

    def get_metadata(self):
        """Return general metadata"""
        return {}

    def get_posts(self):
        """Return an iterable containing all relevant post ids"""

    def get_post_data(self, post_id, extr=text.extract):
        """Extract metadata of a single post"""
        url = self.root + "/post/show/" + post_id
        page = self.request(url, retries=10).text

        tags   , pos = extr(page, "<title>", " | ")
        vavg   , pos = extr(page, "itemprop=ratingValue>", "<", pos)
        vcnt   , pos = extr(page, "itemprop=reviewCount>", "<", pos)
        _      , pos = extr(page, "Posted: <", "", pos)
        created, pos = extr(page, ' title="', '"', pos)
        rating = extr(page, "<li>Rating: ", "<", pos)[0]

        file_url, pos = extr(page, '<li>Original: <a href="', '"', pos)
        if file_url:
            width , pos = extr(page, '>', 'x', pos)
            height, pos = extr(page, '', ' ', pos)
        else:
            width , pos = extr(page, '<object width=', ' ', pos)
            height, pos = extr(page, 'height=', '>', pos)
            file_url = extr(page, '<embed src="', '"', pos)[0]

        return {
            "id": util.safe_int(post_id),
            "md5": file_url.rpartition("/")[2].partition(".")[0],
            "tags": tags,
            "vote_average": float(vavg or 0),
            "vote_count": util.safe_int(vcnt),
            "created_at": created,
            "rating": (rating or "?")[0].lower(),
            "file_url": "https:" + text.unescape(file_url),
            "width": util.safe_int(width),
            "height": util.safe_int(height),
        }

    def wait(self):
        """Wait for a randomly chosen amount of seconds"""
        time.sleep(random.uniform(self.wait_min, self.wait_max))

    def login(self):
        """Login and set necessary cookies"""
        if self._check_cookies(self.cookienames):
            return
        username, password = self._get_auth_info()
        if username:
            cookies = self._login_impl((username, self.subdomain), password)
            for key, value in cookies.items():
                self.session.cookies.set(
                    key, value, domain=self.cookiedomain)
        else:
            self.logged_in = False

    @cache(maxage=90*24*60*60, keyarg=1)
    def _login_impl(self, usertuple, password):
        """Actual login implementation"""
        username = usertuple[0]
        self.log.info("Logging in as %s", username)
        params = {
            "url": "",
            "user[name]": username,
            "user[password]": password,
            "commit": "Login",
        }
        response = self.request(self.root + "/user/authenticate",
                                method="POST", params=params)
        if not response.history or response.url != self.root + "/user/home":
            raise exception.AuthenticationError()
        cookies = response.history[0].cookies
        return {c: cookies[c] for c in self.cookienames}


class SankakuTagExtractor(SankakuExtractor):
    """Extractor for images from chan.sankakucomplex.com by search-tags"""
    subcategory = "tag"
    directory_fmt = ["{category}", "{tags}"]
    pattern = [r"(?:https?://)?chan\.sankakucomplex\.com"
               r"/\?(?:[^&#]*&)*tags=([^&#]+)"]
    test = [
        ("https://chan.sankakucomplex.com/?tags=bonocho", {
            "count": 5,
            "pattern": (r"https://cs\.sankakucomplex\.com/data/[^/]{2}/[^/]{2}"
                        r"/[^/]{32}\.\w+\?e=\d+&m=[^&#]+"),
        }),
        ("https://chan.sankakucomplex.com/?tags=bonocho+a+b+c+d", {
            "options": (("username", None),),
            "exception": exception.StopExtraction,
        })
    ]
    per_page = 20

    def __init__(self, match):
        SankakuExtractor.__init__(self)
        self.tags = text.unquote(match.group(1).replace("+", " "))

    def skip(self, num):
        pages, posts = divmod(num, self.per_page)
        if pages > 49:
            self.log.info("Cannot skip more than 50 pages ahead.")
            pages, posts = 49, self.per_page
        self.start_page += pages
        self.start_post += posts
        return pages * self.per_page + posts

    def get_metadata(self):
        tags = self.tags.split()
        if not self.logged_in and len(tags) > 4:
            self.log.error("Unauthenticated users cannot use "
                           "more than 4 tags at once.")
            raise exception.StopExtraction()
        return {"tags": " ".join(tags)}

    def get_posts(self):
        params = {"tags": self.tags, "page": self.start_page}

        while self.logged_in or params["page"] <= 25:
            page = self.request(self.root, params=params, retries=10).text
            pos = page.find("<div id=more-popular-posts-link>") + 1

            ids = list(text.extract_iter(page, '" id=p', '>', pos))
            if not ids:
                return
            yield from ids

            params["page"] += 1
            params["next"] = int(ids[-1]) - 1

        self.log.warning(
            "Unauthenticated users may only access the first 500 images / 25 "
            "pages. (Use '--range 501-' to continue downloading from this "
            "point onwards after setting up an account.)")


class SankakuPoolExtractor(SankakuExtractor):
    """Extractor for image-pools  from chan.sankakucomplex.com"""
    subcategory = "pool"
    directory_fmt = ["{category}", "pool", "{pool}"]
    pattern = [r"(?:https?://)?chan\.sankakucomplex\.com/pool/show/(\d+)"]
    test = [("https://chan.sankakucomplex.com/pool/show/90", {
        "count": 5,
    })]
    per_page = 24

    def __init__(self, match):
        SankakuExtractor.__init__(self)
        self.pool_id = match.group(1)

    def skip(self, num):
        pages, posts = divmod(num, self.per_page)
        self.start_page += pages
        self.start_post += posts
        return num

    def get_metadata(self):
        return {"pool": self.pool_id}

    def get_posts(self):
        url = self.root + "/pool/show/" + self.pool_id
        params = {"page": self.start_page}

        while True:
            page = self.request(url, params=params, retries=10).text
            ids = list(text.extract_iter(page, '" id=p', '>'))

            yield from ids
            if len(ids) < self.per_page:
                return

            params["page"] += 1


class SankakuPostExtractor(SankakuExtractor):
    """Extractor for single images from chan.sankakucomplex.com"""
    subcategory = "post"
    pattern = [r"(?:https?://)?chan\.sankakucomplex\.com/post/show/(\d+)"]
    test = [("https://chan.sankakucomplex.com/post/show/360451", {
        "content": "5e255713cbf0a8e0801dc423563c34d896bb9229",
        "count": 1,
    })]

    def __init__(self, match):
        SankakuExtractor.__init__(self)
        self.post_id = match.group(1)

    def get_posts(self):
        return (self.post_id,)
