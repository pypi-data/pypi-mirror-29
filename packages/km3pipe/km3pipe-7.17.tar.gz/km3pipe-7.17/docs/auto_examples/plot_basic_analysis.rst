

.. _sphx_glr_auto_examples_plot_basic_analysis.py:


======================
Basic Analysis Example
======================




.. code-block:: python

    # Authors: Tamás Gál <tgal@km3net.de>, Moritz Lotze <mlotze@km3net.de>
    # License: BSD-3
    # Date: 2017-10-10
    # Status: Under construction...







Preparation
-----------
The very first thing we do is importing our libraries and setting up
the Jupyter Notebook environment.



.. code-block:: python


    import matplotlib.pyplot as plt   # our plotting module
    import pandas as pd               # the main HDF5 reader
    import numpy as np                # must have
    import km3pipe as kp              # some KM3NeT related helper functions
    import seaborn as sns              # beautiful statistical plots!








this is just to make our plots a bit "nicer", you can skip it



.. code-block:: python

    import km3pipe.style
    km3pipe.style.use("km3pipe")






.. rst-class:: sphx-glr-script-out

 Out::

    Loading style definitions from '/Users/tamasgal/Dev/km3pipe/km3pipe/kp-data/stylelib/km3pipe.mplstyle'


Accessing the Data File(s)
--------------------------
In the following, we will work with one random simulation file with
reconstruction information from JGandalf which has been converted
from ROOT to HDF5 using the ``tohdf5`` command line tool provided by
``KM3Pipe``.

You can find the documentation here:
http://km3pipe.readthedocs.io/en/latest/cmd.html#tohdf


Note for Lyon Users
~~~~~~~~~~~~~~~~~~~
If you are working on the Lyon cluster, you can activate the latest KM3Pipe
with the following command (put it in your ``~/.bashrc`` to load it
automatically in each shell session)::

    source $KM3NET_THRONG_DIR/src/python/pyenv.sh


Converting from ROOT to HDF5 (if needed)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose a file (take e.g. one from /in2p3/km3net/mc/...),
load the appropriate Jpp/Aanet version and convert it via::

    tohdf5 --aa-format=the_file.root --ignore-hits --skip-header

Note that you may have to ``--skip-header`` otherwise you might
encounter some segfaults. There is currently a big mess of different
versions of libraries in several levels of the MC file processings.

The ``--ignore-hits`` will skip the hit information, so the converted file
is much smaller (normally around 2-3 MBytes). Skip this option if you want
to read the hit information too. The file will still be smaller than the
ROOT file (about 1/3).

Luckily, a handful people are preparing the HDF5 conversion, so in future
you can download them directly, without thinking about which Jpp or Aanet
version you need to open them.


First Look at the Data
----------------------



.. code-block:: python


    filepath = "data/basic_analysis_sample.h5"








We can have a quick look at the file with the ``ptdump`` command
in the terminal::

    ptdump filename.h5

For further information, check out the documentation of the KM3NeT HDF5
format definition: http://km3pipe.readthedocs.io/en/latest/hdf5.html



The ``/event_info`` table contains general information about each event.
The data is a simple 2D table and each event is represented by a single row.

Let's have a look at the first few rows:



.. code-block:: python

    event_info = pd.read_hdf(filepath, '/event_info')
    print(event_info.head(5))






.. rst-class:: sphx-glr-script-out

 Out::

    det_id  frame_index  livetime_sec  mc_id          mc_t  n_events_gen  \
    0      -1            5             0      4  4.499995e+08      91000000   
    1      -1            8             0      7  7.499997e+08      91000000   
    2      -1           13             0     12  1.249999e+09      91000000   
    3      -1           15             0     14  1.449999e+09      91000000   
    4      -1           18             0     17  1.750000e+09      91000000   

       n_files_gen  overlays  trigger_counter  trigger_mask  utc_nanoseconds  \
    0            0         0                3             6        400000000   
    1            0         0                6            22        700000000   
    2            0         0               11             4        200000000   
    3            0         0               13            22        400000000   
    4            0         0               16            22        700000000   

       utc_seconds  weight_w1     weight_w2  weight_w3  run_id  event_id  
    0            0  2080000.0  1.396000e+09    0.07448       1         0  
    1            0  2080000.0  8.907000e+09    0.13710       1         1  
    2            1  2080000.0  5.709000e+09    0.11890       1         2  
    3            1  2080000.0  8.747000e+10    0.29150       1         3  
    4            1  2080000.0  3.571000e+09    0.10220       1         4


