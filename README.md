# evolutionSim

This is the GitHub repo for project Evolution-Simulator.

[intro video/中文简介视频](https://www.bilibili.com/video/BV18Y41117rJ/) (only Chinese avaliable now)

Following studies on this project is in repo [EvoSim](https://github.com/midstreeeam/EvoSim).

## Quick Start

### Install

This project working on Python 3.6 and later version. (If you want to run it on 3.10, you need to ban the usage of Numba)

Then clone the repo and do the following

```shell
cd evolutionSim
pip install -r requirements.txt
```

After install the requirements, try to run the demo.

```shell
cd animation
python3 run.py
```



### Window

As showed in the picture, left part is the map of the virtual world, right part is the panel that shows the useful information. Green pixel means food, blue pixels represent living cells, and black pixels are predators. Every cell has one side with black line, which marks cell’s “face”.

In the middle of the right part, there is a dynamic list, which shows the Top 10 most successful geno-type and the corresponding number.

<img src="https://github.com/midstreeeam/evolutionSim/blob/main/images/window.png?raw=true" alt="window" style="zoom:70%;" />



### Control

When the simulation is running, you can pause the simulation by pressing `C` on your keyboard, and press again to continue the simulation.

During the simulation, clicking on the Top-10 geno-type bar on the right side will mark all cells in that gene. Marked cells and its offspring will change color to red.

When gene is too long, the panel will only show part of it. To get the full gene of one cell, you need to click the cell with mouse. Then the full gene will be print to the terminal.



## Advance Operation

To modifying more parameters of the simulator, you need to change them in the `animation_config.py` file.

### Operate config file

There are plenty of variable that can be changed in `animation_config.py` file. 

Here are several most commonly used parameters. More information in code comments.

- `GRID_SIZE`, represent the size of the grid. Can be bigger if your computer is strong enough.
- `ENLARGE_RATE`, using to adjust the static window size.
- `AUTO_RESTART`, automatically start a new era if all cells died in last one.
- `CELL_AGE` and `PREDATOR_AGE`, how long can a cell or predator lives.
- `REPRODUCE_THRESHOULD` and `PREDATOR_REPRODUCE_THRESHOULD`, how much a cell/predator need to eat to reproduce.
- `FOOD_MAX_AGE`, how long can a food live if no cell eat it.
- `GEN_FOOD_RATE`, how quick the food is generate.

- `RAND_GENE_LENGTH`, gene length of cell. Longer the gene clever the cell can be, but slower the evolution.
- `MAX_NEURAL_NUM`, maximum inner neuron allowed.
- `WEIGHT_MU_RATE` and `LINK_MU_RATE`, the rate that the mutation happens in newly born cell.

### Activate Refresh Mode

To activate refresh mode, which similar to [biosim4](https://github.com/davidrmiller/biosim4), you need to change `REFRESH_MODE` to `True`.

If you activate the refresh mode, here are several useful parameter that you might explore.

- `INDIVIDUAL_NUM`, how many individuals are there in the field.
- `ERA_LENGTH`, how long each generation takes. (calculated in frame)
- `LEFTTOP` and `RIGHTBOTTOM`, should be a list of tuples that represent locations. Cells in that location after generation ended will die.
- `RAND_GENE_LENGTH`, gene length of cell. Longer the gene clever the cell can be, but slower the evolution.
- `WEIGHT_MU_RATE` and `LINK_MU_RATE`, the rate that the mutation happens in newly born cell.



## About

This project is a attempts on genetic algorithm and bio simulation.
See project report [here](https://midstream.cn/blogs/biosim.html) for more details.

This project takes some ideas from [biosim4](https://github.com/davidrmiller/biosim4)(see his video [here](https://www.youtube.com/watch?v=N3tRFayqVtk)), but exploring more on natural evolution rather than solving man-made questions.

Feel free to contact me for any questions. Email: kl389@duke.edu.

## Demo

Here is a [video demo](https://youtu.be/X7VmNgw6EXk) to show that how cells evolve intelligence after a half a million steps. 

