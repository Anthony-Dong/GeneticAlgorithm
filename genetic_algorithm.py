# -*- coding: UTF-8 -*-

# 遗传算法，574986060@qq.com

import random


# 遗传算法
class GeneticAlgorithm:
    def __init__(self, site, demand, initGroupSize, times, maxCarNum, maxWeight, Pw, Pm):
        self.site = site  # 位置坐标
        self.demand = [0] + demand  # 社区需求量
        self.unitSize = len(demand)  # 社区数量
        self.rows = initGroupSize  # 初始化总群大小
        self.times = times  # 遗传次数
        self.maxCarNum = maxCarNum  # 配送车辆总数
        self.maxWeight = maxWeight  # 单次配送上限
        self.Pw = Pw  # 惩罚因子，当超过配送车辆总数，则惩罚，降低适应度大小
        self.Pm = Pm  # 遗传变异率，区间[0,1]

    # 遗传算法主函数
    def run(self):
        # 初始化种群 group编码种群, decodeGroup解码种群， fitness适应度
        group, decodeGroup, fitness = self.initGroup()
        # 遗传算法过程
        for _ in range(0, self.times):
            # 初始化下一代种群
            nextGroup, nextDecodeGroup, nextFitness = self.initNextGroup()
            # 局部最优适应度个体直接遗传到下一代
            maxFit, index = self.sorted(fitness)
            nextFitness[0], nextGroup[0], nextDecodeGroup[0] = maxFit, group[index], decodeGroup[index]
            # 计算当前种群的整体适应度
            totalFit = sum(fitness)
            # 选择函数
            for i in range(1, len(group)):
                index = self.randomSelect(fitness, totalFit)
                nextGroup[i], nextDecodeGroup[i], nextFitness[i] = group[index], decodeGroup[index], fitness[index]
            for i in range(2, len(group), 2):
                # 交叉操作
                px, py = self.onePointCrossover(nextDecodeGroup[i - 1], nextDecodeGroup[i])
                # 变异操作
                if random.random() < self.Pm:
                    self.simpleMutation(px)
                if random.random() < self.Pm:
                    self.simpleMutation(py)
                nextGroup[i - 1], nextGroup[i] = px, py
                nextFitness[i - 1], nextDecodeGroup[i - 1] = self.calculateFitness(px)
                nextFitness[i], nextDecodeGroup[i] = self.calculateFitness(py)
            # 种群遗传
            group, fitness, decodeGroup = nextGroup, nextFitness, nextDecodeGroup
        # 遗传次数完成，打印最优个体
        _, index = self.sorted(fitness)
        print(self.calculateFitness(group[index]))

    # 计算个体适应度
    def calculateFitness(self, unit):
        totalNeed, totalDistance, totalDemond, arr, cur, pre = 1, 0, 0, [[]], 0, 0
        for i in unit:
            if totalDemond + self.demand[i] > self.maxWeight:
                totalDistance, totalDemond, totalNeed, cur, pre = totalDistance + self.site[0][
                    pre], 0, totalNeed + 1, cur + 1, 0
                arr.append([])
            totalDistance, totalDemond, pre = totalDistance + self.site[pre][i], totalDemond + self.demand[i], i
            arr[cur].append(i)
        totalDistance += self.site[pre][0]

        # 适应度 = 1/目标函数
        count = 0 if totalNeed <= self.maxCarNum else totalNeed - self.maxCarNum
        result = 1 / (totalDistance + count * self.Pw)
        return result, arr

    # 选择函数，轮盘赌选择
    def randomSelect(self, fit, totalFit):
        ran = random.uniform(0, totalFit)
        for i in range(0, len(fit)):
            ran -= fit[i]
            if ran < 0:
                return i

    # 交叉操作，单点交叉算法
    def onePointCrossover(self, px, py):
        index = random.randint(0, len(px) - 1 if len(px) < len(py) else len(py) - 1)
        px, py = [px[index]] + px, [px[index]] + py
        return self.fillUnit(px), self.fillUnit(py)

    # 变异操作,基本位变异
    def simpleMutation(self, unit):
        if random.random() < self.Pm:
            index1 = random.randint(0, len(unit) - 1)
            index2 = random.randint(0, len(unit) - 1)
            unit[index1], unit[index2] = unit[index2], unit[index1]

    # 初始化下一代种群
    def initNextGroup(self):
        return self.array(self.unitSize, self.rows), self.array(self.rows, 0, []), self.array(self.rows)

    # 初始化总群的随机生成函数
    def initGroup(self):
        groups = self.array(self.unitSize, self.rows)
        decodeGroup = self.array(self.rows, 0, [])
        fit = self.array(self.rows)
        for i in range(0, self.rows):
            j = 0
            while j < self.unitSize:
                num = random.randint(1, self.unitSize)
                if num not in groups[i]:
                    groups[i][j], j = num, j + 1
            # 计算第一代个体适应度
            fit[i], decodeGroup[i] = self.calculateFitness(groups[i])
        return groups, decodeGroup, fit

    def fillUnit(self, unit):
        arr = self.flap(unit)
        newArr = []
        for i in arr:
            if i not in newArr:
                newArr.append(i)
        return newArr

    def flap(self, unit):
        arr = []
        for row in unit:
            for i in row:
                if i is not 0:
                    arr.append(i)
        return arr

    # 生成多维数组
    def array(self, col, row=0, content=0):
        if row is 0:
            return [content for _ in range(col)]
        else:
            return [[content for _ in range(col)] for _ in range(row)]

    # 排序操作
    def sorted(self, fitness):
        index = 0
        maxFit = fitness[index]
        for i in range(self.rows):
            if maxFit < fitness[i]:
                maxFit, index = fitness[i], i
        return maxFit, index


site = [[0, 1.4, 2.0, 1.5, 0.68, 1.58, 1.12, 2.24, 1.52, 1.9],
        [1.4, 0, 1.23, 2.82, 1.92, 0.80, 0.92, 1.21, 1.91, 3.1],
        [2.0, 1.23, 0, 4.2, 3.5, 2.9, 1.21, 1.08, 1.4, 3.6],
        [1.5, 2.82, 4.2, 0, 1.12, 2.2, 2.65, 3.3, 2.98, 3.05],
        [0.68, 1.92, 3.5, 1.12, 0, 0.86, 1.62, 2.24, 2.12, 2.56],
        [1.58, 0.8, 2.9, 2.2, 0.86, 0, 1.23, 1.75, 2.23, 3.21],
        [1.12, 0.92, 1.21, 2.65, 1.62, 1.23, 0, 0.4, 0.62, 2.85],
        [2.24, 1.21, 1.08, 3.3, 2.24, 1.75, 0.4, 0, 1.42, 3.2],
        [1.52, 1.91, 1.4, 2.98, 2.12, 2.23, 0.62, 1.42, 0, 1.92],
        [1.9, 3.0, 3.6, 3.05, 2.56, 3.21, 2.85, 3.2, 1.92, 0]]
demand = [3, 4, 1, 3, 5, 4, 6, 2, 4]
#  site, demand, initGroupSize, times, maxCarNum, maxWeight, Pw, Pm
ga = GeneticAlgorithm(site=site, demand=demand, initGroupSize=100, times=100, maxCarNum=4, maxWeight=10, Pw=100,
                      Pm=0.01)
ga.run()