Next, we will read out the MC tracks which are stored under ``/mc_tracks``.



.. code-block:: python


    tracks = pd.read_hdf(filepath, '/mc_tracks')







also read event info, for things like weights



.. code-block:: python


    info = pd.read_hdf(filepath, '/event_info')







It has a similar structure, but now you can have multiple rows which belong
to an event. The ``event_id`` column holds the ID of the corresponding event.



.. code-block:: python


    print(tracks.head(10))





.. rst-class:: sphx-glr-script-out

 Out::

    bjorkeny     dir_x     dir_y     dir_z   energy  id  interaction_channel  \
    0  0.057346 -0.616448 -0.781017 -0.100017  4.36550   1                    4   
    1  0.000000  0.488756 -0.535017 -0.689111  0.00618   1                    0   
    2  0.000000 -0.656758 -0.746625 -0.105925  4.12810   2                    0   
    3  0.000000  0.412029 -0.878991 -0.240015  0.96394   3                    0   
    4  0.000000 -0.664951 -0.468928  0.581332  0.21791   4                    0   
    5  0.437484  0.113983  0.914457  0.388298  8.09620   1                    3   
    6  0.000000 -0.345462  0.923065 -0.169138  0.00632   1                    0   
    7  0.000000  0.381285  0.828365  0.410406  4.41940   2                    0   
    8  0.000000 -0.191181  0.907296  0.374518  3.22370   3                    0   
    9  0.000000 -0.244006  0.922082  0.300377  0.90994   4                    0   

       is_cc  length   pos_x    pos_y   pos_z  time  type  event_id  
    0      1     0.0  46.929   67.589 -71.802     0   -14         0  
    1      1     0.0  46.929   67.589 -71.802     0    22         0  
    2      1     0.0  46.929   67.589 -71.802     0   -13         0  
    3      1     0.0  46.929   67.589 -71.802     0  2112         0  
    4      1     0.0  46.929   67.589 -71.802     0  -211         0  
    5      1     0.0 -17.837 -109.844  30.360     0   -14         1  
    6      1     0.0 -17.837 -109.844  30.360     0    22         1  
    7      1     0.0 -17.837 -109.844  30.360     0   -13         1  
    8      1     0.0 -17.837 -109.844  30.360     0  3122         1  
    9      1     0.0 -17.837 -109.844  30.360     0   321         1


We now are accessing the first track for each event by grouping via
``event_id`` and calling the ``first()`` method of the
``Pandas.DataFrame`` object.



.. code-block:: python


    primaries = tracks.groupby('event_id').first()







Here are the first 5 primaries:



.. code-block:: python

    print(primaries.head(5))





.. rst-class:: sphx-glr-script-out

 Out::

    bjorkeny     dir_x     dir_y     dir_z   energy  id  \
    event_id                                                        
    0         0.057346 -0.616448 -0.781017 -0.100017   4.3655   1   
    1         0.437484  0.113983  0.914457  0.388298   8.0962   1   
    2         0.549859 -0.186416 -0.385939 -0.903493   6.9806   1   
    3         0.056390 -0.371672  0.550002 -0.747902  17.3370   1   
    4         0.049141 -0.124809 -0.979083  0.160683   5.9697   1   

              interaction_channel  is_cc  length   pos_x    pos_y   pos_z  time  \
    event_id                                                                      
    0                           4      1     0.0  46.929   67.589 -71.802     0   
    1                           3      1     0.0 -17.837 -109.844  30.360     0   
    2                           3      1     0.0 -70.733  101.459 -30.985     0   
    3                           4      1     0.0  86.852   15.056  24.474     0   
    4                           1      1     0.0  46.822   88.981 -65.848     0   

              type  
    event_id        
    0          -14  
    1          -14  
    2           14  
    3          -14  
    4           14


Creating some Fancy Graphs
--------------------------



.. code-block:: python

    primaries.energy.hist(bins=100, log=True)
    plt.xlabel('energy [GeV]')
    plt.ylabel('number of events')
    plt.title('Energy Distribution')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_001.png
    :align: center





.. code-block:: python

    primaries.bjorkeny.hist(bins=100)
    plt.xlabel('bjorken-y')
    plt.ylabel('number of events')
    plt.title('bjorken-y Distribution')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_002.png
    :align: center





