# This is a sample Python script.
import csv

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
student = ('id', 'priority', 'prof', 'eng', 'sum', 'doc')
student_ru = ('№', 'Приоритет: ', 'Специальность: ', 'Иностранный язык: ', 'Балл ВИ: ', 'Оригиналы документов: ')


class CsvProcessor:
    def __init__(self, filename):
        self.filename = filename

    def re_write(self, source):
        if len(source) == 0:
            return

        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=student)
            writer.writeheader()
            for line in source:
                writer.writerow(line)

    def read_string(self):
        with open('eggs.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

    def check_string(self):
        pass


class SourceProcessor:
    def __init__(self, filename):
        self.list_of_dict = None
        self.filename = filename

    def clear_empty_lines(self):
        non_empty_lines = ()
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            non_empty_lines = (line for line in lines if not line.isspace())
        with open(self.filename, 'w') as f:
            f.writelines(non_empty_lines)

    def print_view(self, count=10):
        with open(self.filename, 'r') as r:
            for i in range(10):
                if i < count:
                    print(r.readline())

    def processor(self):
        self.list_of_dict = []
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            i = 0
            j = 0
            tmp_dict = {}
            while i < len(lines):
                for name in student:
                    tmp_dict[name] = lines[i][lines[i].find(student_ru[j]) + len(student_ru[j]):len(lines[i]) - 1:]
                    i = i + 1
                    j = j + 1
                self.list_of_dict.append(tmp_dict)
                tmp_dict = {}
                j = 0

    def get_list(self):
        if self.is_full():
            return self.list_of_dict
        else:
            return []

    def is_full(self):
        if len(self.list_of_dict) == 0:
            return False
        else:
            return True

    def print_list_view(self, count=10):
        if self.is_full():
            for i in range(count):
                print(self.list_of_dict[i])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sp = SourceProcessor('unsorted.txt')
    sp.print_view()
    sp.processor()
    sp.print_list_view()
    csvp = CsvProcessor('test.csv')
    csvp.re_write(sp.get_list())
    # sp.clear_empty_lines()
    # sp.print_view()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
