# cricket-topology

This repository contains scripts and data that was used for the work:  [Spatial Comparison of Cricketers](https://hal.inria.fr/hal-01852138/document/).

- If you are a cricket enthusiast: This repository has all the scripts to retrieve and parse cricket pitchmaps from ball trajectories for any match. 
- If you are a topology enthusiast:  Head [here](https://github.com/kamakshidasan/irrelevant/). I showcase the scripts that I use to run batch processes in TTK.

Motivation is from a cricinfo [article](http://www.espncricinfo.com/story/_/id/18411329/why-cricket-proper-metrics-fielding)

- Schedules are scrapped from ICC, Ball Trajectories from IPL.
- Trajectory parsing is using Pulse.
- Pitchmap generation and interpolation is using ArcGIS.
- Topological Analysis is using [TTK](https://topology-tool-kit.github.io/)
- Earthmover's distance is using [PyEMD](https://github.com/wmayner/pyemd)
- Bottleneck/Wasserstein distances are using [TDA](http://www.win.tue.nl/SoCG2015/wp-content/uploads/tutorials/150623_presentation_2.pdf)
- Fitting a curve to histogram is using [astropy](http://www.astropy.org/)
- Heatmap visualization inspired from [here](http://www.racketracer.com/2015/05/12/analytics-of-optimal-2-for-1-strategy-in-nba-basketball/)


If you find this repository useful, spread the love by citing the above work :)
