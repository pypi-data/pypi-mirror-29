Classical PSHA with NZ NSHM
===========================

============== ===================
checksum32     865,392,691        
date           2018-02-19T09:59:21
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 29

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 400.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                0.1               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     23                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ======================================================================
Name                    File                                                                  
======================= ======================================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                          
job_ini                 `job.ini <job.ini>`_                                                  
source                  `NSHM_source_model-editedbkgd.xml <NSHM_source_model-editedbkgd.xml>`_
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_          
======================= ======================================================================

Composite source model
----------------------
========= ====== ================ ================
smlt_path weight gsim_logic_tree  num_realizations
========= ====== ================ ================
b1        1.000  trivial(1,0,0,1) 1/1             
========= ====== ================ ================

Required parameters per tectonic region type
--------------------------------------------
====== =================== ========= ========== ===================
grp_id gsims               distances siteparams ruptparams         
====== =================== ========= ========== ===================
0      McVerry2006Asc()    rrup      vs30       hypo_depth mag rake
1      McVerry2006SInter() rrup      vs30       hypo_depth mag rake
====== =================== ========= ========== ===================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=1)
  0,McVerry2006Asc(): [0]
  1,McVerry2006SInter(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================================ ====== ==================== ============ ============
source_model                     grp_id trt                  eff_ruptures tot_ruptures
================================ ====== ==================== ============ ============
NSHM_source_model-editedbkgd.xml 0      Active Shallow Crust 40           40          
NSHM_source_model-editedbkgd.xml 1      Subduction Interface 1.000        2           
================================ ====== ==================== ============ ============

============= =====
#TRT models   2    
#eff_ruptures 41   
#tot_ruptures 42   
#tot_weight   6.000
============= =====

Informational data
------------------
======================= ===============================================================================
count_ruptures.received tot 1.65 KB, max_per_task 878 B                                                
count_ruptures.sent     sources 809.11 KB, srcfilter 1.41 KB, param 1.23 KB, monitor 638 B, gsims 245 B
hazard.input_weight     6.0                                                                            
hazard.n_imts           1                                                                              
hazard.n_levels         29                                                                             
hazard.n_realizations   1                                                                              
hazard.n_sites          1                                                                              
hazard.n_sources        4                                                                              
hazard.output_weight    29.0                                                                           
hostname                tstation.gem.lan                                                               
require_epsilons        False                                                                          
======================= ===============================================================================

Slowest sources
---------------
========= ========================= ============ ========= ========= =========
source_id source_class              num_ruptures calc_time num_sites num_split
========= ========================= ============ ========= ========= =========
21444     CharacteristicFaultSource 1            0.003     2         1        
1         PointSource               20           2.251E-04 2         1        
2         PointSource               20           1.569E-04 2         1        
21445     CharacteristicFaultSource 1            0.0       1         0        
========= ========================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
========================= ========= ======
source_class              calc_time counts
========================= ========= ======
CharacteristicFaultSource 0.003     2     
PointSource               3.819E-04 2     
========================= ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_ruptures     0.004 0.004  0.001 0.007 2        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
reading composite source model 0.191     0.0       1     
total count_ruptures           0.008     0.0       2     
managing sources               0.006     0.0       1     
store source_info              0.004     0.0       1     
aggregate curves               5.960E-05 0.0       2     
reading site collection        4.411E-05 0.0       1     
saving probability maps        2.527E-05 0.0       1     
============================== ========= ========= ======