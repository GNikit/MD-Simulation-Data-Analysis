import os
import numpy as np
from md import StatQ, Isomorph, RDFAnalysis
import matplotlib.pyplot as plt

os.chdir("/home/gn/Desktop/test_data/isomorph")

# Generate the isomorph rho, T and A
# using a reference point of 0.5, 0.5 0.5

t_iso = np.linspace(0.5, 2.0, 5)
iso = Isomorph(0.5, 0.5, 0.5, t_iso)
rho_iso, a_iso = iso.gen_line(8)


obj = StatQ(15000, 10**3)

# Plotting the isomorphic scale data for VAF
for i in range(len(t_iso)):
    obj.vaf(rho_iso[i], t_iso[i], 8, a_iso[i], iso_scale=True)

# Find the isosbestic points
os.chdir("/home/gn/Desktop/test_data")
obj = StatQ(20000, 10**3)
n = [8, 10, 12]
rho = [0.3, 0.5, 1.0]
t = [0.5, 1.0, 2.0]
a = [0, 0.20, 0.25, 0.40, 0.50, 0.75, 0.8, 0.90]

# Plotting a RDF plot
obj.rdf_plot(0.5, 0.5, 8, 0.5)

# Generating the RDF intersection data
rdf_stat = RDFAnalysis(20000, 1000)
# rdf_stat.rdf_intersect(0.5, 0.5, n, 0.7)
# rdf_stat.get_intersections_to_file(rho, t, n, a, "/home/gn/Desktop")

# Plot the intersection points r_iso vs a
os.chdir("/home/gn/Desktop")
# for temp in t:
#     for density in rho:
#         rdf_stat.plot_intersection(density, temp)
plt.show()