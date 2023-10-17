import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

#low_pt=30
#high_pt=200
#endcap = -1
#layer=1
x_var = "nCLS" #"BA" or "rdphi" or "dphi" or "nCLS"
#eta = 8
#gaus_low = -2
#gaus_high = 2
#supch_cut = 1

f = ROOT.TFile("../test/output_qc8analyzer_10086.root")
event = f.Get("QC8Analyzer/analyzer")

if x_var == "BA":
  xlow = -10
  xhigh = 10
  x_plot = "1000*bending_angle"
  x_axis = "Bending Angle [mrad]"
elif x_var == "rdphi":
  xlow = -2
  xhigh = 2
  x_plot = "RdPhi_Corrected"
  x_axis = "#DeltaR#phi [cm]"
elif x_var == "dphi":
  xlow = -5
  xhigh = 5
  x_plot = "1000*dPhi_Corrected" #"-1000*(rechit_localphi_rad-prop_localphi_rad)"
  x_axis = "#Delta#phi [mRad]"
elif x_var == "nCLS":
  xlow = 0
  xhigh = 10
  x_plot = "rechit_CLS"
  x_axis = x_plot #"Cluster Size"
  xbins = 10

ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.08*W_ref

if x_var != "nCLS":
  xbins = 200
ybins = 100
xlow = xlow
xhigh = xhigh
ylow = -300
yhigh = 300
zlow = -2
zhigh = 2

canvas = ROOT.TCanvas("c1", "c1", 100, 100, W, H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)
#canvas.SetLogy()
canvas.SetGrid()

h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
xAxis = h.GetXaxis()
xAxis.SetTitleOffset(1)
xAxis.SetTitleSize(0.05)
if x_var == "BA":
  xAxis.SetNdivisions(-505)
xAxis.SetTitle("{x_axis}".format(x_axis=x_axis))
#xAxis.CenterTitle()

yAxis = h.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("Entries")
#yAxis.CenterTitle()
'''
ch_list = []
ch_list_even = []
ch_list_odd = []
even_cut = ""
odd_cut = ""

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"

for i in range(1,37):
  ch_list.append(str(i))
  if i%2 == 0:
    ch_list_even.append(str(i))
    if i==2:
      even_cut += "(prop_location[2]== {i} ||".format(i=i)
    elif i==36:
      even_cut += " prop_location[2] == {i})".format(i=i)
    else:
      even_cut += " prop_location[2] == {i} ||".format(i=i)
  else:
    ch_list_odd.append(str(i))
    if i==1:
      odd_cut += "(prop_location[2]== {i} ||".format(i=i)
    elif i==35:
      odd_cut += " prop_location[2] == {i})".format(i=i)
    else:
      odd_cut += " prop_location[2] == {i} ||".format(i=i)

if supch_cut==0:
  cut = even_cut
  ch_string = "Even"
elif supch_cut==1:
  cut = odd_cut
  ch_string = "Odd"
'''
#layer = prop_location[3]
#chamber = prop_location[2]
#region or endcap = prop_location[0]

event.Project("h", "{x}".format(x=x_plot), "".format())

h.SetLineWidth(3) #3

h.SetMarkerSize(0)

#yAxis.SetRangeUser(0, 1.5*h.GetMaximum())
yAxis.SetRangeUser(0, 4000)
yAxis.SetMaxDigits(3)

h.Draw("HIST")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.3*canvas.GetTopMargin())

latex.SetTextAlign(32)
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "QC8GE21")#"(13.6 TeV)")
latex.SetTextAlign(12)

latex.DrawLatex(0.6-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Run 10086")#"2023 Data")

latex.SetTextSize(0.25*canvas.GetTopMargin())
#latex.DrawLatex(0.5-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.8*canvas.GetTopMargin(), "{low} GeV".format(low=low_pt)+" < p_{T}^{GLB} < "+"{high} GeV".format(high=high_pt)) 
'''
if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"
'''
#latex.DrawLatex(0.5-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "{reg}Endcap Layer {lay} All {ch} Chambers".format(reg=reg_string, lay=layer, ch=ch_string))
#latex.DrawLatex(0.5-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "Superchambers: 1, 5 , 7, 9, 19, 27, 31")
#latex.DrawLatex(0.35-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "Superchambers: 4, 6, 12, 16, 24, 26, 30, 32, 36")
latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
#latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.27*canvas.GetTopMargin(), "B904")#"CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.3*canvas.GetTopMargin())
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Simulation Preliminary")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()


canvas.SaveAs("10086/nCLS.png".format())
