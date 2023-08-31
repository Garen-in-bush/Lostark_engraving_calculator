import itertools


def check_jewelries_with_template(jewelries, template):
    for i in range(len(jewelries)):
        if template[i]:
            if template[i] not in jewelries:
                return False
    return True


def change_order(jewelries, template):
    res = []
    jewelries = list(jewelries)
    for i in range(len(template)):
        if template[i]:
            res.append(template[i])
            for j in range(len(jewelries)):
                if jewelries[j] == template[i]:
                    del jewelries[j]
                    break
    for jewelry in jewelries:
        res.append(jewelry)
    return res


def get_jewelry_with_template(target, template):
    # 定义所有可能的首饰组合
    jewelry_combinations = list(itertools.combinations_with_replacement(itertools.product(target, repeat=2), 5))
    res = []
    for jewelries in jewelry_combinations:
        flag = False
        if not check_jewelries_with_template(jewelries, template):
            continue
        for item in jewelries:
            if item[0] == item[1]:
                flag = True
                break
        if flag:
            continue
        res.append(jewelries)
    return res


def calculate(target, template, stones, talents):
    # 定义所有可能的首饰组合
    jewelry_combinations = get_jewelry_with_template(target, template)
    # 定义所有可能的能力石组合
    stone_combinations = [(stones[0], stones[1])]
    # 定义所有可能的天赋栏位组合
    talent_combinations = [(talents[0], talents[1])]

    result = []
    # 搜索所有可能的组合
    for jewel_comb in jewelry_combinations:
        for stone_comb in stone_combinations:
            for talent_comb in talent_combinations:
                # 初始化刻印点数
                points = {inscription: 0 for inscription in target}

                # 添加首饰点数
                flag = False
                for jewel in jewel_comb:
                    points[jewel[0]] += 5
                    points[jewel[1]] += 3

                if flag:
                    continue
                # 添加能力石点数
                points[stone_comb[0]] += 7
                points[stone_comb[1]] += 7

                # 添加天赋栏位点数
                points[talent_comb[0]] += 12
                points[talent_comb[1]] += 9

                # 检查是否所有刻印都达到15点
                if all(value == 15 for value in points.values()):
                    result.append(change_order(jewel_comb, template))
    return result
