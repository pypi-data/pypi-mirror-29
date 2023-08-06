

def _raise():
    raise RuntimeError()


class UnpickleFail:
    def __reduce__(self):
        return _raise, ()


class SafeNested:
    def __init__(self, unsafe):
        self._obj = unsafe

    def __getstate__(self):
        return (pickle.dumps(self._obj),)

    def __setstate__(self, state):
        self.obj





if __name__ == "__main__":
    import pickle
