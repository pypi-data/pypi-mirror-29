event based hazard
==================

============== ===================
checksum32     2,235,846,578      
date           2018-02-19T09:58:56
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 1

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         100               
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                0.1               
area_source_discretization      10.0              
ground_motion_correlation_model 'JB2009'          
random_seed                     24                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
exposure                `exposure_model.xml <exposure_model.xml>`_                  
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job_h.ini <job_h.ini>`_                                    
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ====== =============== ================
smlt_path weight gsim_logic_tree num_realizations
========= ====== =============== ================
b1        1.000  trivial(1)      1/1             
========= ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== =================== ========= ========== ==========
grp_id gsims               distances siteparams ruptparams
====== =================== ========= ========== ==========
0      BooreAtkinson2008() rjb       vs30       mag rake  
====== =================== ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,BooreAtkinson2008(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 482          482         
================ ====== ==================== ============ ============

Informational data
------------------
========================= ==================================================================================
compute_ruptures.received tot 20.06 KB, max_per_task 4.36 KB                                                
compute_ruptures.sent     sources 18.89 KB, src_filter 9.87 KB, param 7.7 KB, monitor 4.36 KB, gsims 1.79 KB
hazard.input_weight       482.0                                                                             
hazard.n_imts             1                                                                                 
hazard.n_levels           1                                                                                 
hazard.n_realizations     1                                                                                 
hazard.n_sites            1                                                                                 
hazard.n_sources          1                                                                                 
hazard.output_weight      1.0                                                                               
hostname                  tstation.gem.lan                                                                  
require_epsilons          False                                                                             
========================= ==================================================================================

Exposure model
--------------
=============== ========
#assets         1       
#taxonomies     1       
deductibile     relative
insurance_limit relative
=============== ========

======== ===== ====== === === ========= ==========
taxonomy mean  stddev min max num_sites num_assets
tax1     1.000 NaN    1   1   1         1         
======== ===== ====== === === ========= ==========

Slowest sources
---------------
========= ================= ============ ========= ========= =========
source_id source_class      num_ruptures calc_time num_sites num_split
========= ================= ============ ========= ========= =========
1         SimpleFaultSource 482          0.0       1         0        
========= ================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
================= ========= ======
source_class      calc_time counts
================= ========= ======
SimpleFaultSource 0.0       1     
================= ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
compute_ruptures   0.030 0.013  0.013 0.054 14       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
total compute_ruptures         0.425     0.066     14    
managing sources               0.131     0.0       1     
making contexts                0.019     0.0       5     
saving ruptures                0.009     0.0       14    
reading composite source model 0.006     0.0       1     
store source_info              0.003     0.0       1     
reading exposure               0.002     0.0       1     
setting event years            0.001     0.0       1     
reading site collection        7.629E-06 0.0       1     
============================== ========= ========= ======