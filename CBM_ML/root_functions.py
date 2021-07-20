import sys, ROOT
import pandas as pd
from ROOT import TF1, TCanvas,TMath, TColor
import math


def truncate(number, decimals=2):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def background_selector(df):
    df1 = df[(df['mass']<1.108)]
    df2 = df[df['mass']>1.13]
    df3 = pd.concat([df1, df2])
    return df3['mass'] 

def h1_set(h1):
    h1 . SetTitleOffset(-1)
    h1 . SetFillStyle(3003);
    h1 . SetLineWidth(2)
    h1 . SetStats (0)
    h1 . SetYTitle("Entries")
    h1 . SetLineColor (ROOT . kBlack)
    h1 . GetXaxis () . SetLabelSize (0)
    h1 . GetXaxis () . SetTitleSize (0)
    h1 . GetYaxis () . SetTitleSize (0.05)
    h1 . GetYaxis () . SetLabelSize (0.03)
    h1 . GetYaxis () . SetTitleOffset (0.6)
    h1 . GetYaxis () . SetNdivisions(107)
    return h1


def h3_set(h3):   
    h3 . SetLineWidth(2)
    h3 . SetStats (0)
    h3 . GetXaxis() . SetTitle("Mass [GeV/c^{2}]")
    h3 . SetTitle ("")
    h3 . GetXaxis () . SetLabelSize (0.12)
    h3 . GetXaxis () . SetTitleSize (0.12)
    h3 . GetYaxis () . SetLabelSize (0.1)
    h3 . GetYaxis () . SetTitleSize (0.15)
    #ratio . GetYaxis (). SetTitle (" Data /MC")
    h3 . GetYaxis (). SetTitleOffset (0.17)
    #207,512 divisions
    h3 . GetYaxis (). SetNdivisions (207)
    h3 . GetXaxis (). SetNdivisions (207)
    h3.SetLineColor(TColor.GetColor(5))
    h3.SetYTitle("d-f/#Deltad")
    return h3


def draw_line(line):
    line . SetLineColor ( ROOT . kRed )
    line . SetLineWidth (2)
    return line


ROOT.gInterpreter.Declare('''
TH1F h1_set(TH1F& h1) {
    h1 . SetTitleOffset(-1);
    h1 . SetFillStyle(3003);
    h1 . SetLineWidth(2);
    h1 . SetStats (0);
    h1 . SetYTitle("Entries");
    h1 . SetLineColor (kBlack);
    h1 . GetXaxis () -> SetLabelSize (0);
    h1 . GetXaxis () -> SetTitleSize (0);
    h1 . GetYaxis () -> SetTitleSize (0.05);
    h1 . GetYaxis () -> SetLabelSize (0.03);
    h1 . GetYaxis () -> SetTitleOffset (0.6);
    h1 . GetYaxis () -> SetNdivisions(107);
    return h1;
}
''')


ROOT.gInterpreter.Declare('''
TH1F h3_set(TH1F& h3) {
    h3 . SetLineWidth(2);
    h3 . SetStats (0);
    h3 . GetXaxis() -> SetTitle("Mass [GeV/c^{2}]");
    h3 . SetTitle ("");
    h3 . GetXaxis () -> SetLabelSize (0.12);
    h3 . GetXaxis () -> SetTitleSize (0.12);
    h3 . GetYaxis () -> SetLabelSize (0.1);
    h3 . GetYaxis () -> SetTitleSize (0.15);
    h3 . GetYaxis () -> SetTitleOffset (0.17);
    h3 . GetYaxis () ->  SetNdivisions (207);
    h3 . GetXaxis () -> SetNdivisions (207);
    h3 . SetLineColor (kBlack);
    h3 . SetYTitle("d-f/#Deltad");
    return h3;
}
''')


def f_set(ftot, fs, fb):
    ftot.SetNpx(100000);
    ftot.SetLineColor(ROOT.kRed)
    
    fs.SetNpx(100000);
    fs.SetLineColor(ROOT.kGreen)
    
    fb.SetLineStyle(4)
    fb.SetLineColor(ROOT.kBlue)
    fb.SetNpx(100000);
    return ftot, fs, fb

ROOT.gInterpreter.Declare('''
TLine draw_line(TLine& line) {
    line . SetLineColor ( kRed );
    line . SetLineWidth (2);
    return line;
}
''')

def draw_latex():
    latex = ROOT . TLatex ()
    latex . SetNDC ()
    latex . SetTextSize (0.02)
