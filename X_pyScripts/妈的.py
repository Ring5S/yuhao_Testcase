class person:
    def __init__(self, person_age, person_height, person_name):
        self.age = person_age
        self.height = person_height
        self.name = person_name

    def echo_name(self, sex):
        self.sex = sex
        print(f"小人儿的名字是{self.name}，性别{self.sex}，年龄为{self.age}，身高为{self.height}厘米")

    def play_game(self, your_chip):
        self.chip = your_chip


if __name__ == '__main__':
    # person = person(person_age=18, person_height=200, person_name="jack_ma")
    # person.echo_name("男")
    def fun(i):
        i += 1
        if i < 3:
            print(f"{i}小于3嗷！")
            fun(i)

        else:
            print(f"{i}不小于3嗷！")
            return i

# result = fun(0)
# print(result)
i = 0
while i < 10000:
    i+=1
    print(i)