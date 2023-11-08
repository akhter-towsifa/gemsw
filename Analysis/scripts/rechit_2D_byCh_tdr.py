import ROOT, tdrstyle, sys, os, array

run = "10100"

f = ROOT.TFile("../test/output_qc8analyzer_{r}.root".format(r=run))
event = f.Get("QC8Analyzer/analyzer")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.20*W_ref

xbins = 300
ybins = 16
xlow = -60
xhigh = 60
ylow = -70
yhigh = 130

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

h_list = []

for ch in range(2, 8):
  h_list.append(ROOT.TH2D("h{ch}".format(ch=ch), "h{ch}".format(ch=ch), xbins, xlow, xhigh, ybins, ylow, yhigh))
  xAxis = h_list[ch-2].GetXaxis()
  xAxis.SetTitleOffset(2)
  xAxis.SetTitleSize(0.04)
  xAxis.SetTitle("GE2/1 RecHit Global X [cm]")

  yAxis = h_list[ch-2].GetYaxis()
  yAxis.SetTitleOffset(0)
  yAxis.SetTitleSize(0.04)
  yAxis.SetTitle("GE2/1 RecHit Global Y [cm]")

  event.Project("h{ch}".format(ch=ch), "rechit_GP[1]:rechit_GP[0]", "rechit_location[2]=={ch}".format(ch=ch))
  h_list[ch-2].SetMaximum(16)
  h_list[ch-2].Draw("colz")

  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)

  latex.SetTextFont(42)
  latex.SetTextSize(0.27*canvas.GetTopMargin())
  latex.SetTextAlign(32)
  latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "QC8GE21")

  latex.SetTextAlign(12)
  latex.DrawLatex(0.4-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Run {r} layer {ch}".format(ch=ch, r=run))

  latex.SetTextSize(0.5*canvas.GetTopMargin())
  latex.SetTextFont(61)
  latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.27*canvas.GetTopMargin(), "B904")

  frame = canvas.GetFrame()
  frame.Draw()

  canvas.SaveAs("{r}/rechit_ch{ch}_2D.png".format(ch=ch, r=run))
