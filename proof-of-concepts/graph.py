import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import requests
from matplotlib import font_manager
from inky import InkyPHAT
from datetime import datetime, timedelta

def extractTimestamps(shelf):
  shelf = shelve.open('shelf')
  samples = shelf['weather']
  samples.getSamplesSince(datetime.now() - timedelta(hours=48))

def updateScreen(shelf):
  w, h = (212, 104)
  dpi = 144

  fig, ax = plt.subplots(figsize=(212/dpi, 104/dpi), dpi=dpi)
  fig.subplots_adjust(top=1, bottom=0, left=0.15, right=1)


  ticks_font = font_manager.FontProperties(fname='04B_03__.TTF', size=4)
  plt.rcParams['text.antialiased'] = False

  ax.yaxis.set_ticks(np.arange(0, 3, 1))
  for label in ax.get_yticklabels() :
      label.set_fontproperties(ticks_font)
  ax.yaxis.set_tick_params(pad=1, width=1)

  ax.xaxis.set_ticks([])
  ax.set_frame_on(False)

  plt.autoscale(enable=False)
  ax.plot(timestamps, values)
  ax.set_ylim(-.2, 2.2)
  ax.set_xlim(0, 15)
  ax.autoscale_view()


  with io.BytesIO() as f:
      inky_display = InkyPHAT("yellow")

      fig.savefig(f, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0)
      f.seek(0)
      i = Image.open(f)

      # ensure the image is using the correct pallet
      pal_img = Image.new('P', (1, 1))
      pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
      i = i.convert('RGB', palette=pal_img).quantize(palette=pal_img, dither=Image.NONE)

      inky_display.set_image(i)
      inky_display.show()
