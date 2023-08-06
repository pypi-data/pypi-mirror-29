Classical PSHA — Area Source
============================

============== ===================
checksum32     3,283,112,543      
date           2018-02-19T09:59:19
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 19

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                0.2               
area_source_discretization      5.0               
ground_motion_correlation_model None              
random_seed                     23                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
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
source_model.xml 0      Active Shallow Crust 11,132       11,132      
================ ====== ==================== ============ ============

Informational data
------------------
======================= =================================================================================
count_ruptures.received tot 3.17 KB, max_per_task 812 B                                                  
count_ruptures.sent     sources 101.65 KB, srcfilter 2.82 KB, param 2.16 KB, monitor 1.25 KB, gsims 524 B
hazard.input_weight     1113.2                                                                           
hazard.n_imts           1                                                                                
hazard.n_levels         19                                                                               
hazard.n_realizations   1                                                                                
hazard.n_sites          1                                                                                
hazard.n_sources        1                                                                                
hazard.output_weight    19.0                                                                             
hostname                tstation.gem.lan                                                                 
require_epsilons        False                                                                            
======================= =================================================================================

Slowest sources
---------------
========= ============ ============ ========= ========= =========
source_id source_class num_ruptures calc_time num_sites num_split
========= ============ ============ ========= ========= =========
1         AreaSource   11,132       0.054     485       484      
========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
AreaSource   0.054     1     
============ ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_ruptures     0.018 0.005  0.010 0.021 4        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
managing sources               0.145     0.0       1     
total count_ruptures           0.071     0.0       4     
reading composite source model 0.070     0.0       1     
store source_info              0.003     0.0       1     
aggregate curves               5.960E-05 0.0       4     
reading site collection        4.673E-05 0.0       1     
saving probability maps        2.480E-05 0.0       1     
============================== ========= ========= ======