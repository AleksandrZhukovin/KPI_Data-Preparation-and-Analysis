import rasterio
from matplotlib import pyplot as plt

dataset = rasterio.open('pan2.jp2')
print(dataset.shape)
band1 = dataset.read(1)
# band2 = dataset.read(2)
# band3 = dataset.read(3)
# band4 = dataset.read(4)
plt.imshow(band1)
plt.show()
# plt.imshow(band2)
# plt.show()
# plt.imshow(band3)
# plt.show()
# plt.imshow(band4)
# plt.show()
