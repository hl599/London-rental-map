import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
def transparency(x):
    return hex(round((x + 5) / 15 * 500))[-2:]


def color_dic():
    # Normalize the 'crime_rate' values for both color and transparency
    norm = mcolors.Normalize(vmin=-5, vmax=9)
    cmap = plt.get_cmap('Oranges')

    def normalized_to_rgba(val):
        rgba_color = list(cmap(norm(val)))  # Returns [R, G, B, A]
        return mcolors.to_hex(rgba_color)  # Convert RGBA to hex

    color_dict = []
    for i in range(10):
        color_dict.append(f"{transparency(i)}{normalized_to_rgba(i)[5:7]}{normalized_to_rgba(i)[3:5]}{normalized_to_rgba(i)[1:3]}")
    return color_dict