.. code-block:: python

    zeniths = kp.math.zenith(primaries.filter(regex='^dir_.?$'))
    primaries['zenith'] = zeniths

    plt.hist(np.cos(primaries.zenith), bins=21, histtype='step', linewidth=2)
    plt.xlabel(r'cos($\theta$)')
    plt.ylabel('number of events')
    plt.title('Zenith Distribution')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_003.png
    :align: center




Starting positions of primaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

    plt.hist2d(primaries.pos_x, primaries.pos_y, bins=100, cmap='viridis')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('2D Plane')
    plt.colorbar()




.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_004.png
    :align: center




If you have seaborn installed (`pip install seaborn`), you can easily create
nice jointplots:



.. code-block:: python

    try:
        import seaborn as sns  # noqa
        km3pipe.style.use("km3pipe")  # reset matplotlib style
    except:
        print("No seaborn found, skipping example.")
    else:
        g = sns.jointplot('pos_x', 'pos_y', data=primaries, kind='hex')
        g.set_axis_labels("x [m]", "y[m]")
        plt.subplots_adjust(right=0.90)  # make room for the colorbar
        plt.title("2D Plane")
        plt.colorbar()
        plt.legend()





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_005.png
    :align: center


.. rst-class:: sphx-glr-script-out

 Out::

    Loading style definitions from '/Users/tamasgal/Dev/km3pipe/km3pipe/kp-data/stylelib/km3pipe.mplstyle'



.. code-block:: python

    from mpl_toolkits.mplot3d import Axes3D  # noqa
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(primaries.pos_x, primaries.pos_y, primaries.pos_z, s=3)
    ax.set_xlabel('x [m]', labelpad=10)
    ax.set_ylabel('y [m]', labelpad=10)
    ax.set_zlabel('z [m]', labelpad=10)
    ax.set_title('3D Plane')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_006.png
    :align: center





.. code-block:: python

    gandalfs = pd.read_hdf(filepath, '/reco/gandalf')
    print(gandalfs.head(5))






.. rst-class:: sphx-glr-script-out

 Out::

    beta0     beta1        chi2     dir_x     dir_y     dir_z  jenergy_chi2  \
    0  0.016788  0.011857  -53.119816 -0.877972  0.090814 -0.470018           0.0   
    1  0.007835  0.005533  -32.504874  0.470130  0.786167  0.401147           0.0   
    2  0.012057  0.008456  -81.195134 -0.151203 -0.769743 -0.620189           0.0   
    3  0.007858  0.005554 -200.985734 -0.306306  0.545569 -0.780084           0.0   
    4  0.011166  0.007366  -89.451264 -0.064503 -0.991324 -0.114522           0.0   

       jenergy_energy  jstart_length  jstart_npe_mip    ...     spread_pos_y_std  \
    0             0.0      11.572860        0.000000    ...            39.561800   
    1             0.0      63.148708      165.114696    ...            53.155262   
    2             0.0      23.115671       62.299430    ...            35.788155   
    3             0.0      55.163229       92.317612    ...            41.744175   
    4             0.0     154.211642       77.005050    ...            34.385820   

       spread_pos_z_iqr  spread_pos_z_mad  spread_pos_z_mean  spread_pos_z_median  \
    0         28.138729         11.364669          64.424904            56.583540   
    1         17.349153          5.857349         134.337736           145.034447   
    2          7.366047          2.861858          95.861157            88.861050   
    3         21.986652         11.204107         138.173388           133.728837   
    4          7.724371          3.995879          58.962182            52.932722   

       spread_pos_z_std          time  type  upgoing_vs_downgoing  event_id  
    0         27.679435  4.999955e+07   0.0             -0.274836         0  
    1         30.821526  4.999950e+07   0.0              3.907941         1  
    2         23.508735  4.999935e+07   0.0             -0.385038         2  
    3         31.781891  4.999947e+07   0.0             -0.809872         3  
    4         21.573971  4.999956e+07   0.0             -0.167897         4  

    [5 rows x 83 columns]



.. code-block:: python

    gandalfs.columns









.. code-block:: python

    plt.hist(gandalfs['lambda'], bins=50, log=True)
    plt.xlabel('lambda parameter')
    plt.ylabel('count')
    plt.title('Lambda Distribution of Reconstructed Events')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_007.png
    :align: center





