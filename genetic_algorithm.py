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
        self.times = times  # 进化次数
        self.cars = maxCarNum  # 配送车辆总数
        self.tons = maxWeight  # 单次配送上限
        self.Pw = Pw  # 惩罚因子，当超过配送车辆总数，则惩罚，降低适应度大小
        self.Pm = Pm  # 变异率

    def run(self):
        # 初始化种群 group编码种群, decodeGroup解码种群， fitness适应度
        group, decodeGroup, fitness = self.initGroup()

        # 遗传算法过程
        for _ in range(0, self.times):
            # 初始化下一代种群
            nextGroup, nextDecodeGroup, nextFitness = self.initNextGroup()

            # 最优个体直接遗传到下一代
            maxFit, index = self.sorted(fitness)
            nextFitness[0], nextGroup[0], nextDecodeGroup[0] = maxFit, group[index], decodeGroup[index]
            print maxFit
            # 计算种群整体的适应度
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

            # 种群进化
            group, fitness, decodeGroup = nextGroup, nextFitness, nextDecodeGroup

        # 进化完成，打印最优个体
        maxFit, index = self.sorted(fitness)
        print self.calculateFitness(group[index])
        print 1 / maxFit

    # 计算个体适应度
    def calculateFitness(self, unit):
        totalNeed, totalDistance, totalDemond, arr, cur, pre = 1, 0, 0, [[]], 0, 0
        for i in unit:
            if totalDemond + self.demand[i] > self.tons:
                totalDistance, totalDemond, totalNeed, cur, pre = totalDistance + self.site[0][
                    pre], 0, totalNeed + 1, cur + 1, 0
                arr.append([])
            totalDistance, totalDemond, pre = totalDistance + self.site[pre][i], totalDemond + self.demand[i], i
            arr[cur].append(i)
        totalDistance += self.site[pre][0]

        # 适应度 = 1/总距离
        count = 0 if totalNeed <= self.cars else totalNeed - self.cars
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
                num = int(random.uniform(0, self.unitSize)) + 1
                if not self.isHas(groups[i], num):
                    groups[i][j] = num
                    j += 1
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

    # 线路中是否包含当前的客户
    def isHas(self, line, num):
        for i in range(0, self.unitSize):
            if line[i] == num:
                return True
        return False

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


site = [[0, 4, 6, 7.5, 9, 20, 10, 16, 8],
        [4, 0, 6.5, 4, 10, 5, 7.5, 11, 10],
        [6, 6.5, 0, 7.5, 10, 10, 7.5, 7.5, 7.5],
        [7.5, 4, 7.5, 0, 10, 5, 9, 9, 15],
        [9, 10, 10, 10, 0, 10, 7.5, 7.5, 10],
        [20, 5, 10, 5, 10, 0, 7, 9, 7.5],
        [10, 7.5, 7.5, 9, 7.5, 7, 0, 7, 10],
        [16, 11, 7.5, 9, 7.5, 9, 7, 0, 10],
        [8, 10, 7.5, 15, 10, 7.5, 10, 10, 0]]
demand = [1, 2, 3, 2, 1, 4, 2, 2]
#  site, demand, initGroupSize, times, maxCarNum, maxWeight, Pw, Pm
ga = GeneticAlgorithm(site=site, demand=demand, initGroupSize=100, times=100, maxCarNum=8, maxWeight=5, Pw=100, Pm=0.05)
ga.run()
