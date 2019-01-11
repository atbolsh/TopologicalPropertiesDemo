# Automatic Generation of Strongly Monotone Fixed Point Grids and Lists
## Demo code for paper "Topological properties of strongly monotone planar vector fields," Bolshakov, Balanov and Rachinskii

This code builds on concepts introduced in the paper.

It allows the user to automatically print out all valid grids of arbitrary size (functions `all_validi` and `all_unique`), perform all the permutations described, and freely convert between lists and grids.

Internally, fixed points which are *Repellers*, *Attractors,* and *Saddles*, as described in the paper, are encoded as -1, -2, and -3, respectively, while the quadrants are encoded as the positive numbers 1 - 4. The grids are stored (and indexed) in such a way that calling `print` on a grid produces a readable representation. The function `display` can perform this operation in bulk; for instance, we can reproduce a primitive version of Figure 3 from the paper by calling 
```
>>> from demo import *
>>>
>>>
>>> display(all_unique(4))
```

Which yields

```
[[ 4  4  4 -1]
 [ 4  4 -2  2]
 [ 4 -3  2  2]
 [-2  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4  4  4 -2]
 [ 4  4 -3  2]
 [ 4 -2  2  2]
 [-3  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4  4 -3  1]
 [ 4  4  3 -1]
 [ 4 -2  2  2]
 [-1  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4  4 -3  1]
 [ 4  4  3 -1]
 [ 4 -2  2  2]
 [-3  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4  4 -2  1]
 [ 4 -3  2  1]
 [ 4  3  3 -1]
 [-2  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4 -1  1  1]
 [ 4  3 -3  1]
 [ 4  3  3 -1]
 [-2  2  2  2]]
++++++++++++++++++++++++++++++++++++++
[[ 4 -3  1  1]
 [ 4  3 -1  1]
 [ 4  3  3 -3]
 [-2  2  2  2]]
++++++++++++++++++++++++++++++++++++++
>>>
```
A more presentation-friendly format is accessible through the functions `g_to_tikz` and `l_to_tikz`, which produce LaTeX code for the pictures you see in the paper (provided you `\usepackage{tikz}`).

The most important backend function is `is_valid`, which implements all of the restrictions described in Definition 3.7.

It should be noted that this is all for demonstration purposes only; any practical application should be written in a lower-level language, and the algorithms should be more efficient. This is not optimized for long computations; if you have an interest in a computational exploration of strongly monotone vector fields, it is recommended that you contact the corresponding author of this paper at dmitry.rachinsky@utdallas.edu, or the programmer of this script at atb86@cornell.edu.