.. code-block:: python

    gandalfs['zenith'] = kp.math.zenith(gandalfs.filter(regex='^dir_.?$'))

    plt.hist((gandalfs.zenith - primaries.zenith).dropna(), bins=100)
    plt.xlabel(r'true zenith - reconstructed zenith [rad]')
    plt.ylabel('count')
    plt.title('Zenith Reconstruction Difference')





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_008.png
    :align: center





.. code-block:: python

    l = 0.2
    lambda_cut = gandalfs['lambda'] < l
    plt.hist((gandalfs.zenith - primaries.zenith)[lambda_cut].dropna(), bins=100)
    plt.xlabel(r'true zenith - reconstructed zenith [rad]')
    plt.ylabel('count')
    plt.title('Zenith Reconstruction Difference for lambda < {}'.format(l))





.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_009.png
    :align: center




Combined zenith reco plot for different lambda cuts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python


    fig, ax = plt.subplots()
    for l in [100, 5, 2, 1, 0.1]:
        l_cut = gandalfs['lambda'] < l
        ax.hist((primaries.zenith - gandalfs.zenith)[l_cut].dropna(),
                bins=100, label=r"$\lambda$ = {}".format(l), alpha=.7)
    plt.xlabel(r'true zenith - reconstructed zenith [rad]')
    plt.ylabel('count')
    plt.legend()
    plt.title('Zenith Reconstruction Difference for some Lambda Cuts')




.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_010.png
    :align: center




Fitting Angular resolutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's fit some distributions: gaussian + lorentz (aka norm + cauchy)

Fitting the gaussian to the whole range is a very bad fit, so
we make a second gaussian fit only to +- 10 degree.
Conversely, the Cauchy (lorentz) distribution is a near perfect fit
(note that ``2 gamma = FWHM``).



.. code-block:: python


    from scipy.stats import cauchy, norm  # noqa

    residuals = gandalfs.zenith - primaries.zenith
    cut = (gandalfs['lambda'] < l) & (np.abs(residuals) < 2 * np.pi)
    residuals = residuals[cut]
    info[cut]

    # convert rad -> deg
    residuals = residuals * 180 / np.pi

    pi = 180
    # x axis for plotting
    x = np.linspace(-pi, pi, 1000)

    c_loc, c_gamma = cauchy.fit(residuals)
    fwhm = 2 * c_gamma

    g_mu_bad, g_sigma_bad = norm.fit(residuals)
    g_mu, g_sigma = norm.fit(residuals[np.abs(residuals) < 10])

    plt.hist(residuals, bins='auto', label='Histogram', normed=True,
             alpha=.7)
    plt.plot(x, cauchy(c_loc, c_gamma).pdf(x),
             label='Lorentz: FWHM $=${:.3f}'.format(fwhm),
             linewidth=2)
    plt.plot(x, norm(g_mu_bad, g_sigma_bad).pdf(x),
             label='Unrestricted Gauss: $\sigma =$ {:.3f}'.format(g_sigma_bad),
             linewidth=2)
    plt.plot(x, norm(g_mu, g_sigma).pdf(x),
             label='+- 10 deg Gauss: $\sigma =$ {:.3f}'.format(g_sigma),
             linewidth=2)
    plt.xlim(-pi / 4, pi / 4)
    plt.xlabel('Zenith residuals / deg')
    plt.legend()




.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_011.png
    :align: center




We can also look at the median resolution without doing any fits.

In textbooks, this metric is also called Median Absolute Deviation.



.. code-block:: python


    resid_median = np.median(residuals)
    residuals_shifted_by_median = residuals - resid_median
    absolute_deviation = np.abs(residuals_shifted_by_median)
    resid_mad = np.median(absolute_deviation)

    plt.hist(np.abs(residuals), alpha=.7, bins='auto', label='Absolute residuals')
    plt.axvline(resid_mad, label='MAD: {:.2f}'.format(resid_mad), linewidth=3)
    plt.title("Average resolution: {:.3f} degree".format(resid_mad))
    plt.legend()
    plt.xlabel('Absolute zenith residuals / deg')



.. image:: /auto_examples/images/sphx_glr_plot_basic_analysis_012.png
    :align: center




**Total running time of the script:** ( 0 minutes  3.060 seconds)



.. container:: sphx-glr-footer


  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_basic_analysis.py <plot_basic_analysis.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_basic_analysis.ipynb <plot_basic_analysis.ipynb>`

.. rst-class:: sphx-glr-signature

    `Generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
