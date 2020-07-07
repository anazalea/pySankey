# -*- coding: utf-8 -*-
"""
Produces simple Sankey Diagrams with matplotlib.
@author: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
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
"""

# fmt: off
import warnings
import logging
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
# fmt: on

LOGGER = logging.getLogger(__name__)

class PySankeyException(Exception):
    """ Generic PySankey Exception. """


class NullsInFrame(PySankeyException):
    pass


class LabelMismatch(PySankeyException):
    pass


def check_data_matches_labels(labels, data, side):
    """Check whether or not data matches labels.

    Raise a LabelMismatch Exception if not."""
    if len(labels) > 0:
        if isinstance(data, list):
            data = set(data)
        if isinstance(data, pd.Series):
            data = set(data.unique().tolist())
        if isinstance(labels, list):
            labels = set(labels)
        if labels != data:
            msg = "\n"
            if len(labels) <= 20:
                msg = "Labels: " + ",".join(labels) + "\n"
            if len(data) < 20:
                msg += "Data: " + ",".join(data)
            raise LabelMismatch(
                "{0} labels and data do not match.{1}".format(side, msg)
            )


def sankey(
    left,
    right,
    leftWeight=None,
    rightWeight=None,
    colorDict=None,
    alphaDict=None,
    leftLabels=None,
    rightLabels=None,
    aspect=4,
    rightColor=False,
    fontsize=14,
    figureName=None,
    closePlot=False,
    figSize=None,
    ax=None,
    color_gradient=None
):
    """
    Make Sankey Diagram showing flow from left-->right

    Inputs:
        left = NumPy array of object labels on the left of the diagram
        right = NumPy array of corresponding labels on the right of the diagram
            len(right) == len(left)
        leftWeight = NumPy array of weights for each strip starting from the
            left of the diagram, if not specified 1 is assigned
        rightWeight = NumPy array of weights for each strip starting from the
            right of the diagram, if not specified the corresponding leftWeight
            is assigned
        colorDict = Dictionary of colors to use for each label
            {'label':'color'}
        leftLabels = order of the left labels in the diagram
        rightLabels = order of the right labels in the diagram
        aspect = vertical extent of the diagram in units of horizontal extent
        rightColor = If true, each strip in the diagram will be be colored
                    according to its left label
        figSize = tuple setting the width and height of the sankey diagram.
            Defaults to current figure size
        ax = optional, matplotlib axes to plot on, otherwise uses current axes.
    Output:
        ax : matplotlib Axes
    """
    warn = []
    if figureName is not None:
        msg = "use of figureName in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])
    if closePlot is not False:
        msg = "use of closePlot in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])
    if figSize is not None:
        msg = "use of figSize in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])

    if warn:
        LOGGER.warning(
            " The following arguments are deprecated and should be removed: %s",
            ", ".join(warn),
        )

    if ax is None:
        ax = plt.gca()

    if leftWeight is None:
        leftWeight = []
    if rightWeight is None:
        rightWeight = []
    if leftLabels is None:
        leftLabels = []
    if rightLabels is None:
        rightLabels = []
    # Check weights
    if len(leftWeight) == 0:
        leftWeight = np.ones(len(left))

    if len(rightWeight) == 0:
        rightWeight = leftWeight

    # Create Dataframe
    if isinstance(left, pd.Series):
        left = left.reset_index(drop=True)
    if isinstance(right, pd.Series):
        right = right.reset_index(drop=True)
    dataFrame = pd.DataFrame(
        {
            "left": left,
            "right": right,
            "leftWeight": leftWeight,
            "rightWeight": rightWeight,
        },
        index=range(len(left)),
    )

    if len(dataFrame[(dataFrame.left.isnull()) | (dataFrame.right.isnull())]):
        raise NullsInFrame("Sankey graph does not support null values.")

    # Identify all labels that appear 'left' or 'right'
    allLabels = pd.Series(
        np.r_[dataFrame.left.unique(), dataFrame.right.unique()]
    ).unique()
    LOGGER.debug("Labels to handle : %s", allLabels)

    # Identify left labels
    if len(leftLabels) == 0:
        leftLabels = pd.Series(dataFrame.left.unique()).unique()
    else:
        check_data_matches_labels(leftLabels, dataFrame["left"], "left")

    # Identify right labels
    if len(rightLabels) == 0:
        rightLabels = pd.Series(dataFrame.right.unique()).unique()
    else:
        check_data_matches_labels(rightLabels, dataFrame["right"], "right")

    # If no colorDict given, make one
    if colorDict is None:
        colorDict = {}
        palette = "hls"
        colorPalette = sns.color_palette(palette, len(allLabels))
        for i, label in enumerate(allLabels):
            colorDict[label] = colorPalette[i]
    else:
        missing = [label for label in allLabels if label not in colorDict.keys()]
        if missing:
            msg = (
                "The colorDict parameter is missing values for the following labels : "
            )
            msg += "{}".format(", ".join(missing))
            raise ValueError(msg)
    LOGGER.debug("The colordict value are : %s", colorDict)

    # If no alphaDict given, make one
    if alphaDict is None:
        alphaDict = {}
        for i, label in enumerate(allLabels):
            alphaDict[label] = 0.65
    else:
        missing = [label for label in allLabels if label not in alphaDict.keys()]
        if missing:
            msg = (
                "The alphaDict parameter is missing values for the following labels : "
            )
            msg += "{}".format(", ".join(missing))
            raise ValueError(msg)
    LOGGER.debug("The alphadict value are : %s", alphaDict)

    # Determine widths of individual strips
    ns_l = defaultdict()
    ns_r = defaultdict()
    for leftLabel in leftLabels:
        leftDict = {}
        rightDict = {}
        for rightLabel in rightLabels:
            leftDict[rightLabel] = dataFrame[
                (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            ].leftWeight.sum()
            rightDict[rightLabel] = dataFrame[
                (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            ].rightWeight.sum()
        ns_l[leftLabel] = leftDict
        ns_r[leftLabel] = rightDict

    # Determine positions of left label patches and total widths
    leftWidths, topEdge = _get_positions_and_total_widths(dataFrame, leftLabels, "left")

    # Determine positions of right label patches and total widths
    rightWidths, topEdge = _get_positions_and_total_widths(
        dataFrame, rightLabels, "right"
    )

    # Total vertical extent of diagram
    xMax = topEdge / aspect

    # Draw vertical bars on left and right of each  label's section & print label
    left_coords = {}
    for leftLabel in leftLabels:
        x1 = -0.02 * xMax
        x2 = 0
        y1 = 2 * [leftWidths[leftLabel]['bottom']]
        y2 = 2 * [leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left']]
        left_coords[leftLabel] = (x1, x2, y1[0], y2[0])
        ax.fill_between((x1, x2), y1, y2, color=colorDict[leftLabel], alpha=0.99)
        ax.text(
            -0.05 * xMax,
            leftWidths[leftLabel]["bottom"] + 0.5 * leftWidths[leftLabel]["left"],
            leftLabel.strip(),
            {"ha": "right", "va": "center"},
            fontsize=fontsize,
        )
    right_coords = {}
    for rightLabel in rightLabels:
        x1 = xMax
        x2 = 1.02 * xMax
        y1 = 2 * [rightWidths[rightLabel]['bottom']]
        y2 = 2 * [rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right']]
        right_coords[rightLabel] = (x1, x2, y1[0], y2[0])
        ax.fill_between((x1, x2), y1, y2, color=colorDict[rightLabel], alpha=0.99)
        ax.text(
            1.05 * xMax,
            rightWidths[rightLabel]["bottom"] + 0.5 * rightWidths[rightLabel]["right"],
            rightLabel.strip(),
            {"ha": "left", "va": "center"},
            fontsize=fontsize,
        )

    # Plot strips
    for leftLabel in leftLabels:
        for rightLabel in rightLabels:
            labelColor = leftLabel
            if rightColor:
                labelColor = rightLabel
            if (
                len(
                    dataFrame[
                        (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
                    ]
                )
                > 0
            ):
                # Create array of y values for each strip, half at left value,
                # half at right, convolve
                ys_d = np.array(
                    50 * [leftWidths[leftLabel]["bottom"]]
                    + 50 * [rightWidths[rightLabel]["bottom"]]
                )
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode="valid")
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode="valid")
                ys_u = np.array(
                    50 * [leftWidths[leftLabel]["bottom"] + ns_l[leftLabel][rightLabel]]
                    + 50
                    * [rightWidths[rightLabel]["bottom"] + ns_r[leftLabel][rightLabel]]
                )
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode="valid")
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode="valid")

                # Update bottom edges at each label so next strip starts at the right place
                leftWidths[leftLabel]['bottom'] += ns_l[leftLabel][rightLabel]
                rightWidths[rightLabel]['bottom'] += ns_r[leftLabel][rightLabel]
                if color_gradient:
                    if (leftLabel, rightLabel) in colorDict:
                        cleft = cright = colorDict[leftLabel, rightLabel]
                    else:
                        cleft = colorDict[leftLabel]
                        cright = colorDict[rightLabel]
                    if (leftLabel, rightLabel) in alphaDict:
                        alpha = alphaDict[leftLabel, rightLabel]
                    else:
                        alpha = alphaDict[labelColor]

                    x = list(np.linspace(0, xMax, len(ys_d)))
                    poly, = ax.fill(x + x[::-1] + [x[0]], list(ys_d) + list(ys_u)[::-1] + [ys_d[0]], facecolor='none')

                    # get the extent of the axes
                    xmin, xmax = ax.get_xlim()
                    ymin, ymax = ax.get_ylim()

                    # create a dummy image
                    img_data = np.arange(xmin,xmax,(xmax-xmin) / 100.)
                    img_data = img_data.reshape(img_data.size, 1).T

                    # plot and clip the image
                    im = ax.imshow(img_data, aspect='auto', origin='lower', cmap=mpl.colors.LinearSegmentedColormap.from_list(
                        'custom', [cleft, cright]), alpha=alpha, extent=[xmin,xmax,ymin,ymax])

                    im.set_clip_path(poly)
                else:
                    if (leftLabel, rightLabel) in colorDict:
                        color = colorDict[leftLabel, rightLabel]
                    else:
                        color = colorDict[labelColor]
                    if (leftLabel, rightLabel) in alphaDict:
                        alpha = alphaDict[leftLabel, rightLabel]
                    else:
                        alpha = alphaDict[labelColor]
                    plt.fill_between(
                        np.linspace(0, xMax, len(ys_d)), ys_d, ys_u, alpha=alpha,
                        color=color
                    )

    if figSize is not None:
        plt.gcf().set_size_inches(figSize)

    ax.axis('off')

    if figureName is not None:
        fileName = "{}.png".format(figureName)
        plt.savefig(fileName, bbox_inches="tight", dpi=300)
        LOGGER.info("Sankey diagram generated in '%s'", fileName)
    if closePlot:
        plt.close()

    return ax, left_coords, right_coords


def _get_positions_and_total_widths(df, labels, side):
    """ Determine positions of label patches and total widths"""
    widths = defaultdict()
    for i, label in enumerate(labels):
        labelWidths = {}
        labelWidths[side] = df[df[side] == label][side + "Weight"].sum()
        if i == 0:
            labelWidths["bottom"] = 0
            labelWidths["top"] = labelWidths[side]
        else:
            bottomWidth = widths[labels[i - 1]]["top"]
            weightedSum = 0.02 * df[side + "Weight"].sum()
            labelWidths["bottom"] = bottomWidth + weightedSum
            labelWidths["top"] = labelWidths["bottom"] + labelWidths[side]
            topEdge = labelWidths["top"]
        widths[label] = labelWidths
        LOGGER.debug("%s position of '%s' : %s", side, label, labelWidths)
    if len(labels) == 1:
        topEdge = topEdge = labelWidths["top"]

    return widths, topEdge
