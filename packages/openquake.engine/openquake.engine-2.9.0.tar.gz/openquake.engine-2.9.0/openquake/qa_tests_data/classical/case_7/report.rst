Classical Hazard QA Test, Case 7
================================

============== ===================
checksum32     359,954,679        
date           2018-02-19T09:59:20
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 3

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                0.0               
rupture_mesh_spacing            0.1               
complex_fault_mesh_spacing      0.1               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     1066              
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model_1.xml <source_model_1.xml>`_                  
source                  `source_model_2.xml <source_model_2.xml>`_                  
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ====== =============== ================
smlt_path weight gsim_logic_tree num_realizations
========= ====== =============== ================
b1        0.700  trivial(1)      1/1             
b2        0.300  trivial(1)      0/0             
========= ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,SadighEtAl1997(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================== ====== ==================== ============ ============
source_model       grp_id trt                  eff_ruptures tot_ruptures
================== ====== ==================== ============ ============
source_model_1.xml 0      Active Shallow Crust 140          140         
================== ====== ==================== ============ ============

Informational data
------------------
======================= ===========================================================================
count_ruptures.received tot 1.58 KB, max_per_task 811 B                                            
count_ruptures.sent     sources 2.22 KB, srcfilter 1.41 KB, param 836 B, monitor 638 B, gsims 240 B
hazard.input_weight     378.0                                                                      
hazard.n_imts           1                                                                          
hazard.n_levels         3                                                                          
hazard.n_realizations   2                                                                          
hazard.n_sites          1                                                                          
hazard.n_sources        3                                                                          
hazard.output_weight    3.0                                                                        
hostname                tstation.gem.lan                                                           
require_epsilons        False                                                                      
======================= ===========================================================================

Slowest sources
---------------
========= ================== ============ ========= ========= =========
source_id source_class       num_ruptures calc_time num_sites num_split
========= ================== ============ ========= ========= =========
1         SimpleFaultSource  91           0.003     2         1        
2         ComplexFaultSource 49           0.003     2         1        
========= ================== ============ ========= ========= =========

Computation times by source typology
------------------------------------
================== ========= ======
source_class       calc_time counts
================== ========= ======
ComplexFaultSource 0.003     1     
SimpleFaultSource  0.003     1     
================== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ========= ===== ===== =========
operation-duration mean  stddev    min   max   num_tasks
count_ruptures     0.004 1.598E-04 0.004 0.004 2        
================== ===== ========= ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
reading composite source model 0.201     0.0       1     
total count_ruptures           0.007     0.0       2     
managing sources               0.007     0.0       1     
store source_info              0.003     0.0       1     
reading site collection        4.482E-05 0.0       1     
aggregate curves               3.171E-05 0.0       2     
saving probability maps        2.718E-05 0.0       1     
============================== ========= ========= ======