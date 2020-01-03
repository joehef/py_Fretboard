# -*- coding: utf-8 -*-
"""

@author: H Josiah Raj
2011
"""
import numpy as np
from collections import defaultdict
from data_sc import *


def stune_2tup(strtune):
    '''
    "C#CEGbB" => (2,1,5,7,12)
    IMPORTANT the sharp(#) and the flat(b) symbols should be typed after the Note Letters
    The Notes should be in upper case
    the flat symbol is lower case
    uses
    dict_notesnum={'C':1,'C#':2,'Db':2,'D':3,'D#':4,'Eb':4,
            'E':5,'F':6,'F#':7,'Gb':7,
            'G':8,'G#':9,'Ab':9,
            'A':10,'A#':11,'Bb':11,'B':12}
    '''
    #first replace the double letter strings
    for k,v in dict_notesnum.items():
        if len(k)==2:
            strtune=strtune.replace(k,str(v)+'-')
    for k,v in dict_notesnum.items():
        if len(k)==1:
            strtune=strtune.replace(k,str(v)+'-')
    strtune=strtune[:-1]# as last char would be '-'
    return tuple([int(sn) for sn in strtune.split('-')])


class cl_fretb():
    ''' 
    Example
        chosca=cl_fretb(fret_tup=(0,5),
                        tune_tup=(8,3,10,5),
                        scale_tup=(1,3,5,6,8,10,12))
        chosca.print_fret()
            chosca.tuning >>'GDAE'
            chosca.fretstart,chosca.fretlast >> 1st and 2nd elements from fret_tup
            chosca.nstrings >> number of strings of our instrument
            chosca.fretboard >> a dictionary with strings as keys 
                                the notes which can be played as string types in the fret position
                                frets to be ignored have blank spaces in them
            chosca.numboard  >> a dictionary with note code numbers from which the fretboard was calculated
                                Useful only in the beginning till the code is tested        
    '''
    def __init__(self,fret_tup,tune_tup,scale_tup_untpose,tpose=0,title=''):
        iroot=tpose+1
        # transpose the scale or chord
        li=[]
        for ele in scale_tup_untpose:
            el=ele+tpose
            while el>12:
                el-=12
            li.append(el)
        scale_tup=tuple(li)  
        # tuning tuple if it is a string
        if isinstance(tune_tup,str):
            tune_tup=stune_2tup(tune_tup) # convert to a tuple containing integers
        #----FRETs 
        nut=0.07
        finger=0.4
        if isinstance(fret_tup,int):
            fret_tup=(0,fret_tup)
        fretstart,fretlast=fret_tup
        istrings=len(tune_tup)
        self.nstrings=istrings
        self.fretstart=fretstart
        self.fretlast=fretlast
        # fretboard
        dict_fretb={}
        dict_fretb2={}
        dict_plotdata = defaultdict(list)
        dict_plotdata_open = defaultdict(list)
        dict_plotdata_root=defaultdict(list)# only for plot highlight # labelling data is in other dicts
        fret_dict=defaultdict(list)
        li_plotstrings=[]
        stune=''
        nst=0
        for st in tune_tup:
            nst+=1
            li_plotstrings.append(((nst,nst),(fretstart-nut,fretlast)))
            stemp=dict_numnotes[st]
            stune+=stemp
            litemp=[]
            litemp2=[]
            for fr in range(fretstart):
                itemp=st+fr
                litemp.append(itemp) # the complete integer fretboard will have all the notes
                litemp2.append(' ')# ignore frets till starting fret
            for fr in range(fretstart,fretlast+1):
                if fr>0:
                    fret_dict['label'].append(str(fr))
                    fret_dict['fret'].append(fr)
                    fret_dict['string'].append(0.7)
                itemp=st+fr
                while itemp>12:
                    itemp-=12
                litemp.append(itemp)
                if itemp in scale_tup:
                    litemp2.append(dict_numnotes[itemp])
                    
                    if fr==0:
                        dict_plotdata_open['label'].append(dict_numnotes[itemp])
                        dict_plotdata_open['fret'].append(fr)
                        dict_plotdata_open['string'].append(nst)
                        if itemp==iroot:# for highlighting root notes
                            dict_plotdata_root['label'].append('')
                            dict_plotdata_root['fret'].append(fr)
                            dict_plotdata_root['string'].append(nst)
                    else:
                        dict_plotdata['label'].append(dict_numnotes[itemp])
                        dict_plotdata['fret'].append(fr-finger)
                        dict_plotdata['string'].append(nst)
                        if itemp==iroot:# for highlighting root notes
                            dict_plotdata_root['label'].append('')
                            dict_plotdata_root['fret'].append(fr-finger)
                            dict_plotdata_root['string'].append(nst)
                else:
                    litemp2.append(' ')
                    
            dict_fretb[nst]=litemp
            dict_fretb2[str(nst)+'_'+stemp]=litemp2   

        self.tuning=stune
        self.fretboard=dict_fretb2
        self.numboard=dict_fretb
        # Open notes and fret labels
        if len(dict_plotdata_open)==0:# blank data error fix
            dict_plotdata_open={'label':[], 'fret':[], 'string':[]}
        self.plot_pzero={'notes_open':dict_plotdata_open,'frets':fret_dict}
        # notes to be played
        if len(dict_plotdata)==0:# blank data error fix
            dict_plotdata={'label':[], 'fret':[], 'string':[]}
         # root data
        if len(dict_plotdata_root)==0:
            dict_plotdata_root={'label':[], 'fret':[], 'string':[]}    
        #notes and root notes
        self.plot_p={'notes':dict_plotdata,'root':dict_plotdata_root}
       
        #
        li_plotfrets=[]
        fr=fretstart-nut
        li_plotfrets.append(((1,nst),(fr,fr)))
        for fr in range(fretstart,fretlast+1):
            li_plotfrets.append(((1,nst),(fr,fr)))

        self.plot_lines={'strings':li_plotstrings,'frets':li_plotfrets}
        # TITLE
        title='Root = {} ; '.format(dict_numnotes[tpose+1])+title
        title+='\n Tuning : {} , Active frets : {}=>{}'.format(self.tuning,self.fretstart,self.fretlast)
        self.title=title
    def print_fret(self):
        
        print('Number of strings : ',self.nstrings)
        print('Tuning : ',self.tuning)
        print('Active Frets : {} to {}'.format(self.fretstart,self.fretlast))
        print('')
        
        for fr in range(self.fretlast+1):
            print(('---|'*(self.nstrings))+'---|')
            print(str(fr).zfill(2),end=' | ')
            for k,li in self.fretboard.items():
                print(li[fr],end=' | ')
            print('')
    def bok(self,w=400,h=600):
        '''
        doesn't plot but returns a bokeh plot object ready to be plotted
        '''
        from bokeh.plotting import figure
        from bokeh.models import ColumnDataSource, LabelSet, Label

        # grid lines : strings and frets
        dsty_line={'strings':{'lcolor':'#111111','lwidth':2},
                        'frets':{'lcolor':'#111111','lwidth':1}}
        p = figure(plot_width=w, plot_height=h,
                    title=self.title,y_range=(self.fretlast+0.5,self.fretstart-0.5))
        for pldata in ['strings','frets']:
            for st in self.plot_lines[pldata]:
                x,y=st
                p.line(x, y, 
                        line_color=dsty_line[pldata]['lcolor'],
                        line_width=dsty_line[pldata]['lwidth'])
        dict_bokmodel=defaultdict(dict) # for Bokeh.models.ColumnDataSource() & LabelSet()
        # points with point size zero
        dsty_pzero={'notes_open':{'size':0,'xoff':-5,'yoff':10},
                                'frets':{'size':0,'xoff':0,'yoff':-8}}
        for k,dicdata in self.plot_pzero.items(): # k='frets','notes_open'
            # dicdata keys: 'string','fret','label'
            dict_bokmodel['source'][k] = ColumnDataSource(data=dicdata)     
            p.scatter(x='string', y='fret', size=dsty_pzero[k]['size'], 
                    source=dict_bokmodel['source'][k])
            dict_bokmodel['labels'][k] = LabelSet(x='string', y='fret', text='label', level='glyph',
                        x_offset=dsty_pzero[k]['xoff'], y_offset=dsty_pzero[k]['yoff'], 
                        source=dict_bokmodel['source'][k], render_mode='canvas')
            p.add_layout(dict_bokmodel['labels'][k])
        # points self.plot_p=
        dsty_p={'notes':{'size':10,'xoff':7,'yoff':0,'col':'#009900','alf':0.99},
                'root':{'size':25,'xoff':7,'yoff':0,'col':'#66FF00','alf':0.1}}
        for k,dicdata in self.plot_p.items(): # 
            # dicdata keys: 'string','fret','label'
            dict_bokmodel['source'][k] = ColumnDataSource(data=dicdata)     
            p.scatter(x='string', y='fret', size=dsty_p[k]['size'], 
                    fill_color=dsty_p[k]['col'], fill_alpha=dsty_p[k]['alf'],
                    source=dict_bokmodel['source'][k])
            dict_bokmodel['labels'][k] = LabelSet(x='string', y='fret', text='label', level='glyph',
                        x_offset=dsty_p[k]['xoff'], y_offset=dsty_p[k]['yoff'], 
                        source=dict_bokmodel['source'][k], render_mode='canvas')
            p.add_layout(dict_bokmodel['labels'][k])
        p.xaxis.visible = False  
        p.yaxis.visible = False 
        return p
    def bokplot(self,w=400,h=600,nhtml=False):
        from bokeh.plotting import show
        p=self.bok(w,h)
        if nhtml:
            from bokeh.plotting import output_file
            output_file("output.html")
        else:
            from bokeh.plotting import output_notebook
            output_notebook()
        show(p)     
            
