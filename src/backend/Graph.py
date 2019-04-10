import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from scipy import stats

from backend.Trend import Trend


"""

"""
class Graph:


    def __init__(self, title, documentList):
        """

        """
        self._title = title
        self._testDocuments = documentList.getTrainTestDocuments(1)
        self._date, self._hr_ip, self._user_creator = self.__gatherData()
        self._indexDict = self.__compileIndexDict()


    def getTitle(self):
        """

        """
        return self._title

    def getFig(self):
        """

        """
        return self._fig

    def getAx(self):
        """

        """
        return self._ax

    def getAnnot(self):
        """

        """
        return self._annot


    def __gatherData(self):
        """

        """
        date_HR = []
        date_IP = []
        date = []
        hr_ip_HR = []
        hr_ip_IP = []
        hr_ip = []
        user_creator_HR = []
        user_creator_IP = []
        user_creator = []
        for document in self._testDocuments:
            if document.getClassInformation().getGt():
                date_IP.append(mdates.date2num(document.getPDFmetadata().getDate()))
                hr_ip_IP.append(document.getClassInformation().getIpRat() - document.getClassInformation().getHrRat())
                user_creator_IP.append(document.getClassInformation().getCreatorRat() - document.getClassInformation().getUserRat())
            else:
                date_HR.append(mdates.date2num(document.getPDFmetadata().getDate()))
                hr_ip_HR.append(document.getClassInformation().getIpRat() - document.getClassInformation().getHrRat())
                user_creator_HR.append(document.getClassInformation().getCreatorRat() - document.getClassInformation().getUserRat())
        date.append(date_HR)
        date.append(date_IP)
        hr_ip.append(hr_ip_HR)
        hr_ip.append(hr_ip_IP)
        user_creator.append(user_creator_HR)
        user_creator.append(user_creator_IP)
        return date, hr_ip, user_creator


    def create3dGraph(self):
        """

        """
        self._Xs = self._date
        self._Ys = self._hr_ip
        self._Zs = self._user_creator
        fig = Figure()
        ax = Axes3D(fig)
        Cs = ['Red', 'Blue']
        Ls = ['Human Rights Journal Article', 'Intellectual Property Journal Article']
        for i in range(len(self._Xs)):
            ax.scatter(self._Xs[i], self._Ys[i], self._Zs[i], s=40, marker='o', c=Cs[i], label=Ls[i])

        fig.legend()
        ax.set_ylim(-1, 1)

        ax.set_xlabel("Date of Publication", fontsize='large', fontweight='bold')
        ax.set_ylabel("HR-IP scale", fontsize='large', fontweight='bold')
        ax.set_zlabel("Creator-User scale", fontsize='large', fontweight='bold')
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        yearsFmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.tick_params(axis='x', labelrotation=90, which='major', pad=0)
        ax.tick_params(axis='y', labelrotation=45, which='major', pad=0)
        ax.tick_params(axis='z', labelrotation=45, which='major', pad=0)
        ax.xaxis.labelpad = 23
        ax.yaxis.labelpad = 18
        ax.zaxis.labelpad = 4
        ax.xaxis.label.set_color([0,0.733,0.839])
        ax.yaxis.label.set_color([0,0.733,0.839])
        ax.zaxis.label.set_color([0,0.733,0.839])

        self._ax = ax
        self._fig = fig


    def createIPHRgraph(self):
        """

        """
        self._Xs = self._date
        self._Ys = self._hr_ip
        fig = plt.figure()
        ax = plt.axes()
        Cs = ['Red', 'Blue']
        Ls = ['Human Rights Journal Article', 'Intellectual Property Journal Article']
        self._scs = []
        for i in range(len(self._Xs)):
            sc = ax.scatter(self._Xs[i], self._Ys[i], s=40, marker='o', c=Cs[i], label=Ls[i])
            self._scs.append(sc)

        hrTrend = Trend(self._Xs[0], self._Ys[0])
        ax.plot(hrTrend.getX(), hrTrend.getY(), '-r')

        ipTrend = Trend(self._Xs[1], self._Ys[1])
        ax.plot(ipTrend.getX(), ipTrend.getY(), '-b')


        self._annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                            bbox=dict(boxstyle="round", alpha=0.9,edgecolor=[0,0.733,0.839], fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self._annot.set_visible(False)



        ax.spines['left'].set_position(('axes', 0.0))
        ax.spines['right'].set_color('none')
        ax.yaxis.tick_left()
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        ax.xaxis.tick_bottom()

        plt.legend()
        ax.set_ylim(-1, 1)
        ax.set_xlabel("Date of Publication", fontsize='large', fontweight='bold')
        ax.set_ylabel("HR-IP scale", fontsize='large', fontweight='bold')
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        yearsFmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.tick_params(axis='x', labelrotation=90, which='major', pad=0)
        ax.tick_params(axis='y', labelrotation=45, which='major', pad=0)
        ax.xaxis.labelpad = 23
        ax.yaxis.labelpad = 18
        ax.xaxis.label.set_color([0,0.733,0.839])
        ax.yaxis.label.set_color([0,0.733,0.839])
        self._ax = ax
        self._fig = fig


    def createUserCreatorGraph(self):
        """

        """
        self._Xs = self._date
        self._Ys = self._user_creator
        fig = plt.figure()
        ax = plt.axes()
        Cs = ['Red', 'Blue']
        Ls = ['Human Rights Journal Article', 'Intellectual Property Journal Article']

        self._scs = []
        for i in range(len(self._Xs)):
            sc = ax.scatter(self._Xs[i], self._Ys[i], s=40, marker='o', c=Cs[i], label=Ls[i])
            self._scs.append(sc)


        userTrend = Trend(self._Xs[0], self._Ys[0])
        ax.plot(userTrend.getX(), userTrend.getY(), '-r')

        creatorTrend = Trend(self._Xs[1], self._Ys[1])
        ax.plot(creatorTrend.getX(), creatorTrend.getY(), '-b')


        self._annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                            bbox=dict(boxstyle="round", alpha=0.9,edgecolor=[0,0.733,0.839], fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self._annot.set_visible(False)

        ax.spines['left'].set_position(('axes', 0.0))
        ax.spines['right'].set_color('none')
        ax.yaxis.tick_left()
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        ax.xaxis.tick_bottom()

        plt.legend()
        ax.set_xlabel("Date of Publication", fontsize='large', fontweight='bold')
        ax.set_ylabel("User-Creator scale", fontsize='large', fontweight='bold')
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        yearsFmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.tick_params(axis='x', labelrotation=90, which='major', pad=0)
        ax.tick_params(axis='y', labelrotation=45, which='major', pad=0)
        ax.xaxis.labelpad = 23
        ax.yaxis.labelpad = 18
        ax.xaxis.label.set_color([0,0.733,0.839])
        ax.yaxis.label.set_color([0,0.733,0.839])

        self._ax = ax
        self._fig = fig


    def createIPHRUserCreatorGraph(self):
        """

        """
        self._Xs = self._hr_ip
        self._Ys = self._user_creator
        fig = plt.figure()
        ax = plt.axes()
        Cs = ['Red', 'Blue']
        Ls = ['Human Rights Journal Article', 'Intellectual Property Journal Article']

        self._scs = []
        for i in range(len(self._Xs)):
            sc = ax.scatter(self._Xs[i], self._Ys[i], s=40, marker='o', c=Cs[i], label=Ls[i])
            self._scs.append(sc)

        hrTrend = Trend(self._Xs[0], self._Ys[0])
        ax.plot(hrTrend.getX(), hrTrend.getY(), '-r')

        ipTrend = Trend(self._Xs[1], self._Ys[1])
        ax.plot(ipTrend.getX(), ipTrend.getY(), '-b')

        self._annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                            bbox=dict(boxstyle="round", alpha=0.9,edgecolor=[0,0.733,0.839], fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self._annot.set_visible(False)


        ax.spines['left'].set_position(('zero'))
        ax.spines['right'].set_color('none')
        ax.yaxis.tick_left()
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        ax.xaxis.tick_bottom()

        plt.legend()
        ax.set_xlabel("HR-IP scale", fontsize='large', fontweight='bold')
        ax.set_ylabel("User-Creator scale", fontsize='large', fontweight='bold')
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        yearsFmt = mdates.DateFormatter('%Y')
        ax.tick_params(axis='x', labelrotation=45, which='major', pad=0)
        ax.tick_params(axis='y', labelrotation=45, which='major', pad=0)
        ax.xaxis.labelpad = 10
        ax.yaxis.labelpad = 10
        ax.xaxis.label.set_color([0,0.733,0.839])
        ax.yaxis.label.set_color([0,0.733,0.839])
        self._ax = ax
        self._fig = fig


    def hover(self, event, canvas):
        """

        """
        vis = self._annot.get_visible()
        if event.inaxes == self._ax:
            for sc in self._scs:
                cont, ind = sc.contains(event)
                if cont:
                    self.__update_annot(sc, ind)
                    self._annot.set_visible(True)
                    canvas.draw_idle()
                else:
                    if vis:
                        self._annot.set_visible(False)
                        canvas.draw_idle()

    def __update_annot(self, sc, ind):
        """

        """
        pos = sc.get_offsets()[ind["ind"][0]]
        document = self._testDocuments[self._indexDict[tuple(pos)]]
        documentData = document.getPDFmetadata()
        self._annot.xy = pos
        text = "Title: {}\nJournal: {}\nDate: {}\nFilename: {}".format(                     \
            documentData.getTitle(),                                         \
            documentData.getJournal(),
            documentData.getDate(),
            document.getFilename())
        self._annot.set_text(text)


    def __compileIndexDict(self):
        """

        """
        indexDict = {}
        for c, document in enumerate(self._testDocuments):
            index = self._testDocuments
            classInfo = document.getClassInformation()
            hr_ip = classInfo.getIpRat() - classInfo.getHrRat()
            user_creator = classInfo.getCreatorRat() - classInfo.getUserRat()
            date = mdates.date2num(document.getPDFmetadata().getDate())
            indexDict[(date, hr_ip, user_creator)] = c
            indexDict[(date, hr_ip)] = c
            indexDict[(date, user_creator)] = c
            indexDict[(hr_ip, user_creator)] = c
        return indexDict