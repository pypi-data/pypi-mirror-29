
Some tips how to use jscatter efficient.

**Configuration for xmgrace**

 A template can be saved to .grace/templates/Default.agr
 This is opened whenever you open xmgrace as a standard layout.
 If you open this file with a text editor you may change the order of colors.

 To allow easier data loading in xmgrace a configuration file can be used that defines filters.
 This prevents for most files that text lines make errors if ASCII is imported.
 Set your desktop environment to open .agr files by click.
 Save this to .grace/gracerc
 ::

    # define input filter
    # the used endings were filtered to accept only lines starting with +,- or a number .123 also
    # filters are used for files with given suffix
    DEFINE IFILTER "egrep '*' '%s'" PATTERN "*.agr"
    DEFINE IFILTER "egrep '*' '%s'" PATTERN "*.user"
    DEFINE IFILTER "tail -n+6 '%s' | egrep '^(\s*[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)+\s*$|^\s*$'" PATTERN "*.pdh"
    DEFINE IFILTER "egrep '^(\s*[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)+\s*$|^\s*$' '%s'" PATTERN "*.???"
    DEFINE IFILTER "egrep '^(\s*[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)+\s*$|^\s*$' '%s'" PATTERN "*"
    #  Device Setup    Menue Print setup
    # default output format to print to
    HARDCOPY DEVICE "JPEG"
    #HARDCOPY DEVICE "Postscript"
    #default set to
    #PAGE LAYOUT FREE
    # options for eps
    DEVICE "EPS" OP "bbox:tight"
    DEVICE "PNG" DPI 300
    #options for Postscript
    DEVICE "PostScript" DPI 300
    #general page  -size  or do it with dafault.agr


**Reading data from a xmgrace figure**
 and extracting the legend.
 Just in case you didnt save your data :-)
 ::

    aq=js.dL('examples/effectiveDiffusion.agr')
    leg=[s[13:-1] for s in aq[0].comment if 'legend' in s and s[2] is 's' ]
    for line in filter(lambda a:'legend' in a and a[2]=='s',aq[0].comment):
        i=int(line.split()[1][1])
        aq[i].legend=line.split('"')[1]


**Xmgrace special characters**
  ::

   make font oblique: \q Test \Q
   greek: use \x w \B
   super: use \S letters \N
   sub:   use \s letters \N
   new line: \n

   Examples:
    F\sX\N(\xe\f{}) = sin(\xe\f{})\#{b7}e\S-X\N\#{b7}cos(\xe\f{})

   Partial derivative of energy with respect to lambda: \x\c6\CE/\c6\C\xl
   Infinity symbol: \x\c%
   Angstrom: \cE\C
   not equal symbol ≠ : \x\c9\C\f{}
   plus-minus sign ±:   \x\c1\C\f{}

**Crop xmgrace plot**

 A snippet how to convert a bunch of .agr files to cropped pdf for publication.::


    import os
    import glob

    # print to ps and convert to pdf
    path='./'
    for infile in glob.glob( os.path.join(path, '*.agr') ):
        os.system('xmgrace -hdevice PostScript -hardcopy -printfile '+infile[:-4]+'.ps '+infile)
        os.system('ps2pdf '+infile[:-4]+'.ps')
        os.system('pdfcrop '+infile[:-4]+'.pdf')

    #with pdf printer installed
    path='./'
    for infile in glob.glob( os.path.join(path, '*.agr') ):
        os.system('xmgrace -hdevice PDF -hardcopy -printfile '+infile[:-4]+'.pdf '+infile)
        os.system('pdfcrop '+infile[:-4]+'.pdf')