def bokgrid(pgrid,nhtml=False):
    '''
    pgrid= [[p1, p2], [None, p3]]
    '''
    from bokeh.io import show
    from bokeh.layouts import gridplot
    if nhtml:
        from bokeh.io import output_file
        output_file("output.html")
    else:
        from bokeh.io import output_notebook
        output_notebook()
    # make a grid
    grid = gridplot(pgrid)
    # show the results
    show(grid)     

'''
********************* TKinter section **********************************
'''
import tkinter as tk
f='Courier 13 bold' #Arial
#♣label formatting
px,py=5,5   
cdw=15
my_window = tk.Tk()

# geometry width x height + xposition +yposition
my_window.geometry('600x200+200+200')

# row 0
lab_title=tk.Label(my_window, text='Title',font=f)
lab_title.grid(row=0,column=0,padx=px, pady=py)
en_title=tk.Entry(my_window,width=cdw*2+5,font=f)
en_title.grid(row=0,column=1,columnspan=2,padx=px, pady=py)
# row 1
lab_scachor=tk.Label(my_window, text='Scales or Chords',font=f)
lab_scachor.grid(row=1,column=0,padx=px, pady=py)
cb_scachor=tk.ttk.Combobox(width=cdw,values = ['Scales [2]','Chords[3]'],font=f)
cb_scachor.grid(row=1,column=1,padx=px, pady=py)
cb_scachor.current(0) # selects the first value as default
cb_scachor.event_generate("<<ComboboxSelect>>") # works with the prev line

cb_sccat=tk.ttk.Combobox(width=cdw,values = ['Scales','Chords'],font=f)
cb_sccat.grid(row=1,column=2,padx=px, pady=py)
cb_sccat.current(0) # selects the first value as default
cb_sccat.event_generate("<<ComboboxSelect>>") # works with the prev line

# row 2
lab_tune=tk.Label(my_window, text='Tuning',font=f)
lab_tune.grid(row=2,column=0,padx=px, pady=py)
cb_tune=tk.ttk.Combobox(width=cdw,values = ['Scales','Chords'],font=f)
cb_tune.grid(row=2,column=1,padx=px, pady=py)
var1=tk.StringVar()
en_tune=tk.Entry(my_window,width=cdw*2+5,font=f)
en_tune.grid(row=2,column=2,padx=px, pady=py)


#Label 
but_1=tk.Button(my_window,
           borderwidth=2,
           text='Click for Hello',
           font='Arial 12 bold',
           padx=10,)
           #command=add_label)

but_1.grid(row=8,column=0)

# title
my_window.title('My Scaleboard')
#entry_1.focus()
my_window.mainloop()