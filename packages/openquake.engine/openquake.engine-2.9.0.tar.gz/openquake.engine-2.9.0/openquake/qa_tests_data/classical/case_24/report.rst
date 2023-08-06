Classical PSHA using Area Source
================================

============== ===================
checksum32     1,839,663,514      
date           2018-02-19T09:59:01
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 197

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            5.0               
complex_fault_mesh_spacing      5.0               
width_of_mfd_bin                0.3               
area_source_discretization      10.0              
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
source_model.xml 0      Active Shallow Crust 260          260         
================ ====== ==================== ============ ============

Informational data
------------------
======================= ============================================================================
count_ruptures.received max_per_task 812 B, tot 812 B                                               
count_ruptures.sent     sources 11.41 KB, param 2.49 KB, srcfilter 722 B, monitor 319 B, gsims 131 B
hazard.input_weight     26.0                                                                        
hazard.n_imts           9                                                                           
hazard.n_levels         197                                                                         
hazard.n_realizations   1                                                                           
hazard.n_sites          1                                                                           
hazard.n_sources        1                                                                           
hazard.output_weight    197.0                                                                       
hostname                tstation.gem.lan                                                            
require_epsilons        False                                                                       
======================= ============================================================================

Slowest sources
---------------
========= ============ ============ ========= ========= =========
source_id source_class num_ruptures calc_time num_sites num_split
========= ============ ============ ========= ========= =========
1         AreaSource   260          0.007     53        52       
========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
AreaSource   0.007     1     
============ ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_ruptures     0.009 NaN    0.009 0.009 1        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
reading composite source model 0.026     0.0       1     
managing sources               0.022     0.0       1     
total count_ruptures           0.009     0.0       1     
store source_info              0.004     0.0       1     
reading site collection        5.794E-05 0.0       1     
saving probability maps        3.171E-05 0.0       1     
aggregate curves               2.217E-05 0.0       1     
============================== ========= ========= ======