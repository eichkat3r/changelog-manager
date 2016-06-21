class Version(object):
    def __init__(self, major, minor=None, patch=None):
        if minor == None and patch == None:
            s = major.split('.')
            major = int(s[0])
            minor = int(s[1])
            patch = int(s[2])
        self.major = major
        self.minor = minor
        self.patch = patch

    def increment(self):
        self.patch += 1

    def __gt__(self, v):
        if not isinstance(v, Version):
            raise NotImplementedError
        if self.major > v.major:
            return True
        if self.major == v.major and self.minor > v.minor:
            return True
        if self.major == v.major and self.minor == v.minor and self.patch > v.patch:
            return True
        return False

    def __str__(self):
        return '%d.%d.%d' % (self.major, self.minor, self.patch)

