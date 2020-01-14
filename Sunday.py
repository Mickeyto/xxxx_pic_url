class Sunday:
    _table = []

    def search(self, haystack, needle):
        haystack_len = len(haystack)
        needle_len = len(needle)

        if needle_len > haystack_len:
            return -1

        diff = haystack_len - needle_len
        print(diff)
        self.prefix_table(needle)

    def prefix_table(self, needle):
        print(needle)


if __name__ == '__main__':
    print("test")
    sunday = Sunday()
    sunday.search('test', 'test')