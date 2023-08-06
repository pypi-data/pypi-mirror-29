class ERRAutoWeb4Spider4DownloadTimeout(Exception):
    """
    文件下载失败（一般错误原因是：突然出现验证码需要人工确认，网络出现异常情况，等等）
    """

    def __init__(self, filename):
        super(ERRAutoWeb4Spider4NotExistSelectorDom, self).__init__()
        self.filename = filename

    def __str__(self):
        return '[%s]download file [%s] timeout' % (__class__, self.filename)


class ERRAutoWeb4Spider4NotExistSelectorDom(Exception):
    """
    页面元素CSS选择器不存在（一般原因是抓取页面发生升级结构调整，需要修改代码抓取逻辑。）
    """

    def __init__(self, url, selector):
        super(ERRAutoWeb4Spider4NotExistSelectorDom, self).__init__()
        self.url = url
        self.selector = selector

    def __str__(self):
        return '[%s] url [%s] has no selector dom [%s]' % (__class__, self.url, self.selector)
