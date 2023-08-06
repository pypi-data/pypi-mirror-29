from rtv.options import DEFAULT_OPTIONS
from rtv.downloaders.youtubedl import YoutubePD


class Video:
    """ Video class."""
    def __init__(self, video_data):
        self.data = video_data

    def choose_format(self, quality):
        quality_func = {
            'worst': min,
            'best': max
        }
        formats = self.data.get('formats')
        if formats:
            func = quality_func[quality]

            def get_format_quality(f):
                """
                Get quality of a video. If quality key is present return its value, height otherwise.
                Args:
                    f (dict): format dictionary

                Returns:
                    Integer value of quality or height if present, None otherwise.

                """
                return f.get('quality') or f.get('height')

            if len(formats) > 1:
                video_formats = list(filter(get_format_quality, formats))
                # TODO: Refactor this solution
                choice = func(video_formats or formats, key=get_format_quality)
            else:
                choice = formats[0]

            # TODO: Fix IT!!!! it might mix quality with height
            # In[5]: min([{'height': 24}, {'quality': 23, 'height': 0}], key=lambda f: f.get(
            #     ...: 'quality') or f.get('height'))
            # Out[5]: {'height': 0, 'quality': 23}
        else:
            choice = self.data
            # not sure about clarity, but self.data contains all format information
            # if there is not 'formats' key in the dictionary
        return choice

    def info(self, quality='worst'):
        """
        Get video info, depending on the given quality. If there are no formats in video data,
        return the values associated with the entire video, not with any specific quality.
        Args:
            quality (str): String representation of quality ('worst'/'best'), worst by default.

        Returns:
            dict: Dictionary containing most important information about the video of given
            quality, i.e. url, ext, but also more general information such as title, show name,
            date.

        """

        f = self.choose_format(quality)
        return {
            'title': self.data.get('title'),
            'show_name': self.data.get('show_name'),
            'date': self.data.get('date'),

            # format specific data
            'url': f.get('url'),
            'ext': f.get('ext'),
        }

    def ext(self, quality: str) -> str:
        data = self.info(quality)
        return data['ext']

    def url(self, quality: str) -> str:
        data = self.info(quality)
        return data['url']

    @property
    def title(self):
        return self.data.get('title')

    def print_data(self):
        """
        Pretty print all attributes (info) of this video instance.

        Returns:
            None

        """
        import pprint
        pprint.pprint(self.data)

    def download(self, quality: str = None, **kwargs):
        """
        Download this video in the given quality. Invoke with keyword arguments
        to change default options.

        Args:
            quality (:py:obj:`str`, optional): Quality of the video ('best'/'worst').
                Defaults to 'worst'.
            **kwargs: Arbitrary keyword arguments used to update options, e.g. dl_path.

        Returns:
            None

        """
        # TODO: Fix option passing don't use defaults.
        options = DEFAULT_OPTIONS
        options.update(kwargs)

        if not quality:
            quality = options.get('quality', 'worst')

        video = self
        ypd = YoutubePD(video, options)
        ypd.download(quality)

    # TODO: fix repr
    def __repr__(self):
        return f"<Video {{'url': '{self.info()['url']}', 'title': '{self.info()['title']}'}}>"

    def __str__(self):
        return self.title
