Example
=======

Given an excel file with rows similar to the below

+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| variab | sce | module          | distr | param  | par | par | un | star | end  | CA | ref  | labe | com | sou |
| le     | nar |                 | ibuti | 1      | am  | am  | it | t    | date | GR | date | l    | men | rce |
|        | io  |                 | on    |        | 2   | 3   |    | date |      |    |      |      | t   |     |
+========+=====+=================+=======+========+=====+=====+====+======+======+====+======+======+=====+=====+
| a      |     | numpy.random    | choic | 1      |     |     | kg | 01/0 | 01/0 | 0. | 01/0 | test |     |     |
|        |     |                 | e     |        |     |     |    | 1/20 | 4/20 | 10 | 1/20 | var  |     |     |
|        |     |                 |       |        |     |     |    | 09   | 09   |    | 09   | 1    |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| b      |     | numpy.random    | unifo | 2      | 4   |     | -  |      |      |    |      | labe |     |     |
|        |     |                 | rm    |        |     |     |    |      |      |    |      | l    |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| c      |     | numpy.random    | trian | 3      | 6   | 10  | -  |      |      |    |      | labe |     |     |
|        |     |                 | gular |        |     |     |    |      |      |    |      | l    |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| d      |     | bottom\_up\_com | Distr | core\_ |     |     | J/ |      |      |    |      | labe |     |     |
|        |     | parision.sampli | ibuti | router |     |     | Gb |      |      |    |      | l    |     |     |
|        |     | ng\_core\_route | on    | s.csv  |     |     |    |      |      |    |      |      |     |     |
|        |     | rs              |       |        |     |     |    |      |      |    |      |      |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| a      | s1  | numpy.random    | choic | 2      |     |     |    |      |      |    |      | test |     |     |
|        |     |                 | e     |        |     |     |    |      |      |    |      | var  |     |     |
|        |     |                 |       |        |     |     |    |      |      |    |      | 1    |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+
| multip |     | numpy.random    | choic | 1,2,3  |     |     | kg | 01/0 | 01/0 |    |      | test |     |     |
| le     |     |                 | e     |        |     |     |    | 1/20 | 1/20 |    |      | var  |     |     |
| choice |     |                 |       |        |     |     |    | 07   | 09   |    |      | 1    |     |     |
+--------+-----+-----------------+-------+--------+-----+-----+----+------+------+----+------+------+-----+-----+

You can run python/ numpy code that references these variables and
generates random distributions.

For example, the following will initialise a variable ``c`` with a
vector of size 2 with random values from a triangular distribution.

::

        np.random.seed(123)

        data = ParameterLoader.from_excel('test.xlsx', size=2, sheet_index=0)
        c = data['c']
    >>> [ 7.08471918  5.45131111]

Other types of distributions include ``choice`` and ``normal``. However
you can specify any distribution from numpy that takes up to three
parameters to init.

You can also specify a .csv file with samples and an empiricial
distribution function is generated and variable values will be sampled
from that.

Scenarios
---------

It is possible to define scenarios and have paramter values for a
variable change with each scenario.

::

        data = ParameterLoader.from_excel('test.xlsx', size=1, sheet_index=0)
        res = data['a'][0]

        assert res == 1.

        data.select_scenario('s1')
        res = data['a'][0]

        assert res == 2.

use ``data.unselect_scenario()`` to return to the default value.

Pandas Dataframes
-----------------

It is possible to define a time frame for distributions and have sample
values change over time.

::

        # the time axis of our dataset
        times = pd.date_range('2009-01-01', '2009-04-01', freq='MS')
        # the sample axis our dataset
        samples = 2

        dfl = DataSeriesLoader.from_excel('test.xlsx', times, size=samples, sheet_index=0)
        res = dfl['a']

        assert res.loc[[datetime(2009, 1, 1)]][0] == 1
        assert np.abs(res.loc[[datetime(2009, 4, 1)]][0] - pow(1.1, 3. / 12)) < 0.00001

Reload
------

Reloading data sources is useful when underlying excel files change.

::

            times = pd.date_range('2009-01-01', '2009-04-01', freq='MS')        
            samples = 2

            data = MultiSourceLoader()
            data.add_source(ExcelSeriesLoaderDataSource('test.xlsx', times, size=samples, sheet_index=0))

            res = data['a'][0]
            assert res == 1.

            wb = load_workbook(filename='test.xlsx')
            ws = wb.worksheets[0]
            ws['E2'] = 4.
            wb.save(filename='test.xlsx')

            data.reload_sources()

            res = data['a'][0]
            assert res == 4.

            wb = load_workbook(filename='test.xlsx')
            ws = wb.worksheets[0]
            ws['E2'] = 1.
            wb.save(filename='test.xlsx')

            data.reload_sources()

            data.set_scenario('s1')
            res = data['a'][0]

            assert res == 2.

            data.reset_scenario()
            res = data['a'][0]

            assert res == 1.

Metadata
--------

The contents of the rows is also contained in the metadata

::

        # the time axis of our dataset
        times = pd.date_range('2009-01-01', '2009-04-01', freq='MS')
        # the sample axis our dataset
        samples = 3

        dfl = DataSeriesLoader.from_excel('test.xlsx', times, size=samples, sheet_index=0)
        res = dfl['a']

        print(res._metadata)


15.5.2015   0.1.1   Renamed class to ParameterLoader
22.5.2015   0.1.2   Add sheet index as parameter to loader
11.1.2016   0.2.2   Added support to generate pandas dataframes, update to python 3
18.4.2016   0.2.7   Added new flag 'single_var' to freeze all variables except one to their mean value - use in sensitivity analysis.
19.8.2016   0.3.0   Upgrade to xarray 0.8.1
20.8.2016   0.3.1   Single var mean now analytical for choice, uniform, triangular and normal; trim white space from var names
4.07.2017   0.4.0   Rewrite with new API
4.07.2017   0.4.1   Added XLWings interface to read from Excel
14.09.2017   0.5.0   Delay sampling from data source until __call__ on Parameter.
16.2.2018   0.5.1   Fixed error in generation of random distributions with zero param values


