#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Julian Teuber
# Created Date: 29.04.2022
# version ='1.0'
# ---------------------------------------------------------------------------
"""
{Description}
{License_info}
# TODO: enable vias along polygons
"""

# kicad specific librarys
import pcbnew
from pcbnew import *
from pcbnew import wxPoint, wxPoint_Vector
import wx

# system libs
import os

# mathematical operations
import numpy as np
from numpy import sin, cos, ceil, linspace, double
from math import pi

# morphological operations
from shapely.geometry import LineString, MultiLineString
from shapely import ops

from . import ViasAlongPathDlg

debug = True
res = 10


def wxLogDebug(msg, show):
    """printing messages only if show is omitted or True"""
    if show:
        wx.LogMessage(msg)


def PopulateNets(anet, dlgChoices):
    nets = pcbnew.GetBoard().GetNetsByName()
    for netname, net in nets.items():
        netname = net.GetNetname()
        if netname is not None and netname != "":
            dlgChoices.Append(netname)
    if anet is not None:
        index = dlgChoices.FindString(anet)
        dlgChoices.Select(index)


class ViasAlongPath_Dlg(ViasAlongPathDlg.ViasAlongPathDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(ViasAlongPath_Dlg, self).SetSizeHints(sz1, sz2)

    def onRunClick(self, event):
        return self.EndModal(wx.ID_REVERT)

    def __init__(self,  parent):
        import wx
        ViasAlongPathDlg.ViasAlongPathDlg.__init__(self, parent)
        self.SetMinSize(self.GetSize())
        self.SetIcon(wx.Icon(os.path.join(
            os.path.dirname(__file__), "./vias_along_path.png")))
        self.m_buttonRun.Bind(wx.EVT_BUTTON, self.onRunClick)
        self.m_buttonRun.SetFocus()
        if wx.__version__ < '4.0':
            self.m_buttonRun.SetToolTipString(
                u"Place vias along the selected path.")
            self.m_buttonCancel.SetToolTipString(
                u"Close the plugin.")
        else:
            self.m_buttonRun.SetToolTip(
                u"Place vias along the selected path.")
            self.m_buttonCancel.SetToolTip(
                u"Close the plugin.")


class ViasAlongPath(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Vias Along Path"  # As shown when hovering over the toolbar icon
        self.category = "Modify PCB"
        self.description = "Create vias evenly spaced along the selected path."
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "./vias_along_path.png")
        self.show_toolbar_button = True

    def Warn(self, message, caption='Warning!'):
        dlg = wx.MessageDialog(
            None, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

    def CheckDistanceInput(self, value, data):
        val = None
        try:
            val = float(value.replace(',', '.'))
            if val <= 0:
                raise Exception("Invalid")
        except:
            self.Warn(
                "Invalid parameter for %s: Must be a positive number" % data)
            val = None
        return val

    def Run(self):
        pcb = pcbnew.GetBoard()
        _pcbnew_frame = [x for x in wx.GetTopLevelWindows()
                         if x.GetName() == 'PcbFrame'][0]
        aParameters = ViasAlongPath_Dlg(_pcbnew_frame)
        aParameters.Show()
        aParameters.m_DistMM.SetValue("2.0")
        aParameters.m_SizeMM.SetValue("0.8")
        aParameters.m_DrillMM.SetValue("0.4")
        PopulateNets("GND", aParameters.m_NetName)
        aParameters.m_bitmapHelp.SetBitmap(wx.Bitmap(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), r"res\via_path_help.png")))

        # aParameters.m_bitmap1.SetBitmap(wx.Bitmap(os.path.join(
        #    os.path.dirname(os.path.realpath(__file__)), "round_track_help.png")))
        modal_result = aParameters.ShowModal()
        viaDist = FromMM(self.CheckDistanceInput(
            aParameters.m_DistMM.GetValue(), "distance between vias"))
        viaSize = FromMM(self.CheckDistanceInput(
            aParameters.m_SizeMM.GetValue(), "size of the vias"))
        viaDrill = FromMM(self.CheckDistanceInput(
            aParameters.m_DrillMM.GetValue(), "drill size of the vias"))
        viaNet = aParameters.m_NetName.GetStringSelection()

        if viaDist is not None and viaSize is not None and viaDrill is not None:
            if modal_result == wx.ID_REVERT:
                create_vias(pcb, viaDist, viaSize, viaDrill, viaNet)
            else:
                None  # Cancel
        else:
            None  # Invalid input
        aParameters.Destroy()


