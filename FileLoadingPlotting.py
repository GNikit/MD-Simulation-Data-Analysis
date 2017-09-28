import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Look for improvements

class FilePlotting:
    """
    Class responsible for Plotting the data generated by the MD simulation
    software written in C++.
    Constructor purposly does not have any arguments
    """

    def __init__(self):
        self.sep = "~"
        self.dif_coef = np.array([])
        self.reduced_dif_coef = np.array([])
        self.dif_err = np.array([])
        self.reduced_dif_err = np.array([])
        self.dif_y_int = np.array([])
        self.reduced_dif_y_int = np.array([])
        self.line_style = ['solid', 'dashed', 'dotted', 'dashdot']

        # Colors used for plots
        self.color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                          '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                          '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
        self.color_sequence2 = ['#1f77b4', '#ff7f0e', '#2ca02c',
                           '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                           '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                           '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
        # This is an iterator for the color array
        self.p, self.c = 0, 0
        self.j = 0
        self.v = 0
        self.s = 0
        self.line_it = 0

    def energy_plots(self, power, par_a):
        power_str = str(power)
        A = "{:.2f}".format(par_a)
        Data = "Data" + power_str + self.sep + A + ".txt"

        #  Loads the files from the dir
        # num_lines = sum(1 for line in open(Data))  # Calculates the num of lines in a file
        num_lines = 0
        for line in open(Data):
            if line.startswith('#'):
                continue
            num_lines += 1

        KE, U, Tot = np.loadtxt(Data, usecols=(1, 2, 3), delimiter='\t',
                                comments='#', unpack=True)

        #  Plots the Energies
        step = 0.005
        time = num_lines * step
        x = np.linspace(0, time, num_lines)
        fig = plt.figure()

        Kin = plt.subplot2grid((3, 2), (0, 0), colspan=1)
        Pot = plt.subplot2grid((3, 2), (1, 0), colspan=1)
        TOT = plt.subplot2grid((3, 2), (2, 0), colspan=1)
        All = plt.subplot2grid((3, 2), (0, 1), rowspan=3)

        k, u, t = KE[500], U[500], Tot[500]
        Kin.plot(x, KE, 'r')
        Kin.locator_params(axis='y', nbins=4), Kin.set_ylim(ymax=4)
        Pot.plot(x, U, 'g')
        Pot.locator_params(axis='y', nbins=3)
        Pot.set_ylabel("Energy units", size=16)
        TOT.plot(x, Tot, 'b')
        TOT.locator_params(axis='y', nbins=4)
        TOT.set_ylim(ymax=6)

        x_r = time / 2 - time / 4
        # Kin.set_title('Individual Plots n = %d' %power, fontsize=17)
        Kin.set_title('Individual Plots', fontsize=17)
        All.set_title('Energy Contributions', fontsize=17)
        All.set_xlabel(r"Time $t$", fontsize=16)

        TOT.set_xlabel(r"Time $t$", fontsize=16)
        fig.subplots_adjust(hspace=0)

        for ax in [Kin, Pot]:
            plt.setp(ax.get_xticklabels(), visible=False)
            # The y-ticks will overlap with "hspace=0", so we'll hide the bottom tick
            ax.set_yticks(ax.get_yticks()[1:])

        All.plot(x, KE, 'r', x, U, 'g', x, Tot, 'b')
        All.set_ylim(ymax=5)

    def particle_plot(self, power, par_a):
        """
        3D Plot of the cubic container showcasing the position of the particles
        :param power: n of the pair potential
        :param par_a: parameter A of the pair potential
        :return:
        """
        power_str = str(power)
        A = "{:.2f}".format(par_a)

        data = "Positions_Velocities" + power_str + self.sep + A + ".txt"

        rx, ry, rz = np.loadtxt(data, usecols=(0, 1, 2), delimiter='\t',
                                comments='#', unpack=True)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        S = ax.scatter(rx, ry, rz, c=rz, cmap='gnuplot_r')
        plt.colorbar(S)

    def vector_field(self, power, par_a):
        power_str = str(power)
        A = "{:.2f}".format(par_a)
        data = "Positions_Velocities" + power_str + self.sep + A + ".txt"

        rx, ry, rz, vx, vy, vz = np.loadtxt(data,
                                            usecols=(0, 1, 2, 3, 4, 5),  # redundant
                                            delimiter='\t',
                                            comments='#',
                                            unpack=True)

        # num_lines = sum(1 for line in open(RX))  # Calculates the num of lines in a file
        # d = np.linspace(0,num_lines,num_lines)
        # plt.plot(d,vz)
        # erx = np.sqrt(vx**2+vz**2)
        # ery = np.sqrt(vy**3+vz**2)
        plt.figure()
        name = "n: " + power_str + "  A: " + A
        Q = plt.quiver(rx, ry, vx, vy, rz, pivot='mid', cmap='gnuplot_r', alpha=0.75, label=name)
        # plt.scatter(rx, ry, alpha=0.4, label=name)
        plt.colorbar(Q)
        plt.legend(loc="upper right")

    def vector_field3D(self, power, par_a):
        power_str = str(power)
        A = "{:.2f}".format(par_a)
        data = "Positions_Velocities" + power_str + self.sep + A + ".txt"

        rx, ry, rz, vx, vy, vz = np.loadtxt(data,
                                            usecols=(0, 1, 2, 3, 4, 5),  # redundant
                                            delimiter='\t',
                                            comments='#',
                                            unpack=True)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # v = np.sqrt(vx**2 + vy**2 + vz**2)
        name = "n: " + power_str + "  A: " + A
        Q = plt.quiver(rx, ry, rz, vx, vy, vz, rz,
                       label=name, alpha=0.7, normalize=True,
                       cmap='gnuplot_r')
        plt.colorbar(Q)
        plt.legend(loc="upper right")

    # RDF Histogram
    def radial_dist_func(self, power, par_a):
        power_str = str(int(power))
        A = "{:.2f}".format(par_a)
        HIST = "Hist" + power_str + self.sep + A + ".txt"
        # num_lines = len(open(HIST))
        num_lines = sum(1 for line in open(HIST))  # yields size=101, index=100
        Hist = np.loadtxt(HIST, delimiter="\n")
        # gr is supposed to have 101 entries since the boundaries are 0 and cut_off
        # and both of them are inclusive
        print(num_lines)
        # print(Hist.size)

        N, rho, Nhist = 10 ** 3, 0.5, 100
        rg = ((N / rho) ** (1. / 3.)) / 2.
        dr = rg / Nhist

        x = np.linspace(0, 99, 100)
        pwr = float(power)
        force_max = (par_a
                     / (1. + pwr)) ** (0.5)
        x = np.multiply(x, dr)
        name = "n: " + power_str  # "  A: " + A  # "n: " + power_str +
        max_scaling = np.max(Hist)  # Scaling the ymax
        plt.figure(3)
        iso = np.sqrt(1 - par_a)
        plt.plot(x, Hist, 'o-', markersize=4, label=name, color=self.color_sequence2[self.c])
        plt.xlabel(r"$r$", fontsize=16)
        plt.ylabel(r"$g(r)$", fontsize=16)
        plt.plot([0, x[-1]], [1, 1], '--', color='black', linewidth=0.5)
        plt.plot([iso, iso], [0, max_scaling + 0.1], '--', color='red')
        plt.xlim(xmin=0, xmax=5)
        plt.ylim(ymin=0, ymax=max_scaling + 0.1)
        plt.legend(loc="upper right", fancybox=True)
        self.c += 1
        self.line_it += 1

    # VAF
    def vel_autocor_func(self, power, par_a):
        # Changes the directory
        power_str = str(power)
        A = "{:.2f}".format(par_a)

        vaf = "VAF" + power_str + self.sep + A + ".txt"

        cr = np.loadtxt(vaf, delimiter='\n')
        num_lines = sum(1 for line in open(vaf))
        time = 0.005 * num_lines
        xxx = np.linspace(0, time, num=num_lines)
        name = ""
        if num_lines < 7000:
            name = "n: " + power_str + "  A: " + A

        plt.figure(5)
        y = np.full(num_lines, 0)
        xx = np.full(num_lines, time)
        yy = np.linspace(5, -0.5, num_lines)
        plt.plot(xx, yy, '--', color='black')
        plt.plot(xxx, y, '--', color='black')
        plt.plot(xxx, cr, label=name)  # ,color=color_sequence2[p])
        # plt.title("Velocity Autocorrelation Functions (VAF) ")
        plt.xlabel(r"Time $t$", fontsize=18)
        plt.ylabel(r"$C_v$", fontsize=18)
        plt.ylim(ymax=5, ymin=-0.5)
        plt.legend(loc="upper right", ncol=1, borderpad=0.1,
                   labelspacing=0.01, columnspacing=0.01, fancybox=True,
                   fontsize=16)
        self.p += 1

    # MSD
    def mean_sqr_disp(self, power, par_a):
        # Changes the directory
        power_str = str(power)
        A = "{:.2f}".format(par_a)

        msd = "MSD" + power_str + self.sep + A + ".txt"

        MSD = np.loadtxt(msd, delimiter='\n')

        num_lines = sum(1 for line in open(msd))
        limit = 0.005 * num_lines
        step = int(0.6 * num_lines)
        x = np.linspace(0, limit, num=num_lines)

        if par_a >= 0:
            x_sliced = x[step:]
            MSD_sliced = MSD[step:]
            gradient, intercept, r_value, p_value, std_err = stats.linregress(x_sliced, MSD_sliced)

            self.reduced_dif_coef = np.append(self.reduced_dif_coef, gradient)
            self.reduced_dif_err = np.append(self.reduced_dif_err, std_err)
            self.reduced_dif_y_int = np.append(self.reduced_dif_y_int, intercept)

        # Regular coefs are calculated independent of the if loop
        gradient, intercept, r_value, p_value, std_err = stats.linregress(x, MSD)
        self.dif_coef = np.append(self.dif_coef, gradient)
        self.dif_err = np.append(self.dif_err, std_err)
        self.dif_y_int = np.append(self.dif_y_int, intercept)

        print('Diffusion coef: ', gradient, '\n',
              'y-intercept: ', intercept, '\n',
              'R value: ', r_value, '\n',
              'Fit Error: ', std_err)

        name = "n: " + power_str + "  A: " + A
        plt.figure(29)
        plt.plot(x, MSD, label=name)  # , color=color_sequence[p])
        plt.xlabel(r"$t$", fontsize=16)
        plt.ylabel(r"$MSD$", fontsize=16)
        plt.xlim(xmin=0, xmax=x[num_lines - 1])
        plt.ylim(ymin=0, ymax=MSD[num_lines - 1])
        plt.legend(loc="upper left", fancybox=True)
        self.p += 1

    # Pressure C
    def pc(self, power, par_a):
        global p
        # Changes the directory
        power_str = str(power)
        A = "{:.2f}".format(par_a)

        Pc = "Data" + power_str + self.sep + A + ".txt"

        cr = np.loadtxt(Pc, usecols=4, delimiter='\t',
                        comments='#', unpack=True)
        num_lines = 0
        for line in open(Pc):
            if line.startswith('#'):
                continue
            num_lines += 1

        time = num_lines * 0.005
        xxx = np.linspace(0, time, num=num_lines)

        name = "n: " + power_str + "  A: " + A
        plt.figure(5)

        plt.plot(xxx, cr, label=name)  # color=color_sequence[p])
        plt.xlabel(r"Time $t$", size=18)
        plt.ylabel(r"Configurational Pressure $P_C$", size=18)
        # plt.ylim(0,0.1)
        # plt.title("Pressure of Liquid against time", size=17)
        plt.legend(loc="upper right", prop={'size': 12},
                   borderpad=0.2, labelspacing=0.2, handlelength=1)
        self.p += 1

    # Averages
    @staticmethod
    def avg_pressure(power):
        global p
        power_str = str(power)

        PC = "AVGdata" + power_str + ".txt"
        name = "n: " + power_str

        num_lines = sum(1 for line in open(PC))
        a, Pc = np.loadtxt(PC, delimiter='\t', comments='#', usecols=(0, 5), unpack=True)

        plt.figure(6)
        plt.plot(a, Pc, '-o', label=name, markersize=3)
        plt.xlim(xmin=0, xmax=4.0)
        # plt.title("Configurational Pressure for multiple Potentials")
        plt.xlabel(r"$A$", size=16)
        plt.ylabel(r"$P_c$", size=16)
        plt.legend(loc="upper right")

    @staticmethod
    def avg_Kin(power):
        power_str = str(power)

        K = "AVGdata" + power_str + ".txt"
        name = "n: " + power_str

        a, k = np.loadtxt(K, delimiter='\t', comments='#', usecols=(0, 2), unpack=True)

        plt.figure(21)
        plt.plot(a, k, label=name)
        plt.title("Kinetic Energy vs multiple values of A")
        plt.xlabel(r"Parameter A")
        plt.ylabel(r"Kinetic Energy $K$")
        plt.legend(loc="lower right")

    @staticmethod
    def avg_Pot(power):
        power_str = str(power)

        K = "AVGdata" + power_str + ".txt"
        name = "n: " + power_str

        a, k = np.loadtxt(K, delimiter='\t', comments='#', usecols=(0, 3), unpack=True)

        plt.figure(22)
        plt.plot(a, k, label=name)
        plt.title("Potential Energy against parameter A")
        plt.xlabel(r"Parameter A")
        plt.ylabel(r"Potential Energy $U$")
        plt.legend(loc="upper right")

    @staticmethod
    def avg_en(power):
        # Changes the directory
        power_str = str(power)

        E = "AVGdata" + power_str + ".txt"
        name = "n: " + power_str

        num_lines = sum(1 for line in open(E))

        a, K, U, T = np.loadtxt(E, delimiter='\t', comments='#', usecols=(0, 2, 3, 4), unpack=True)

        fig = plt.figure(111)
        Kin = plt.subplot2grid((3, 2), (0, 0), colspan=1)
        Pot = plt.subplot2grid((3, 2), (1, 0), colspan=1)
        TOT = plt.subplot2grid((3, 2), (2, 0), colspan=1)
        All = plt.subplot2grid((3, 2), (0, 1), rowspan=3)

        Kin.plot(a, K, color='r')
        Kin.set_ylim(ymin=2.0), Kin.locator_params(axis='y', nbins=5, prune='lower')
        Pot.plot(a, U, color='g')
        Pot.locator_params(axis='y', nbins=4), Pot.set_ylabel("Energy units")
        TOT.plot(a, T, color='c')
        TOT.locator_params(axis='y', nbins=3), TOT.locator_params(axis='x', nbins=4)
        TOT.set_xlabel(r"Parameter $A$")

        # k, u, t = K[4], U[4], T[4]
        # Kin.text(a[4], k*1.01, 'Average Kinetic Energy', fontsize=12)
        # Pot.text(a[4], u*0.95, 'Average Potential Energy', fontsize=12)
        # TOT.text(a[4], t, 'Average Total Energy', fontsize=12)
        Kin.set_title('Individual Plots for n = %d' % power, fontsize=14)
        All.set_title('Total Energy, Kinetic and Potential')
        All.set_xlabel(r"Parameter $A$")

        fig.subplots_adjust(hspace=0)

        for ax in [Kin, Pot]:
            plt.setp(ax.get_xticklabels(), visible=False)
            # The y-ticks will overlap with "hspace=0", so we'll hide the bottom tick
            ax.set_yticks(ax.get_yticks()[1:])

        All.plot(a, K, 'r', a, U, 'g', a, T, 'c')
        All.set_ylim(ymax=6)
        All.locator_params(axis='x', nbins=4)

    def diffusion_plot(self, power, my_list):
        """
        Plots a graph of the Diffusion coefficients D against a list of parameter A values
        :param power: Potential strength parameter n
        :param my_list: List of parameter A coefficients
        :return: Figure of D vs A for a given number of iterations
        """
        #   List example:
        # my_list = [0, 0.25, 0.50, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 1.00, 1.1, 1.2, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50,
        #            2.75, 4.00]

        for i in my_list:
            self.mean_sqr_disp(power, i)
            print("-----------------------------")

        # File saving Dif coe
        # np.savetxt("../../PlotAnalysis/Diffusion coefficients n=%d.txt"%power,dif_coef, fmt='%.5f')
        # np.savetxt("../../PlotAnalysis/Reduced Diffusion coefficients n=%d.txt"%power,reduced_dif_coef, fmt='%.5f')
        # np.savetxt("../../PlotAnalysis/dif error n=%d.txt"%power, dif_err, fmt='%.5f')
        # np.savetxt("../../PlotAnalysis/reduced dif error n=%d.txt"%power, reduced_dif_err, fmt='%.5f')
        # np.savetxt("../../PlotAnalysis/dif y int n=%d.txt"%power, dif_y_int, fmt='%.5f')
        # np.savetxt("../../PlotAnalysis/reduced dif y hint n=%d.txt"%power, reduced_dif_y_int, fmt='%.5f')
        name = "n: " + str(power)
        steps = ['5k', '10k', '12.5k', '15k', '20k']

        plt.figure(66)
        plt.plot(my_list, self.dif_coef, '--o', label=name)  # color=color_sequence[v])
        plt.xlabel(r"$A$", fontsize=16)
        plt.ylabel(r"$D$", fontsize=16)
        plt.legend(loc="lower right", fancybox=True, ncol=2,
                   labelspacing=0.05, handletextpad=0.5, fontsize=16)

        self.dif_coef, self.dif_err, self.dif_y_int = np.array([]), np.array([]), np.array([])
        self.reduced_dif_coef, self.reduced_dif_err, self.reduced_dif_y_int = np.array([]), np.array([]), np.array([])
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        self.p = 0
        self.j += 15
        self.v += 1

    # No data plots
    def potential(self, power, par_a):
        power_str = str(power)
        A = str(float(par_a))

        x = np.linspace(0.5, 3, 150)  # TODO:  0.5
        V = 1 / pow((x ** 2 + par_a), power / 2)
        plt.figure(6)
        # name = "n: " + power_str + " A: " + A
        # plt.plot(x,V, label=name, linestyle='-', color=color_sequence[p])

        name = "A: " + A
        if par_a <= 1.:
            iso = np.sqrt(1 - par_a)
            sak = 1 / pow((iso ** 2 + par_a), power / 2)

            # plt.scatter(iso, sak, marker='o', color='magenta', label= 'Isosbestic point')
        plt.plot(x, V, label=name, linestyle=self.line_style[self.line_it], color='black')
        plt.xlim(xmin=0.5, xmax=2)
        plt.ylim(ymin=0)

        plt.xlabel(r"$r$", size=16)
        plt.ylabel(r"$\Phi$", size=16)
        lgnd = plt.legend(loc="upper right", fancybox=True, ncol=1)
        f, v = [], []
        temp = np.sqrt(par_a / (1. + power))
        f.append(temp)
        temp = 1 / pow((temp ** 2 + par_a), power / 2.)
        v.append(temp)
        plt.scatter(f, v, color='red', marker='o', s=13, label='Inflection point')
        plt.locator_params(axis='x', nbins=5)
        self.p += 1
        self.line_it += 1

    def force(self, power, par_a):
        power_str = str(power)
        A = str(float(par_a))

        x = np.linspace(0.0, 3, 300)  # division with 0
        V = power * x * (pow((x ** 2 + par_a), (-power / 2 - 1)))
        plt.figure(7)
        name = " A: " + A
        plt.plot(x, V, label=name, linestyle=self.line_style[self.line_it], color='black')
        plt.xlabel(r"$r$", size=16)
        plt.ylabel(r"$f$", size=16)
        plt.legend(loc="upper right", fancybox=True)  # fontsize=16
        f, v = [], []
        temp = np.sqrt(par_a / (1. + power))
        f.append(temp)
        temp = power * temp * (pow((temp ** 2 + par_a), (-power / 2 - 1)))
        v.append(temp)
        plt.scatter(f, v, color='red', marker='o', s=13, label='Inflection point')
        plt.xlim(0, 2)
        plt.ylim(ymin=0)

        self.p += 1
        self.line_it += 1

    def RDF2(self, power, par_a):
        power_str = str(power)
        A = str(float(par_a))
        name = "n: " + power_str + " A: " + A

        x = np.linspace(0, 3, 100)
        G = np.exp(-1. / ((x ** 2 + par_a) ** (power / 2.0)) / 1.4)
        plt.figure(79)
        plt.plot(x, G, label=name, color=self.color_sequence2[self.c])
        plt.xlim(xmin=0, xmax=2.5)
        plt.ylim(ymin=0)
        plt.legend(loc='upper right', fancybox=True)

        self.c += 1

    def vel_dist(self, power, par_a):
        """
        Profiling of the velocity distribution of the fluid, compared to a
        Maxwell Boltzmann distribution, with parameters extracted from the data.
        :param power: Potential strength n.
        :param par_a: Smothening parameter A.
        :return: Figure comparing an M&B distribution with data obtained from the simulation.
        """
        power_str = str(power)
        A = "{:.2f}".format(par_a)
        data = "Positions_Velocities" + power_str + self.sep + A + ".txt"
        name = "n: " + power_str + " A: " + A
        vx, vy, vz = np.loadtxt(data,
                                usecols=(3, 4, 5),
                                delimiter='\t',
                                comments='#',
                                unpack=True)
        v = np.sqrt(np.square(vx) + np.square(vy) + np.square(vz))

        # kb = 1.38064852 * 10**-23  # Boltzman constant
        # T = 1.4  # Temperature
        # m = 1  # mass
        # norm = np.power((m/(2.*np.pi*kb*T)), 3./2.)   # normalised in C++ simulation
        # v = np.multiply(v, 1./norm)

        n, bins, patches = plt.hist(v, 100, normed=1, label=name)
        xmin, xmax = 0, max(v) + 1
        lnspc = np.linspace(xmin, xmax, len(v))
        # m, var, skew, kurt = stats.maxwell.stats(moments='mvsk')
        mean, std = stats.maxwell.fit(v, loc=0, scale=1)
        pdf_mb = stats.maxwell.pdf(lnspc, mean, std)
        plt.plot(lnspc, pdf_mb, label='Theory')

        plt.xlim(xmin=0)
        plt.title(power_str + '~' + A)
        plt.legend(loc='upper right', fancybox=True)

