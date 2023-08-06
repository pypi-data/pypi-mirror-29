Event Based QA Test, Case 13
============================

============== ===================
checksum32     3,958,324,456      
date           2018-02-19T09:59:44
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 3

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         5000              
truncation_level                2.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     42                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
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
source_model.xml 0      Active Shallow Crust 1.000        1           
================ ====== ==================== ============ ============

Informational data
------------------
========================= ==========================================================================
compute_ruptures.received max_per_task 91.23 KB, tot 91.23 KB                                       
compute_ruptures.sent     sources 1.32 KB, src_filter 722 B, param 583 B, monitor 319 B, gsims 131 B
hazard.input_weight       0.1                                                                       
hazard.n_imts             1                                                                         
hazard.n_levels           3                                                                         
hazard.n_realizations     1                                                                         
hazard.n_sites            1                                                                         
hazard.n_sources          1                                                                         
hazard.output_weight      50.0                                                                      
hostname                  tstation.gem.lan                                                          
require_epsilons          False                                                                     
========================= ==========================================================================

Slowest sources
---------------
========= ============ ============ ========= ========= =========
source_id source_class num_ruptures calc_time num_sites num_split
========= ============ ============ ========= ========= =========
1         PointSource  1            0.0       1         0        
========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
PointSource  0.0       1     
============ ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
compute_ruptures   0.038 NaN    0.038 0.038 1        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
managing sources               0.085     0.0       1     
total compute_ruptures         0.038     0.145     1     
saving ruptures                0.033     0.0       1     
setting event years            0.028     0.0       1     
store source_info              0.005     0.0       1     
reading composite source model 0.001     0.0       1     
making contexts                6.373E-04 0.0       1     
reading site collection        5.341E-05 0.0       1     
============================== ========= ========= ======