def create_vias(pcb, viaDist, viaSize, viaDrill, viaNet):
    shapes = selected_shapes(pcb)
    shapes_arc = []
    shapes_line = []

    if shapes == []:
        wx.LogError("No line geometrie selected!")
        return

    # Destinguish between straight lines and arcs
    for shape in shapes:
        if shape.GetRadius() == 1:
            shapes_line.append(shape)
        else:
            shapes_arc.append(shape)

    n_arcs = len(list(shapes_arc))
    n_lines = len(list(shapes_line))
    wxLogDebug(f"{n_arcs} arc(s) and {n_lines} line(s) selected", debug)

    line_segments = []

    # Parse streight lines to shapely LineString
    for line in shapes_line:
        x1 = line.GetStartX()
        y1 = line.GetStartY()
        x2 = line.GetEndX()
        y2 = line.GetEndY()
        segment = LineString([[x1, y1], [x2, y2]])
        line_segments.append(segment)

    # Parse arcs to shapely LineString
    for arc in shapes_arc:
        pos = arc.GetCenter()  # wxPoint
        rad = arc.GetRadius()  # double
        aStart = arc.GetArcAngleStart()  # double
        aEnd = aStart + arc.GetArcAngle()  # double

        if arc.GetArcAngle() < 0:  # sense of rotation can be negative
            # allways use mathematical sense of rotation
            (aStart, aEnd) = (aEnd, aStart)

        # Flatten arcs to streight line segments
        arc_segments = arcToSegments(pos, rad, aStart, aEnd, res)
        # Ensure line endpoints are coincident
        arc_segments[0] = arc.GetStart()
        arc_segments[-1] = arc.GetEnd()
        line_segments.append(arc_segments)

    multi_line = MultiLineString(line_segments)
    line = ops.linemerge(multi_line)

    # Guard clause for non contigous lines
    if type(line) == MultiLineString:
        wx.LogError("Non contiguous lines selected!")
        return

    # Guard clause for self intersecting lines
    if not line.is_simple:
        wx.LogError("Line crosses itself!")
        return

    distances = np.arange(0, line.length, viaDist)
    points = [line.interpolate(distance)
              for distance in distances]
    points = points + [line.boundary[1]] if not line.is_ring else points
    viaPoints = ops.unary_union(points)

    # Place vias on precalculated points
    for viaPoint in viaPoints:
        if not(hasattr(pcbnew, 'DRAWSEGMENT')):
            newVia = pcbnew.PCB_VIA(pcb)
        else:
            newVia = pcbnew.VIA(pcb)
        if hasattr(newVia, 'SetTimeStamp'):
            ts = 4711
            # adding a unique number as timestamp to mark this via as generated by this script
            newVia.SetTimeStamp(ts)

        pcb.Add(newVia)
        newVia.SetPosition(pcbnew.wxPoint(viaPoint.x, viaPoint.y))
        newVia.SetWidth(viaSize)
        newVia.SetDrill(viaDrill)

        if hasattr(pcbnew, 'VIA_THROUGH'):
            newVia.SetViaType(pcbnew.VIA_THROUGH)
        else:
            newVia.SetViaType(pcbnew.VIATYPE_THROUGH)

        net = pcb.FindNet(viaNet)
        if net is not None:
            newVia.SetNet(net)

    wxLogDebug(f"Line is a closed ring.", line.is_ring and debug)
    wxLogDebug(f"Path length is {ToMM(line.length):.3f} mm.", debug)
    wxLogDebug(f"{len(viaPoints)} vias placed.", debug)


def selected_shapes(pcb):
    shapes = []
    for item in pcb.GetDrawings():
        if item.IsSelected() and isinstance(item, pcbnew.PCB_SHAPE):
            shapes.append(item)
    return shapes


def FromDeg(pcbnewAngle):
    return pcbnewAngle*10


def arcToSegments(center: wxPoint, rad: double, aStart: double, aEnd: double, resolution: int):
    aFull = 3600  # full angel, pcbnew uses 1/10 degrees angles
    aArc = (aEnd - aStart) % aFull
    # prevent linspace from counnting backwards
    if aStart > aEnd:
        aEnd += 3600
    angles = linspace(2*pi*aStart/aFull, 2*pi*aEnd/aFull,
                      int(ceil(4*resolution*abs(aArc)/10)))
    xs = np.round(rad * cos(angles))
    ys = np.round(rad * sin(angles))
    arc_points = []
    for i in range(len(angles)):
        arc_points.append(center + wxPoint(xs[i], ys[i]))
    return arc_points
