Classical PSHA-Based Hazard
===========================

============== ===================
checksum32     343,519,400        
date           2018-02-19T09:58:14
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 8

Parameters
----------
=============================== ==================
calculation_mode                'classical_damage'
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                0.1               
area_source_discretization      20.0              
ground_motion_correlation_model None              
random_seed                     42                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
exposure                `exposure_model.xml <exposure_model.xml>`_                  
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job_haz.ini <job_haz.ini>`_                                
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
structural_fragility    `fragility_model.xml <fragility_model.xml>`_                
======================= ============================================================

Composite source model
----------------------
========= ====== =============== ================
smlt_path weight gsim_logic_tree num_realizations
========= ====== =============== ================
b1        1.000  simple(2)       2/2             
========= ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================================== ========= ========== ==========
grp_id gsims                              distances siteparams ruptparams
====== ================================== ========= ========== ==========
0      AkkarBommer2010() SadighEtAl1997() rjb rrup  vs30       mag rake  
====== ================================== ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=2)
  0,AkkarBommer2010(): [1]
  0,SadighEtAl1997(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 1,694        1,694       
================ ====== ==================== ============ ============

Informational data
------------------
======================= ==================================================================================
count_ruptures.received tot 11.1 KB, max_per_task 814 B                                                   
count_ruptures.sent     sources 14.75 KB, srcfilter 9.87 KB, param 6.26 KB, monitor 4.36 KB, gsims 2.86 KB
hazard.input_weight     1694.0                                                                            
hazard.n_imts           1                                                                                 
hazard.n_levels         8                                                                                 
hazard.n_realizations   2                                                                                 
hazard.n_sites          1                                                                                 
hazard.n_sources        1                                                                                 
hazard.output_weight    8.0                                                                               
hostname                tstation.gem.lan                                                                  
require_epsilons        False                                                                             
======================= ==================================================================================

Exposure model
--------------
=============== ========
#assets         1       
#taxonomies     1       
deductibile     absolute
insurance_limit absolute
=============== ========

======== ===== ====== === === ========= ==========
taxonomy mean  stddev min max num_sites num_assets
Wood     1.000 NaN    1   1   1         1         
======== ===== ====== === === ========= ==========

Slowest sources
---------------
========= ================= ============ ========= ========= =========
source_id source_class      num_ruptures calc_time num_sites num_split
========= ================= ============ ========= ========= =========
1         SimpleFaultSource 1,694        0.039     16        15       
========= ================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
================= ========= ======
source_class      calc_time counts
================= ========= ======
SimpleFaultSource 0.039     1     
================= ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_ruptures     0.004 0.001  0.002 0.007 14       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
managing sources               0.095     0.0       1     
total count_ruptures           0.050     0.078     14    
reading composite source model 0.011     0.0       1     
store source_info              0.003     0.0       1     
reading exposure               0.002     0.0       1     
aggregate curves               1.869E-04 0.0       14    
saving probability maps        2.599E-05 0.0       1     
reading site collection        8.583E-06 0.0       1     
============================== ========= ========= ======