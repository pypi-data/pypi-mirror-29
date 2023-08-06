from pathlib import Path
import logging
from numpy.ma import masked_invalid
from matplotlib.pyplot import figure, draw
from matplotlib.ticker import MultipleLocator #LogFormatterMathtext,
from matplotlib.colors import LogNorm

dymaj=50
dymin=10
dpi = 100

def _nicez(ax, zlim:tuple=None):
    """ make ordinate axis look nice for altitude """
    ax.autoscale(True,axis='both',tight=True)
    ax.set_ylim(zlim)
    ax.yaxis.set_major_locator(MultipleLocator(dymaj))
    ax.yaxis.set_minor_locator(MultipleLocator(dymin))
    ax.grid(True,which='major',linewidth=1.)
    ax.grid(True,which='minor',linewidth=0.5)
    ax.tick_params(axis='both',which='major',labelsize='medium')


def plotaurora(phitop,ver,zceta,photIon,isr,sion,t,glat:float, glon:float,
               prate, lrate, tez, E0:float,
               flux:float=None, sza:float=None, zlim:tuple=None,
               makeplot:list=None, odir:Path=None):
    """ Plot all sorts of auroral/dayglow parameters from GLOW simulation. """
    if makeplot is None:
        return

    if E0 and sza:
        titlend = '$E_0={E0:.0f}$ eV  SZA={sza:.1f}$^\circ$'
    else:
        titlend = ''

#%% neutral background (MSIS) and Te,Ti (IRI-90)
    if not 'eig' in makeplot:
        fg = figure(figsize=(15,8))
        axs = fg.subplots(1,2,sharey=True,)
        fg.suptitle(f'{t} ({glat},{glon}) ' + titlend)

        ind = ['nO','nO2','nN2','nNO']
        ax = axs[0]
        # Need to use .values here.
        ax.semilogx(photIon.loc[:,ind].values, photIon.z_km)
        ax.set_xlabel('Number Density')
        ax.set_xscale('log')
        ax.set_xlim(left=1e1)
        ax.set_ylabel('Altitude [km]')
        _nicez(ax,zlim)
        ax.legend(ind)
        ax.set_title('Neutral Number Density')

        ind=['Te','Ti']
        ax = axs[1]
        # Need to use .values here.
        ax.semilogx(isr.loc[:,ind].values, isr.z_km)
        ax.set_xlabel('Temperature [K]')
        ax.legend(ind)
        _nicez(ax,zlim)
        ax.set_xlim(100,10000)
        ax.set_title('Background Temperature')

        writeplots(fg,odir,'bg_',E0,makeplot)
#%% production and loss rates for species
    if 'eig' in makeplot:
        plotprodloss(prate.loc['final',...],
                     lrate.loc['final',...],t,glat,glon,zlim,'',titlend)
#%% volume emission rate
    fg = figure(figsize=(15,8))
    axs = fg.subplots(1,3,sharey=False)
    fg.suptitle(f'{t} ({glat},{glon}) ' + titlend)
    fg.tight_layout(pad=3.2, w_pad=0.6)

#%% incident flux at top of ionosphere
    ax = axs[0]
    ax.plot(phitop.eV,phitop,marker='.')

    titxt='Incident Flux'
    if flux:
        titxt += f'  Total Flux={flux:.1f},'
    ax.set_title(titxt)

    ax.set_xlabel('Beam Energy [eV]')
    ax.set_ylabel('Flux [erg sr$^{-1}$ s$^{-1}$]')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(1e-4,1e6)
    ax.grid(True)
# %% ver visible
    ind= [4278, 5200, 5577, 6300]
    ax = axs[1]
    ax.plot(ver.loc[...,ind].values.squeeze(), ver.z_km)
    ax.set_xlabel('Volume Emission Rate')
    ax.set_ylabel('altitude [km]')
    _nicez(ax,zlim)
    ax.set_xscale('log')
    if not 'eig' in makeplot:
        ax.set_xlim(1e-5,1e3)
    ax.legend(ind,loc='best')
    ax.set_title('Volume Emission Rate: Visible')
#%% ver invisible
    ind = [3371,7320,10400,3466,7774, 8446,3726,1356., 1304., 1027., 989., 1900.]
    ax = axs[2]
    ax.plot(ver.loc[...,ind].values, ver.z_km)
    ax.set_xlabel('Volume Emission Rate')
    _nicez(ax,zlim)
    ax.set_xscale('log')
    if not 'eig' in makeplot:
        ax.set_xlim(1e-5,1e3)
    ax.legend(ind,loc='best')
    ax.set_title('Volume Emission Rate: IR & UV')

    writeplots(fg,odir,'ver_',E0,makeplot)
# %% Ne, Ni
    if not 'eig' in makeplot:
        ind=['ne','nO+(2P)','nO+(2D)','nO+(4S)','nN+','nN2+','nO2+','nNO+']
        fg=figure()
        ax = fg.gca()
        ax.semilogx(photIon.loc[:,ind].values, photIon.z_km)
        ax.set_xlabel('Density')
        ax.set_xscale('log')
        ax.set_xlim(left=1e-3)
        _nicez(ax,zlim)
        ax.legend(ind)
        ax.set_title('Electron and Ion Densities')
        ax.set_ylabel('Altitude [km]')

        writeplots(fg,odir,'effects_',E0,makeplot)
