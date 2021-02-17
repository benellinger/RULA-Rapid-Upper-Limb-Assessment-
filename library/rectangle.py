import matplotlib.pyplot as plt
import matplotlib.patches as pt
import numpy as np
import datetime
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use('ggplot')
# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
x = np.linspace(-50, 50, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.power(x,3)
y4 = np.sqrt(np.abs(x))

width, height = 25/2.54, 29/2.54
with PdfPages('multipage_pdf.pdf') as pdf:
    fig = plt.figure(figsize=(width, height))
    a = plt.axes([.05, .8, .4, .16])
    plt.plot(x, y1)
    plt.tick_params(axis="both", labelsize=0.0)
    a = plt.axes([.55, .8, .4, .16])
    plt.tick_params(axis="both", labelsize=0.0)
    plt.plot(x, y2)
    a = plt.axes([.05, .6, .4, .16])
    plt.tick_params(axis="both", labelsize=0.1)
    plt.plot(x, y3)
    a = plt.axes([.55, .6, .4, .16])
    plt.tick_params(axis="both", labelsize=0.1)
    plt.axvspan(-10, 10, alpha=0.5)
    plt.plot(x, y4)

    # plt.rc('text', usetex=True)
    # rect1 = pt.Rectangle((0, 0), 10, 10)
    # ax1.add_patch(rect1)
    # ax1.set_title('Plot Two')
    # pdf.attach_note("plot of sin(x)")  # you can add a pdf note to
    #
    #
    # plt.rc('text', usetex=False)
    # rect2 = pt.Rectangle((0, 0), 10, 10)
    # ax2.add_patch(rect2)
    # ax2.set_title('Plot Three')

    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    plt.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009, 11, 13)
    d['ModDate'] = datetime.datetime.today()
