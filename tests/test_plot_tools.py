"""
Tests of functions relative to plot tool GUI
"""
import re
from examples.ex_plot_tools import ex_load_data, ex_update_entries, ex_plot_figure


def test_update_entries():
    """ Test the GUi behavior """
    ex_update_entries()


def test_plot_figure():
    """ Test the plot behavior """
    ex_plot_figure()


def test_quantification():
    """ Test the importation of the data and the multiplication with RSF """
    test_app = ex_load_data()
    assert len(test_app.display_tab.QUANTI) == 3
    assert test_app.display_tab.QUANTI[1] == {'P2p 3/2': 0.015463917525773196,
                                              'P2p 1/2': 0.007731958762886598,
                                              'P2p 3/2 Ox': 0.0,
                                              'P2p 1/2 Ox': 0.0,
                                              'Plasmon': 1.09,
                                              'Si2p 3/2': 0.12571957917025078,
                                              'Si2p 1/2': 0.06285978958512539,
                                              'Si2p 3/2 Ox': 0.0072785019519618875,
                                              'Si2p 1/2 Ox': 0.0033084099781644943,
                                              'Si2p 1+ 3/2': 0.03573082776417654,
                                              'Si2p 1+ 1/2': 0.01786541388208827,
                                              'Si2p 2+ 3/2': 0.0,
                                              'Si2p 2+ 1/2': 0.0,
                                              'Si2p 3+ 1/2': 0.003970091973797393,
                                              'Si2p 3+ 3/2': 0.0019850459868986964,
                                              'Si1s Ox': 0.0,
                                              'Si1s': 0.18847204346068216,
                                              'Si1s 1+': 0.0036723358351121206,
                                              'Si1s 2+': 0.005367260066702331,
                                              'Si1s 3+': 0.0,
                                              'P1s': 0.02009010105929624,
                                              'O1s': 0.010212711634512582}

    assert test_app.display_tab.QUANTI[0] == {'P2p 3/2': 0.009793814432989692,
                                              'P2p 1/2': 0.005154639175257733,
                                              'P2p 3/2 Ox': 0.0015463917525773197,
                                              'P2p 1/2 Ox': 0.0005154639175257732,
                                              'Plasmon': 1.19,
                                              'Si2p 3/2': 0.09991398134056773,
                                              'Si2p 1/2': 0.049626149672467416,
                                              'Si2p 3/2 Ox': 0.02977568980348045,
                                              'Si2p 1/2 Ox': 0.015218685899556675,
                                              'Si2p 1+ 3/2': 0.013233639912657977,
                                              'Si2p 1+ 1/2': 0.006616819956328989,
                                              'Si2p 2+ 3/2': 0.0013233639912657977,
                                              'Si2p 2+ 1/2': 0.0006616819956328988,
                                              'Si2p 3+ 1/2': 0.0013233639912657977,
                                              'Si2p 3+ 3/2': 0.0006616819956328988,
                                              'Si1s Ox': 0.04050162695070772,
                                              'Si1s': 0.10918136925160267,
                                              'Si1s 1+': 0.004872907165821852,
                                              'Si1s 2+': 0.002030377985759105,
                                              'Si1s 3+': 0.002171621671724956,
                                              'P1s': 0.013657210114046837,
                                              'O1s': 0.09366971452279509}

    assert test_app.display_tab.QUANTI[2] == {'P2p 3/2': 0.002061855670103093,
                                              'P2p 1/2': 0.0010309278350515464,
                                              'P2p 3/2 Ox': 0.0,
                                              'P2p 1/2 Ox': 0.0,
                                              'Plasmon': 0.89,
                                              'Si2p 3/2': 0.13101303513531398,
                                              'Si2p 1/2': 0.06550651756765699,
                                              'Si2p 3/2 Ox': 0.006616819956328989,
                                              'Si2p 1/2 Ox': 0.0033084099781644943,
                                              'Si2p 1+ 3/2': 0.01654204989082247,
                                              'Si2p 1+ 1/2': 0.008601865943227685,
                                              'Si2p 2+ 3/2': 0.0006616819956328988,
                                              'Si2p 2+ 1/2': 0.0,
                                              'Si2p 3+ 1/2': 0.003970091973797393,
                                              'Si2p 3+ 3/2': 0.0019850459868986964,
                                              'Si1s Ox': 0.0,
                                              'Si1s': 0.17641336377134764,
                                              'Si1s 1+': 0.005031806312533435,
                                              'Si1s 2+': 0.003089705630502986,
                                              'Si1s 3+': 0.0,
                                              'P1s': 0.003064247737327002,
                                              'O1s': 0.004787208578677773}

    test_app.destroy()


def test_interpeter():
    """ Test the result of the function Entry """

    # Create the app
    test_app = ex_load_data()

    # Set the test function
    test_app.display_tab.function_var.set('([1] + [3:4])/[]')

    # Select the good mode
    test_app.display_tab.calc_type.set(2)

    # Select the 3 samples
    for i in range(3):
        test_app.display_tab.sample_LIST.select_set(i)

    # Update the orbitals
    test_app.display_tab.update_entries()

    # Split the function around each parameter
    spliter = re.findall(r'\[[^\]]*\]|[^[]+', test_app.display_tab.function_var.get()
                         .replace('exp', 'np.exp')
                         .replace('log', 'np.log'))

    # Compute the calculation
    results = [test_app.display_tab.interpreter(spliter, i) for i in
               test_app.display_tab.sample_LIST.curselection()]
    assert results == [0.060634779313027444, 0.08106982691133109, 0.10247517091635]

    test_app.destroy()
