# -*- coding=utf-8 -*-
# 整理: A.Star chenxiaolong12315@163.com
# 使用时请保留此信息

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
import time
import itertools

npm = np.mat
npa = np.array


class Kohonen(object):
    def __init__(self, dataMat=None, steps=1000, M=2, N=2):
        self.lratemax = 0.8  # 最大学习率-欧式距离
        self.lratemin = 0.05  # 最小学习率-欧式距离
        self.rmax = 5  # 最大聚类半径--根据数据集
        self.rmin = 0.5  # 最小聚类半径--根据数据集
        self.Steps = steps  # 迭代次数
        self.lratelist = []
        self.rlist = []
        self.w = []
        self.M = M
        self.N = N
        if dataMat is None:
            self.dataMat = []  # 外部导入数据集
        else:
            self.dataMat = npm(dataMat)
        self.classLabel = []  # 聚类后的类别标签

    def loadData(self, data, split_char='\t'):  # 加载数据文件

        if isinstance(data, str):
            fileName = data
        else:
            self.dataMat = npm(data)
            return
        fr = open(fileName)
        for line in fr.readlines():
            curLine = line.strip().split(split_char)
            lineArr = []
            lineArr.append(float(curLine[0]))
            lineArr.append(float(curLine[1]))
            self.dataMat.append(lineArr)
        self.dataMat = np.mat(self.dataMat)

    def file2matrix(self, path, delimiter):
        fp = open(path)
        content = fp.read()
        fp.close()
        rowlist = content.splitlines()  # 按行转换为一维表
        # 逐行遍历      # 结果按分隔符分割为行向量
        recordlist = [map(eval, row.split(delimiter)) for row in rowlist if row.strip()]
        # 返回转换后的矩阵形式
        self.dataMat = np.mat(recordlist)

    def normalize(self, dataMat):
        [m, n] = np.shape(dataMat)
        for i in range(n):
            dataMat[:, i] = (dataMat[:, i] - np.mean(dataMat[:, ])) / np.std(dataMat[:, ])
        return dataMat

    def distEclud(self, matA, matB):
        return dist.cdist(matA, matB.T)

    def init_grid(self):  # 初始化第二层网格
        # 构建低二层网络模型
        # 数据集的维度即网格的维度，分类的个数即网格的行数

        itor = itertools.product(range(self.M), range(self.N))
        grid = [list(x) for x in itor]
        return npm(grid)

    def ratecalc(self, i):
        lrate = self.lratemax - (i + 1.0) * (self.lratemax - self.lratemin) / self.Steps
        r = self.rmax - ((i + 1.0) * (self.rmax - self.rmin)) / self.Steps
        return lrate, r

    # 主程序
    def train(self):
        # 1.构建输入层网络
        dm, dn = np.shape(self.dataMat)
        # 归一化数据
        normDataSet = self.normalize(self.dataMat)
        # 2.初始化第二层分类网络
        grid = self.init_grid()
        # 3.随机初始化两层之间的权重向量
        self.w = np.random.rand(dn, self.M * self.N)
        distM = self.distEclud  # 确定距离公式
        # 4.迭代求解
        if self.Steps < 5 * dm:
            self.Steps = 5 * dm  # 设定最小迭代次数
        for i in range(self.Steps):
            lrate, r = self.ratecalc(i)  # 1.计算当前迭代次数下的学习率和学习聚类半径
            self.lratelist.append(lrate);
            self.rlist.append(r)
            # 2.随机生成样本索引，并抽取一个样本
            k = np.random.randint(0, dm)
            mySample = normDataSet[k, :]
            # 3.计算最优节点：返回最小距离的索引值
            minIndx = (distM(mySample, self.w)).argmin()
            # 4.计算领域
            d1 = np.ceil(minIndx / self.M)  # 计算此节点在第二层矩阵中的位置
            d2 = np.mod(minIndx, self.M)
            distMat = distM(np.mat([d1, d2]), grid.T)
            nodelindx = (distMat < r).nonzero()[1]  # 获取领域内的所有点
            for j in range(np.shape(self.w)[1]):
                if sum(nodelindx == j):
                    self.w[:, j] = self.w[:, j] + lrate * (mySample[0] - self.w[:, j])
        # 主循环结束

        self.classLabel = np.zeros(dm)  # 分配和存储聚类后的类别标签
        for i in range(dm):
            self.classLabel[i] = distM(normDataSet[i, :], self.w).argmin()
        self.classLabel = np.mat(self.classLabel)
        return self.w

    def showCluster(self, plt):  # 绘图
        plt.figure()
        lst = np.unique(self.classLabel.tolist()[0])  # 去重
        i = 0
        colorMap = ['bo', 'rd', 'gD', 'c^', 'k+', 'y*']
        for cindx in lst:
            myclass = np.nonzero(self.classLabel == cindx)[1]
            xx = self.dataMat[myclass].copy()
            plt.plot(xx[:, 0], xx[:, 1], colorMap[i % 6])
            i += 1
        plt.show()

    def drawW(self):
        w = self.w
        mmap = w / (np.max(w) - np.min(w)) + np.min(w)
        plt.figure()
        plt.imshow(mmap)
        plt.show()
SOM = Kohonen
