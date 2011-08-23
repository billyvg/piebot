import re
import urllib2
import time
import traceback

try:
    import simplejson as json
except ImportError:
    import json

import gdata.youtube
import gdata.youtube.service

class Youtube(object):
    """Checks incoming messages for YouTube urls and parses the
    video details and statistics.

    """

    pattern = re.compile("http(s|)://(www\.|)youtu(?:\.be/|be\.com/.*?v=)([^&# ]+)")

    def __init__(self, *args, **kwargs):
        """Constructor."""
        pass

    def handle(self, match, **kwargs):
        try:
            data = self.fetch(match.group(3))

            m, s = divmod(int(data.media.duration.seconds), 60)
            h, m = divmod(m, 60)

            if h > 0:
                duration = '%dh %dm %ds' % (h, m, s)
            else:
                duration = '%dm %ds' % (m, s)

            ts = time.strptime(data.published.text[:19], '%Y-%m-%dT%H:%M:%S')
            timestamp = time.strftime('%m-%d-%Y', ts)
            return '\x02%s\x02 - length \x02%s\x02 - rated \x02%.1f\x02/5.0 (%d) - \x02%d\x02 views - Posted by \x02%s\x02 on \x02%s\x02' % (
                        data.media.title.text, duration,
                        float(data.rating.average), int(data.rating.num_raters),
                        int(data.statistics.view_count),
                        data.author[0].name.text,
                        timestamp
                    )

        except:
            print "Problem fetching video"
            print traceback.print_exc()


    def fetch(self, status_id):
        """Use gdata API to fetch the video."""

        yt = gdata.youtube.service.YouTubeService()
        data = yt.GetYouTubeVideoEntry(video_id=status_id)

        return data