#    latex . DrawLatex (0.4 ,0.85, "Significance in m_{0} #pm 2.5#Gamma  = #frac{%.1f #pm %.1f}{#sqrt{%.1f+%.1f}} = %.1f"%(signal_under_peak_2_point_5_sigma, man_sigma_signal_under_peak_2_point_5_sigma, signal_under_peak_2_point_5_sigma,bac_under_peak_2_point_5_sigma,signal_under_peak_2_point_5_sigma/TMath.Sqrt(bac_under_peak_2_point_5_sigma+signal_under_peak_2_point_5_sigma) ))
#    latex . DrawLatex (0.4 ,0.80, "Significance in m_{0} #pm 3#Gamma = #frac{%.1f #pm %.1f}{#sqrt{%.1f+%.1f}} = %.1f"%(signal_under_peak_3_sigma,man_sigma_signal_under_peak_3_sigma, signal_under_peak_3_sigma,backgnd_under_peak_3_sigma,signal_under_peak_3_sigma/TMath.Sqrt(backgnd_under_peak_3_sigma+signal_under_peak_3_sigma) ))
#    latex . DrawLatex (0.4 ,0.75, "Significance in m_{0} #pm 3.5#Gamma = #frac{%.1f #pm %.1f}{#sqrt{%.1f+%.1f}} = %.1f"%(signal_under_peak_3_point_5_sigma,man_sigma_signal_under_peak_3_point_5_sigma,signal_under_peak_3_point_5_sigma,bac_under_peak_3_point_5_sigma,signal_under_peak_3_point_5_sigma/TMath.Sqrt(signal_under_peak_3_point_5_sigma+bac_under_peak_3_point_5_sigma) ))
    latex . DrawLatex (0.4 ,0.70, " #Gamma = %.4f #pm %.5f GeV"%(par2 [1],f2.GetParError(1) ))
    latex . DrawLatex (0.4 ,0.65, " m_{0} = %.4f #pm %.5f GeV"%(par2 [2],f2.GetParError(2) ))
    if f2.GetNDF()!= 0:
        latex . DrawLatex (0.4 ,0.6," #frac{#chi^{2}}{ndf} = %.1f/%d = %.4f"%(f2.GetChisquare() , f2.GetNDF() , f2.GetChisquare() / f2.GetNDF() ))
    latex . DrawLatex (0.4 ,0.55," True signal (MC=1) = %.f"%(mc_counts))
    return latex
    
    
def draw_legend(fit_func):
    if fit_func =='gaus':
        var1 = "e^{-0.5 (#frac{x-#mu}{#sigma})^2} "
    if fit_func =='lorenz':
        var1 = "#frac{0.5 #Gamma}{(m-m_{0})^{2} + 0.25#Gamma^{2}} "
    
    legend = ROOT.TLegend(0.87,0.3,0.6,0.6);
    legend . AddEntry(h1,"Invariant mass of lambda","l")
    #legend.AddEntry(f2,"A "+var1+"+B+Cx+Dx^{2}","l")
    legend.AddEntry(fs,"A "+var1,"l")
    #legend . AddEntry(fb,"B+Cx+Dx^{2}","l")
    legend . SetLineWidth (0)
    return legend


def createCanvasPads():
    c = ROOT . TCanvas (" canvas ","", 1200,1000)
    
    pad1 = ROOT . TPad (" pad1 "," pad1 " ,0 ,0.3 ,1 ,1)
    pad1 . SetBottomMargin (0)
    pad1 . Draw ()
    
    pad2 = ROOT . TPad (" pad2 "," pad2 " ,0 ,0.05 ,1 ,0.3)
    pad2 . SetGrid()
    pad2 . SetTopMargin (0)
    pad2 . SetBottomMargin (0.25)
    pad2 . Draw ()
    return c, pad1, pad2


ROOT.gInterpreter.Declare('''
void compute(TH1F& h1, Double_t i) {
h1.Fill(i);
}
''')


def draw_hist(h1, f2, fs, fb, h3):   
    c, pad1, pad2 = createCanvasPads ()
    c . Draw ()
    pad1 . cd ()
    
    #h1 = h1_set (h1)
    h1 = ROOT . h1_set (h1)
    f2, fs, fb = f_set (f2, fs, fb)
    
    h1 . Draw("pe")
    fs . Draw("SAME")
    fb . Draw("SAME")
    f2 . Draw("SAME")
    draw_latex()
    legend = draw_legend ('lorenz')
    legend . Draw()
    
    c . cd ()
    pad2 . cd ()
    
    #h3_set(h3) . Draw()
    h3 = ROOT . h3_set(h3)
    h3 . Draw()
    
    #line = draw_line (line = ROOT . TLine (mm,0 ,1.23 ,0))
    line = ROOT . draw_line (line = ROOT . TLine (mm,0 ,1.23 ,0))
    line . Draw (" same ")
    c . Print ("/home/shahid/cbmsoft/Cut_optimization/uncut_data/Project/pT_rapidity_distribution_XGB_extracted_signal.pdf [")
    
    
    
