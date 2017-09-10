# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 18:43:02 2016

@author: anneya


                      .-.
                 .--.(   ).--.
      <-.  .-.-.(.->          )_  .--.
       `-`(     )-'             `)    )
         (o  o  )                `)`-'
        (      )                ,)
        ( ()  )                 )
         `---"\    ,    ,    ,/`
               `--' `--' `--'
                |  |   |   |
                |  |   |   |
                '  |   '   |
                
Produces Sankey Diagrams with matplotlib

Copyright (C) 2016  Anneya Golob

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter
plt.rc('text',usetex=False)
plt.rc('font',family='serif')
import seaborn as sns;
sns.set_style("white",{'font.family':[u'serif']})


        
def sankey(before,after,colorDict={},aspect=4,rightColor=False,fontsize=14):
    '''
    Make Sankey Diagram showing flow from before-->after
    
    Inputs:
        left = NumPy array of object labels on the left of the digram
        right = NumPy array of corresponding labels on the right of the digram 
            len(right) == len(left)
        colorDict = Dictionary of colors to use for each label {'label':'color'}
        aspect = vertical extent of the digram in units of horizontal extent
        rightColor = If true, each strip in the diagram will be be colored 
                    according to its left label
    Ouput:
        None
    '''
    
    df = pd.DataFrame({'before':before,'after':after},index=range(len(before)))
    
    # Identify all labels that appear 'before' or 'after'
    #allLabels = pd.Series(np.r_[np.array(Counter(before).most_common())[:,0],np.array(Counter(after).most_common())[:,0]]).unique()
    allLabels = np.array(Counter(np.r_[before,after]).most_common())[:,0][::-1]
    
    # If no colorDict given, make one
    if colorDict == {}:
        pal = "hls"
        cls = sns.color_palette(pal, len(allLabels))
        for i,l in enumerate(allLabels):
            colorDict[l] = cls[i]
    
    # Determine widths of individual strips
    ns = defaultdict()
    for l in allLabels:
        myD = {}
        for l2 in allLabels:
            myD[l2] = len(df[(df.before==l) & (df.after==l2)])
        ns[l] = myD
        
    # Determine positions of left and right label patches and total widths
    widths = defaultdict()
    for i,l in enumerate(allLabels):
        myD = {}
        myD['left'] = len(df[df.before==l])
        myD['right'] = len(df[df.after==l])
        myD['total'] = max(myD['left'],myD['right'])
        if i==0:    
            myD['bottom'] = 0
            myD['top'] = myD['total']
            myD['leftBottom'] = 0.5*(myD['top']+myD['bottom']) - 0.5*myD['left']
            myD['rightBottom'] = 0.5*(myD['top']+myD['bottom']) - 0.5*myD['right']
        else:
            myD['bottom'] = widths[allLabels[i-1]]['top'] + 0.02*len(df)
            myD['top'] = myD['bottom'] + myD['total']
            myD['leftBottom'] = 0.5*(myD['top']+myD['bottom']) - 0.5*myD['left']
            myD['rightBottom'] = 0.5*(myD['top']+myD['bottom']) - 0.5*myD['right']
            topEdge = myD['top']
        widths[l] = myD
    
    # Total vertical extent of diagram
    xMax = topEdge/aspect
    
    # Draw vertical bars on left and right of each  label's section & print label
    for l in allLabels:
        plt.fill_between([-0.02*xMax,0],2*[widths[l]['leftBottom']],\
            2*[widths[l]['leftBottom']+widths[l]['left']],color=colorDict[l],alpha=0.99)
        plt.fill_between([xMax,1.02*xMax],2*[widths[l]['rightBottom']],\
            2*[widths[l]['rightBottom']+widths[l]['right']],color=colorDict[l],alpha=0.99)
            
        plt.text(-0.05*xMax,widths[l]['leftBottom']+0.5*widths[l]['left'],l,{'ha': 'right', 'va': 'center'},fontsize=fontsize)
        plt.text(1.05*xMax,widths[l]['rightBottom']+0.5*widths[l]['right'],l,{'ha': 'left', 'va': 'center'},fontsize=fontsize)
        
    # Plot strips
    for l in allLabels:
        for l2 in allLabels:
            lc = l
            if rightColor:
                lc = l2
            # Create array of y values for each strip, half at left value, half at right, convolve
            ys = np.array(50*[widths[l]['leftBottom']+0.5*ns[l][l2]]+50*[widths[l2]['rightBottom']+0.5*ns[l][l2]])
            ys = np.convolve(ys,0.05*np.ones(20),mode='valid')
            ys = np.convolve(ys,0.05*np.ones(20),mode='valid')
            
            # Update bottom edges at each label so next strip starts at the right place
            widths[l]['leftBottom'] = widths[l]['leftBottom']+ns[l][l2]
            widths[l2]['rightBottom'] = widths[l2]['rightBottom']+ns[l][l2]
            plt.fill_between(np.linspace(0,xMax,len(ys)),ys-0.5*ns[l][l2],ys+0.5*ns[l][l2],alpha=0.65,color=colorDict[lc])
        
    plt.gca().axis('off')  