# To-do's:

### □: posted <br> ☑︎: completed <br> ☒: cancelled <br> ○: in progress <br> ●: on hold <br> ◌: unconfirmed

---

##### ☑︎ Resolve `run.py` and `kaggle_competition_mini_sample` Dataset Incompatibility
##### ☑︎ Data Retrieval - Execute Python code to fetch data
##### ☑︎ Create data roadmap for project

---

##### ○ Revise script to better modularize data transformation and visualization steps
##### ○ U-Net Notebook - Develop `U-Net` notebook

##### □ Organize repo branches
##### □ Notebook Tests - Create tests for `U-Net` notebook
##### □ Check if conversion to `float64` in `compute_stats` function causes issues

##### □ Refactor and tidy the `/sample` folder, ∴  `usage` in `README.md`

##### □ Refactor `.gitignore` and `requirements.txt` or `.yml` files

##### □ Complete the `docs_index.md` build.
##### □ Adapt setup to use `manba`` and/or `pip`` for package management

##### □ Update roadmap with checked off items and new features: stats, histogram``

##### □ Add scatterplots, other visualizations, and data augmentation

##### □ Add multiple bands of data to the visualization script. Normalize the data  and create false-color  images. 
##### □ Sequence and instance segmentation analisys. How many different contrails where detected?

##### ◌ Generate animations over time for visual inspection using `.json` files?

##### ◌ Use of the GOES-R Split-Window Difference to Diagnose Deepening Low-Level Water Vapor Channels ([Two bands centered at 10.35 and 12.3 μm. Split-window difference is brightness temperature difference between these bands providing information about atmospheric column water vapor](https://journals.ametsoc.org/view/journals/apme/53/8/jamc-d-14-0010.1.xml)). Or, total water vapor in vertical atmospheric column. 

##### ☒ Script that test [utils/direcotry_tree_generator](https://www.kaggle.com/code/patimejia/utils-directory-tree-generator) and potentially the mini open contrail sample
##### ● Draw: wrap data along z on globe, pass data to `plot_3d` function

---
##### ☒ Draw: script to imagine a global reference ellipsoid

---


- **Pending**: Implement changes to reduce memory usage in script by processing numpy files in smaller batches, reducing the resolution of histograms, or refactoring code to discard data when no longer needed. Also, fix the repeated legend issue.

