"""
This is a demo of creating a pdf file with several pages,
as well as adding metadata and annotations to pdf files.
"""

import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as pt
import matplotlib.pyplot as plt
import matplotlib.image as im

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
def single_plots_graph(l, b, w, h, cols, title, data):
    """This function sets the settings for the different plots using several parameters
    """
    subFig = plt.axes([l, b, w, h])
    plt.title("!!")
    for i in range(len(cols)):
        plt.plot(data[:, cols[i]]), plt.plot(data[:, cols[i]], color='black')

    plt.axhspan(0.5, 2.5, alpha=0.15, color="green")
    plt.axhspan(2.5, 6.5, alpha=0.15, color="yellow")
    plt.axhspan(6.5, 10, alpha=0.15, color="red")
    plt.yticks(np.arange(1, 10, step=1))
    plt.title(title, fontsize=8)
    plt.tick_params(axis="both", labelsize=5)


def single_plots_hist(l, b, w, h, index, title, data):
    """This function defines and plots the data as histograms
    """
    subFig = plt.axes([l, b, w, h])
    plt.hist(data[:,index], bins=18, range = (1,9), color='black', align='mid')
    plt.title(title, fontsize=8)
    plt.axvspan(1, 3, alpha=0.15, color="green")
    plt.axvspan(3, 7, alpha=0.15, color="yellow")
    plt.axvspan(7, 10, alpha=0.15, color="red")
    plt.tick_params(axis="both", labelsize=5)
    plt.yticks(np.arange(0,101,step=20))


def ampel_plot(data):
    """Perfoming an ample plot for final scores and each of the VALUES
    """
    l, b, w, h = .03, .03, .1, .1
    title = ["Arm li", "Arm re", "Arm combo", "Oberkörper", "Ober-Arm li", "Ober-Arm re", "Total"]
    for i in range(data.shape[1]):
        x, y = 0.5, 0.5
        if np.mean(data[:,i]) <= 3:
            color = "green"
        elif (np.mean(data[:,i]) > 3) and (np.mean(data[:,i]) <= 6):
            color = "yellow"
        else:
            color = "red"

        subPlot = plt.axes([l, b, w, h])
        circle = pt.Circle((x, y), radius=.45, color=color, fill=True)
        subPlot.add_artist(circle)
        plt.tick_params(axis="both", labelsize=0)
        plt.text(x, y, s=str(np.around(np.mean(data[:,i]), decimals=2)))
        plt.title(title[i], fontsize=8)
        l += 1/7


def rula_to_pdf(name, data):
    """This function generates a *.pdf Report
    name = Output Path (string); data = array (input)
    """
    plt.style.use('fivethirtyeight')
    width, height = 25/2.54, 29/2.54
    l, b, w, h = .95, .95, .95, .95
    image_path = ["../pics/skelett.png", "../pics/skelett_back.png"]
    with PdfPages(name + '.pdf') as pdf:
        fig = plt.figure(figsize=(width, height), dpi=200)
        # -1- first page
        # first half of page
        plt.axes([.02, .52, .99, .5])
        plt.text(0.4,0.9, s="Verlauf über die Zeit")
        plt.axis("off")
        single_plots_graph(.05, .84, 0.4, .1, [0,1], "Arm: li-re", data)
        single_plots_graph(.50, .84, 0.4, .1, [2], "Arm: komb.", data)
        single_plots_graph(.05, .69, 0.4, .1, [3], "Oberkörper", data)
        single_plots_graph(.50, .69, 0.4, .1, [4], "Final li (OK, Arm)", data)
        single_plots_graph(.05, .55, 0.4, .1, [5], "Final re (OK, Arm)", data)
        single_plots_graph(.50, .55, 0.4, .1, [6], "Final komb.", data)


        # second half of page
        plt.axes([.02, .02, .49, .5])
        plt.text(0.65,0.95, s="Prozentuale Verteilung pro Bereich")
        plt.axis("off")
        single_plots_hist(.05, .35, .4, .1, 0, "Arm: li", data)
        single_plots_hist(.50, .35, .4, .1, 2, "Arm: komb.", data)
        single_plots_hist(.05, .20, .4, .1, 3, "Oberkörper", data)
        single_plots_hist(.50, .20, .4, .1, 4, "Final li (OK, Arm)", data)
        single_plots_hist(.05, .05, .4, .1, 5, "Final re (OK, Arm)", data)
        single_plots_hist(.50, .05, .4, .1, 6, "Final komb.", data)


        pdf.savefig()  # saves the current figure into a pdf page

        # -2- plotting second page
        fig2 = plt.figure(figsize=(width, height), dpi=200)
        image = im.imread(image_path[0])
        subImg = plt.axes([.06, .4, .5, .55])
        #plt.axis("off")

        # adding a table to the picture showing statistical parameters
        rows = ["Oberarm", "Unterarm", "Hand", "Hals", "Oberkörper", "Beine"]
        cols = ["Mean", "SD", "Variance"]
        cell_text = np.random.randint(0,90, size=(6, 3)).astype(str)
        plt.table(cellText = cell_text, rowLabels = rows, colLabels = cols,
          loc='right', cellLoc = 'center', rowLoc = 'left', colLoc = 'center',
          colWidths = [0.2 for x in cols])
        plt.subplots_adjust(left=.9)

        # drawing circles onto the skeleton
        circle = pt.Circle((200, 200), radius=50, color="green", fill=True, alpha=.9)
        subImg.add_artist(circle)
        plt.imshow(image, interpolation="sinc")
        #plt.axis("off")

        # third third of page
        ampel_plot(data)

        pdf.savefig()

        plt.close()

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = 'RUlA Report'
        d['Author'] = 'Velamed GmbH'
        d['Subject'] = 'RULA Report based on myoMOTION data'
        d['Keywords'] = 'myoMOTION, RULA, Velamed'
        d['CreationDate'] = datetime.datetime.today()
        #d['ModDate'] = datetime.datetime.today()


test_array = np.random.rand(5000, 7)
name = "test"
rula_to_pdf(name, test_array)
