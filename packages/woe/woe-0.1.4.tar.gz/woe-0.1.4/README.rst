woe
===

.. image:: https://travis-ci.org/justdoit0823/pywxclient.svg?branch=master
    :target: https://travis-ci.org/justdoit0823/pywxclient

version: 0.1.4

Tools for WoE Transformation mostly used in ScoreCard Model for credit rating

Installation
--------------------------------

We can simply use pip to install, as the following:

.. code-block:: bash

   $ pip install woe

or installing from git

.. code-block:: bash

   $ pip install git+https://github.com/boredbird/woe


Features
========

  * Split tree with IV criterion

  * Rich and plentiful model eval methods

  * Unified format and easy for output

  * Storage of IV tree for follow-up use



**woe** module function tree
============================

:: 

	|- __init__
	|- config.py 
	|   |-- config
	|   	|-- __init__
	|		|-- change_config_var_dtype()
	|		|-- load_file()
	|- eval.py 
	|   |-- compute_ks()
	|   |-- eval_data_summary()
	|   |-- eval_feature_detail()
	|   |-- eval_feature_stability()
	|   |-- eval_feature_summary()
	|   |-- eval_model_stability()
	|   |-- eval_model_summary()
	|   |-- eval_segment_metrics()
	|   |-- plot_ks()
	|   |-- proc_cor_eval()
	|   |-- proc_validation()
	|   |-- wald_test()
	|- feature_process.py 
	|   |-- binning_data_split()
	|   |-- calculate_iv_split()
	|   |-- calulate_iv()
	|   |-- change_feature_dtype()
	|   |-- check_point()
	|   |-- fillna()
	|   |-- format_iv_split()
	|   |-- proc_woe_continuous()
	|   |-- proc_woe_discrete()
	|   |-- process_train_woe()
	|   |-- process_woe_trans()
	|   |-- search()
	|   |-- woe_trans()
	|- ftrl.py 
	|   |-- FTRL()
	|   |-- LR()
	|- GridSearch.py 
	|   |-- fit_single_lr()
	|   |-- grid_search_lr_c()
	|   |-- grid_search_lr_c_main()
	|   |-- grid_search_lr_validation()


Examples
========

In the examples directory, there is a simple woe transformation program as tutorials.

Or you can write a more complex program with this `woe` package.

Version Records
================
woe 0.1.4 2018-03-01
	* support py3

woe 0.1.3 2018-02-09

	* woe.feature_process.proc_woe_discrete(): fix bug when deal with discrete varibales
	* woe.eval.eval_feature_detail(): fix bug : utf-8 output file format
	* woe.GridSearch.grid_search_lr_c_main(): add function warper for convenience and high efficiency
	* woe.GridSearch.grid_search_lr_c_validation(): monitor the ks performance of training sets and test sets on different 'c'
	* supplement examples test scripts


woe 0.1.2 2017-12-05

	* woe.ftrl.FTRL(): add online learning module

woe 0.1.1 2017-11-28

	* woe.config.load_file(): change param data_path to be optional
	* woe.eval.eval_feature_stability(): fix bug : psi_dict['stability_index'] computation error
	* woe.feature_process.change_feature_dtype(): add friendly tips when encounter a error
	* woe.feature_process.calulate_iv(): refactor the code
	* woe.feature_process.calculate_iv_split(): refactor the code
	* woe.feature_process.binning_data_split(): reduce the number of len() function calls with __len__() and shape attributes;replace namedtuple with dict
	* woe.feature_process.fillna(): new added function to fill null value
	* woe.GridSearch.grid_search_lr_c(): list of regularization parameter c specified inside the function is changed to the user specified
	
woe 0.0.9 2017-11-21

	* Add module : GridSearch for the search of optimal hyper parametric C in LogisticRegression
	* Code refactoring: function compute_ks and plot_ks

woe 0.0.8 2017-09-28

	* More flexible: cancel conditional restriction in function feature_process.change_feature_dtype() 
	* Fix bug: the wrong use of deepcopy in function feature_process.woe_trans()
	
woe 0.0.7 2017-09-19

	* Fix bug: eval.eval_feature_detail raises ValueError('arrays must all be same length')
	* Add parameter interface: alpha specified step learning rate ,default 0.01

How to Contribute
--------------------------------

Email me,1002937942@qq.com.
