from django.test import TestCase
from django.core.cache import cache
from django.db import IntegrityError
from embeds.templatetags.embed_filters import embedly
from embeds.models import SavedEmbed

class EmbedlyTemplateFilterTest(TestCase):
    """Warning: This will clear your cache. see below yo.
    """
    def setUp(self):
        text = {}

        text['photo'] = """<p>Wish I was here..</p>
        EMBED:http://www.flickr.com/photos/visualpanic/233508614/
        <p>!!!</p>
        """

        text['video'] = """3rd world democracy:
        galaaang Embed: http://www.youtube.com/watch?v=DCL1RpgYxRM
        """

        text['noop'] = """walk the line like an egyptian, but do not mess wit my links!
        do not embed this: http://en.wikipedia.org/wiki/Walk_Like_an_Egyptian<br/>
        or this: http://en.wikipedia.org/wiki/The_Bangles
        (piracy funds terrorism)
        """

        self.text = text
        cache.clear()

    def test_photo_embed(self):
        embed = embedly(self.text['photo'])
        self.assertTrue('<img' in embed)
        self.assertTrue('flickr' in embed)
        self.assertTrue('EMBED' not in embed)

    def test_video_embed(self):
        embed = embedly(self.text['video'])
        self.assertTrue('width' in embed)
        self.assertTrue('youtube' in embed)
        self.assertTrue('Embed' not in embed)

    def test_multi_embeds(self):
        embed = embedly(self.text['photo'] + self.text['video'])
        self.assertTrue('flickr' in embed)
        self.assertTrue('youtube' in embed)
        self.assertTrue('Embed' not in embed)
        self.assertTrue('EMBED' not in embed)

    def test_db_store(self):
        embed = embedly(self.text['video'])
        row = SavedEmbed.objects.get(url='http://www.youtube.com/watch?v=DCL1RpgYxRM')
        self.assertTrue('youtube' in row.html)

    def test_cache(self):
        embed = embedly(self.text['video'])
        row = SavedEmbed.objects.get(url='http://www.youtube.com/watch?v=DCL1RpgYxRM')
        last_updated = row.last_updated

        embed = embedly(self.text['video'])
        row = SavedEmbed.objects.get(url='http://www.youtube.com/watch?v=DCL1RpgYxRM')
        self.assertEqual(row.last_updated, last_updated)

    def test_db_fallback(self):
        url = 'http://www.youtube.com/watch?v=test_fail'
        text = 'Bad link. Embed: %s' % url

        SavedEmbed.objects.create(url=url, maxwidth=100, type='video',
                html='100')

        SavedEmbed.objects.create(url=url, maxwidth=200, type='video',
                html='200')

        embed = embedly(text, 200)
        self.assertTrue('200' in embed)
        self.assertTrue('Embed' not in embed)

    def test_leave_my_links_in_peace(self):
        embed = embedly(self.text['noop'])
        self.assertEqual(self.text['noop'], embed)

    def test_maxwidth(self):
        embed = embedly(self.text['video'], 333)
        self.assertTrue('333' in embed)

        embed = embedly(self.text['video'], 444)
        self.assertTrue('444' in embed)

    def test_unique_fields(self):
        url = 'http://www.youtube.com/watch?v=DCL1RpgYxRM'

        SavedEmbed.objects.create(url=url, maxwidth=100, type='video',
                html='100')
        SavedEmbed.objects.create(url=url, maxwidth=200, type='video',
                html='200')

        self.assertEqual(SavedEmbed.objects.count(), 2)

        self.assertRaises(IntegrityError, SavedEmbed.objects.create,
                url=url, maxwidth=100, type='video', html='this should break')

    def test_ignore_html(self):
        text = '<p>Embed: http://www.youtube.com/watch?v=DCL1RpgYxRM</p>'

        embedly(text)

        self.assertTrue(SavedEmbed.objects.all()[0].url,
            'http://www.youtube.com/watch?v=DCL1RpgYxRM')
