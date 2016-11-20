


class Person(object):
    def __init__(self,a,b):
        self.__dict__.update()


    def to_dict(self):
        return self.__dict__


if __name__ == '__main__':
    p = Person()

    print(p.to_dict())