# %% total energy deposition vs. altitude
    if not 'eig' in makeplot:
        plotenerdep(tez,t,glat,glon,zlim,titlend)
#% % e^- impact ionization rates from ETRANS
        fg = figure(figsize=(15,8))
        axs = fg.subplots(1,2,sharey=True,)
        fg.suptitle(f'{t} ({glat},{glon})  '+ titlend)
        fg.tight_layout(pad=3.2, w_pad=0.3)

        ind=['photoIoniz','eImpactIoniz']
        ax = axs[0]
        ax.plot(photIon.loc[:,ind].values, photIon.z_km)
        ax.set_xlabel('ionization')
        ax.set_xscale('log')
        ax.set_xlim(left=1e-1)
        _nicez(ax,zlim)
        ax.legend(ind)
        ax.set_title('Photo and e$^-$ impact ionization')
        ax.set_ylabel('Altitude [km]')

        ind=['O','O2','N2']
        ax = axs[1]
        ax.plot(sion.T.values, sion.z_km)
        ax.set_xscale('log')
        ax.set_xlim(1e-5,1e4)
        _nicez(ax,zlim)
        ax.set_xlabel('e$^-$ impact ioniz. rate')

        ax.set_title('electron impact ioniz. rates')
        ax.legend(ind)

        writeplots(fg,odir,'ioniz_',E0,makeplot)
#%% constituants of per-wavelength VER
#    zcsum = zceta.sum(axis=-1)
    if not 'eig' in makeplot:
        fg = figure(figsize=(15,8))
        axs = fg.subplots(3,4,sharey=True)
        for ax,zc,i in zip(axs.ravel(),
                           zceta.transpose('wavelength_nm','type','z_km'),
                           zceta.wavelength_nm):
            ax.plot(zc.T,zc.z_km)
            ax.set_xscale('log')
            #ax.set_xlabel('emission constituants  ' + titlend)
            ax.set_ylabel('Altitude [km]')
            ax.set_title(f'{i.values} angstrom')
            #ax.legend(True)

        writeplots(fg,odir,'constit_',E0,makeplot)


def plotenerdep(tez,t,glat,glon,zlim,titlend=''):
    """ plot energy deposition vs. altitude """
    fg= figure()
    ax = fg.gca()
    if tez.ndim==1:
        ax.plot(tez,tez.z_km)
        ax.set_xscale('log')
        ax.set_xlim(1e-1,1e6)
        ax.set_xlabel('Energy Deposited')
    else:
        ax.set_label('Beam Energy [eV]')
        hi=ax.pcolormesh(tez.eV,tez.z_km,masked_invalid(tez.values),norm=LogNorm())
        cb=fg.colorbar(hi,ax=ax)
        cb.set_label('Energy Deposited')

    _nicez(ax,zlim)
    ax.set_title('Total Energy Depostiion')
    ax.set_ylabel('altitude [km]')


def plotprodloss(prod,loss,t,glat,glon,zlim,titlbeg='',titlend=''):
    """ plot production/loss vs. alttiude """
    fg = figure(figsize=(15,8))
    ax = fg.subplots(1,2,sharey=True)
    fg.suptitle(titlbeg + f' Volume Production/Loss Rates   {t} ({glat},{glon}) ' + titlend)

    ax[0].set_title('Volume Production Rates')
    ax[0].set_ylabel('altitude [km]')

    ax[1].set_title('Volume Loss Rates')

    for a,R in zip(ax,[prod,loss]):
        try:
            hi=a.pcolormesh(R.eV.values,
                            R.z_km.values,
                            masked_invalid(R.values),
                            norm=LogNorm()) #pcolormesh canNOT handle nan at all!
            cb=fg.colorbar(hi,ax=a)
            cb.set_label('[cm$^{-3}$ s$^{-1}$ eV$^{-1}$]',labelpad=0)
            a.set_xscale('log')
            a.set_xlabel('Beam Energy [eV]')
    #        a.legend(prod.minor_axis,loc='best')  # old, when plotting for each energy / input spectrum
            _nicez(a,zlim)
        except TypeError as e:
            logging.warning(f'prodloss plot error    {e}')

# %%
def writeplots(fg:figure, odir:Path, plotprefix:str, E0:float, method:str='png'):
    """ Save Matplotlib plots to disk.

    inputs:
    ------

    fg: Matplotlib figure handle
    odir: directory to write image into e.g. for this particular simulation.
    plotprefix: stem of filename
    E0: beam energy (eV)
    method: format of image

    Some observations on image formats:

      * TIF was not faster and was 100 times the file size!
      * PGF is slow and big file,
      * RAW crashes
      * JPG no faster than PNG
    """
    if not odir:
        return

    odir = Path(odir).expanduser()
    draw() #Must have this here or plot doesn't update in animation multiplot mode!

    if 'png' in method:
        cn = odir / (plotprefix + f'beam{E0:.0f}.{method}')
        print('write',cn)
        fg.savefig(cn, bbox_inches='tight', dpi=dpi)  # this is slow and async