def signal_cal(h1, f2, fs, fb):
    tot_sig_3_point_5_sigma, tot_sig_3_sigma, tot_sig_2_point_5_sigma, tot_sig_2_sigma = 0, 0, 0, 0
    tot_bac_3_sigma, tot_bac_3_point_5_sigma, tot_bac_2_point_5_sigma = 0, 0, 0    
    
    binwidth = h1.GetXaxis().GetBinWidth(1);
    tot = f2.Integral(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])))/binwidth;
    sigma_integral = f2.IntegralError(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])));
    #params.integral = fit->GetParameter(0) * sqrt(2*3.1415) * fit->GetParameter(2) / h->GetBinWidth(1);
    #signal_under_peak = par2[1] * np.sqrt(2*3.1415) *3 *par2[2]/ binwidth
    signal_under_peak_3_sigma = fs.Integral(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])))/binwidth
               
    sigma_signal_under_peak_3_sigma = fs.IntegralError(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])));
    man_sigma_signal_under_peak_3_sigma = TMath.Sqrt(signal_under_peak_3_sigma)


    tot_sig_3_sigma= tot_sig_3_sigma+signal_under_peak_3_sigma
#Background
    backgnd_under_peak_3_sigma = (fb.Integral(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])))/binwidth)

    sigma_backgnd_under_peak_3_sigma = fb.IntegralError(par2[2] - (TMath.Abs(3*par2[1])),par2[2] + (TMath.Abs(3*par2[1])));
    tot_bac_3_sigma = tot_bac_3_sigma+backgnd_under_peak_3_sigma

    signal_under_peak_3_point_5_sigma = (fs.Integral(par2[2] - (TMath.Abs(3.5*par2[1])),par2[2] + (TMath.Abs(3.5*par2[1])))/binwidth);
    bac_under_peak_3_point_5_sigma = (fb.Integral(par2[2] - (TMath.Abs(3.5*par2[1])),par2[2] + (TMath.Abs(3.5*par2[1])))/binwidth);
    tot_sig_3_point_5_sigma = tot_sig_3_point_5_sigma+signal_under_peak_3_point_5_sigma
    tot_bac_3_point_5_sigma = tot_bac_3_point_5_sigma + bac_under_peak_3_point_5_sigma

    sigma_signal_under_peak_3_point_5_sigma = fs.IntegralError(par2[2] - (TMath.Abs(3.5*par2[1])),par2[2] + (TMath.Abs(3.5*par2[1])));
    man_sigma_signal_under_peak_3_point_5_sigma = TMath.Sqrt(signal_under_peak_3_point_5_sigma)

    signal_under_peak_2_point_5_sigma = (fs.Integral(par2[2] - (TMath.Abs(2.5*par2[1])),par2[2] + (TMath.Abs(2.5*par2[1])))/binwidth);
    bac_under_peak_2_point_5_sigma = (fb.Integral(par2[2] - (TMath.Abs(2.5*par2[1])),par2[2] + (TMath.Abs(2.5*par2[1])))/binwidth);
    tot_sig_2_point_5_sigma = tot_sig_2_point_5_sigma+signal_under_peak_2_point_5_sigma
    tot_bac_2_point_5_sigma = tot_bac_2_point_5_sigma + bac_under_peak_2_point_5_sigma

    sigma_signal_under_peak_2_point_5_sigma = fs.IntegralError(par2[2] - (TMath.Abs(2.5*par2[1])),par2[2] + (TMath.Abs(2.5*par2[1])));
    man_sigma_signal_under_peak_2_point_5_sigma = TMath.Sqrt(signal_under_peak_2_point_5_sigma)

    signal_under_peak_2_sigma = (fs.Integral(par2[2] - (TMath.Abs(2*par2[1])),par2[2] + (TMath.Abs(2*par2[1])))/binwidth);
    
    return  signal_under_peak_3_sigma, man_sigma_signal_under_peak_3_sigma, backgnd_under_peak_3_sigma, signal_under_peak_3_point_5_sigma, bac_under_peak_3_point_5_sigma, tot_sig_3_point_5_sigma, tot_bac_3_point_5_sigma, man_sigma_signal_under_peak_3_point_5_sigma, signal_under_peak_2_point_5_sigma, man_sigma_signal_under_peak_2_point_5_sigma, bac_under_peak_3_point_5_sigma, bac_under_peak_2_point_5_sigma, signal_under_peak_2_point_5_sigma, signal_under_peak_2_sigma




