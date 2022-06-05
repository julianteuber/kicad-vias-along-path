# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class ViasAlongPathDlg
###########################################################################

class ViasAlongPathDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Vias Along Path", pos = wx.DefaultPosition, size = wx.Size( 300,475 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer_Main = wx.BoxSizer( wx.VERTICAL )

		bSizer_Image = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmapHelp = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer_Image.Add( self.m_bitmapHelp, 1, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer_Image.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer_Main.Add( bSizer_Image, 1, wx.ALIGN_RIGHT|wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

		fgSizer_Parameters = wx.FlexGridSizer( 4, 2, 0, 0 )
		fgSizer_Parameters.SetFlexibleDirection( wx.BOTH )
		fgSizer_Parameters.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_DistMM_Text = wx.StaticText( self, wx.ID_ANY, u"Via distance (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_DistMM_Text.Wrap( -1 )

		fgSizer_Parameters.Add( self.m_DistMM_Text, 0, wx.ALL, 5 )

		self.m_DistMM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Parameters.Add( self.m_DistMM, 0, wx.ALL, 5 )

		self.m_SizeMM_Text = wx.StaticText( self, wx.ID_ANY, u"Via size (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_SizeMM_Text.Wrap( -1 )

		fgSizer_Parameters.Add( self.m_SizeMM_Text, 0, wx.ALL, 5 )

		self.m_SizeMM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Parameters.Add( self.m_SizeMM, 0, wx.ALL, 5 )

		self.m_DrillMM_Text = wx.StaticText( self, wx.ID_ANY, u"Via drill (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_DrillMM_Text.Wrap( -1 )

		fgSizer_Parameters.Add( self.m_DrillMM_Text, 0, wx.ALL, 5 )

		self.m_DrillMM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Parameters.Add( self.m_DrillMM, 0, wx.ALL, 5 )

		self.m_NetName_Text = wx.StaticText( self, wx.ID_ANY, u"Net name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_NetName_Text.Wrap( -1 )

		fgSizer_Parameters.Add( self.m_NetName_Text, 1, wx.ALL, 5 )

		m_NetNameChoices = []
		self.m_NetName = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_NetNameChoices, 0 )
		fgSizer_Parameters.Add( self.m_NetName, 1, wx.ALL, 5 )


		bSizer_Main.Add( fgSizer_Parameters, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer_Main.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer_Buttons = wx.BoxSizer( wx.HORIZONTAL )


		bSizer_Buttons.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_buttonRun = wx.Button( self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_Buttons.Add( self.m_buttonRun, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )

		self.m_buttonCancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_Buttons.Add( self.m_buttonCancel, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer_Main.Add( bSizer_Buttons, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer_Main )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


