# -*- coding: utf-8 -*-
"""

@author: H Josiah Raj
2011
"""
from collections import defaultdict
from data_sc import *

def validate_stune(strtune):
    #first replace the double letter strings
    for k,v in dict_notesnum.items():
        if len(k)==2:
            strtune=strtune.replace(k,'')
    for k,v in dict_notesnum.items():
        if len(k)==1:
            strtune=strtune.replace(k,'')
    if len(strtune)==0:
        return True
    else:
        return False  
    
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
        dict_plotdata_open['label'].append('')
        dict_plotdata_open['fret'].append(-0.9)
        dict_plotdata_open['string'].append(self.nstrings +1)# to add space on the right
        #if len(dict_plotdata_open)==0:# blank data error fix
            #dict_plotdata_open={'label':[], 'fret':[], 'string':[]}
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
        #title='Root = {} ; '.format(dict_numnotes[tpose+1])+title
        #title+='\n Tuning : {} , Active frets : {}=>{}'.format(self.tuning,self.fretstart,self.fretlast)
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
                    title=self.title,y_range=(self.fretlast+0.5,self.fretstart-0.8))
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
        p.xgrid.visible = False
        p.ygrid.visible = False
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
            
def bokgrid(pgrid,nhtml=False, hname=''):
    '''
    pgrid= [[p1, p2], [None, p3]]
    '''
    from bokeh.io import show
    from bokeh.layouts import gridplot
    if nhtml:
        from bokeh.io import output_file
        output_file("fb_{}.html".format(hname))
    else:
        from bokeh.io import output_notebook
        output_notebook()
    # make a grid
    grid = gridplot(pgrid)
    # show the results
    show(grid) 


if __name__ == '__main__':
    # tkinter imports
    from tkinter import messagebox, Entry, Label, LabelFrame, Button, Tk, END
    from tkinter.ttk import Combobox
    from PIL import ImageTk, Image
    '''
    ********************* Bokeh Tkinter connecting section ******************
    '''
    def tk2bok(dict_vals):
        '''
        dict_vals.keys =['title',
                         'tune_cb','tune_ent',
                         'fret1_cb','fret2_cb',
                          'scorchor','sc_cat',
                          
                          'desc',
                         'root1','sq1',
                         'root2','sq2',
                         'root3','sq3']
        '''
        dtup={}
        # CHECK TUNING
        if validate_stune(dict_vals['tune_ent'])==False:
            # message box display
            messagebox.showerror("Custom tuning invalid", 
                                 "{} will be used instead".format(dict_tunings[dict_vals['tune_cb']]))
            dict_vals['tune_ent']=dict_vals['tune_cb'].split('_')[0] # Eg DADF#AD_OpenD_Guitar
        if dict_vals['title']=="":
            stitle='Tuning={}, '.format(dict_vals['tune_ent'])
        else:
            stitle=dict_vals['title']+ ', Tuning={}, '.format(dict_vals['tune_ent'])
        dtup['title']=stitle
        dtup['tun']=stune_2tup(dict_vals['tune_ent'])
        
        #------Frets check
        for k in ['fret1_cb','fret2_cb']:
            dict_vals[k]=int(dict_vals[k])
        if dict_vals['fret1_cb']>dict_vals['fret2_cb']-2:
            dict_vals['fret2_cb']=dict_vals['fret1_cb']+3
        dtup['fr']=(dict_vals['fret1_cb'],dict_vals['fret2_cb'])
        dtup['tpose']=dict_notesnum[dict_vals['root1']]-1
        # dict_definitions 1st level keys ='scales' or chords    : dict_vals['scorchor']
        # 2nd level keys = categories Eg  w_western, mr_melakarta, jr_janya
        # 3rd level keys = scale names Eg  'mr21_Keeravani' 'w007_Dorian_mode'
        # 4th level keys = asc/ desc /melakarta / melakarta_num
        if dict_vals["scorchor"] == "scales":
            temp_scale_dict=dict_definitions['scales'][dict_vals['sc_cat']][dict_vals['sq1']]
            dtup['sq']=temp_scale_dict['asc']
            title_full=dict_vals['title']+'_'+dict_vals['root1']+'_' +dict_vals['sc_cat'].split('_')[1]+'_'
            title_full+=dict_vals['sq1'].split('_',1)[1] +'; Tuning=' +dict_vals['tune_ent']
            fretbod1=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq'],dtup['tpose'],title_full)
            if ('desc' in temp_scale_dict.keys()) and (dict_vals['desc']=='desc'):
                dtup['sq2']=temp_scale_dict['desc']
                title_full=dict_vals['title']+'_'+dict_vals['root1']+'_Desc_' +dict_vals['sc_cat'].split('_')[1]+'_'
                title_full+=dict_vals['sq1'].split('_',1)[1] +'; Tuning=' +dict_vals['tune_ent']
                fretbod2=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq2'],dtup['tpose'],title_full)
                bokgrid([[fretbod1.bok(450,650),fretbod2.bok(450,650)]],True,dict_vals['title'])
            else:
                if dict_vals['sq2']=='':
                    bokgrid([[fretbod1.bok(550,750)]],True,dict_vals['title'])
                else:
                    dtup['tpose2']=dict_notesnum[dict_vals['root2']]-1
                    temp_scale_dict=dict_definitions['scales'][dict_vals['sc_cat']][dict_vals['sq2']]
                    dtup['sq2']=temp_scale_dict['asc']
                    title_full=dict_vals['title']+'_'+dict_vals['root2']+'_' +dict_vals['sc_cat'].split('_')[1]+'_'
                    title_full+=dict_vals['sq2'].split('_',1)[1] +'; Tuning=' + dict_vals['tune_ent']
                    fretbod2=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq2'],dtup['tpose2'],title_full)
                    bokgrid([[fretbod1.bok(450,650),fretbod2.bok(450,650)]],True,dict_vals['title'])
        if dict_vals["scorchor"] == "chords": # chords
            # 2nd level keys = categories Eg  common, quality
            # 3rd level keys = quality Eg  'Maj' 'm', 'm7'
            dtup['sq']=dict_definitions['chords'][dict_vals['sc_cat']][dict_vals['sq1']]
            title_full=dict_vals['title']+'_'+dict_vals['root1']+' '+dict_vals['sq1'] +'; Tuning='
            title_full+=dict_vals['tune_ent']
            fretbod1=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq'],dtup['tpose'],title_full)
            if (dict_vals['sq2']=='') & (dict_vals['sq3']==''):
                bokgrid([[fretbod1.bok(550,750)]],True,dict_vals['title'])
            elif (dict_vals['sq2']!='') & (dict_vals['sq3']==''):
                dtup['tpose2']=dict_notesnum[dict_vals['root2']]-1
                dtup['sq2']=dict_definitions['chords'][dict_vals['sc_cat']][dict_vals['sq2']]
                title_full=dict_vals['title']+'_'+dict_vals['root2']+' '+dict_vals['sq2'] +'; Tuning='
                title_full+=dict_vals['tune_ent']
                fretbod2=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq2'],dtup['tpose2'],title_full)
                bokgrid([[fretbod1.bok(450,650),fretbod2.bok(450,650)]],True,dict_vals['title'])
            elif (dict_vals['sq2']=='') & (dict_vals['sq3']!=''):
                dtup['tpose3']=dict_notesnum[dict_vals['root3']]-1
                dtup['sq3']=dict_definitions['chords'][dict_vals['sc_cat']][dict_vals['sq3']]
                title_full=dict_vals['title']+'_'+dict_vals['root3']+' '+dict_vals['sq3'] +'; Tuning='
                title_full+=dict_vals['tune_ent']
                fretbod3=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq3'],dtup['tpose3'],title_full)
                bokgrid([[fretbod1.bok(450,650),fretbod3.bok(450,650)]],True,dict_vals['title'])
            else:
                dtup['tpose2']=dict_notesnum[dict_vals['root2']]-1
                dtup['sq2']=dict_definitions['chords'][dict_vals['sc_cat']][dict_vals['sq2']]
                title_full=dict_vals['title']+'_'+dict_vals['root2']+' '+dict_vals['sq2'] +'; Tuning='
                title_full+=dict_vals['tune_ent']
                fretbod2=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq2'],dtup['tpose2'],title_full)
                # # 3
                dtup['tpose3']=dict_notesnum[dict_vals['root3']]-1
                dtup['sq3']=dict_definitions['chords'][dict_vals['sc_cat']][dict_vals['sq3']]
                title_full=dict_vals['title']+'_'+dict_vals['root3']+' '+dict_vals['sq3'] +'; Tuning='
                title_full+=dict_vals['tune_ent']
                fretbod3=cl_fretb(dtup['fr'],dtup['tun'],dtup['sq3'],dtup['tpose3'],title_full)
                bokgrid([[fretbod1.bok(300,500),fretbod2.bok(300,500),fretbod3.bok(300,500)]],True,dict_vals['title'])
    
    
    '''
    ********************* TKinter section **********************************
    '''
    
    f='Courier 13 bold' #Arial
    f2='Arial 11' # normal
    fsm='Arial 9 italic' # normal
    f3='Arial 13 bold' #
    #♣label formatting
    px,py=5,5   
    cdw=15
    
    my_window = Tk()
    '''
    class tab_frame(LabelFrame):
        def __init__(self, parent,fbnum,sinfo,cblist=['desc','ignore desc'], 
                     *args, **kwargs):
            LabelFrame.__init__(self, parent)
            self.fretB=fbnum
            lab=Label(self,text='Fretboard # {}'.format(fbnum))
            lab.grid(column=0, row=0)
            #♠ row 4-3
            lab_cinf=Label(my_window, text=sinfo,font=fsm)
            lab_cinf.grid(row=1,column=0,padx=px, pady=py)
            # row 5-3
            if isinstance(cblist,list):
                cb_desc=Combobox(width=cdw,values = cblist,font=f)
                cb_desc.grid(row=2,column=1,padx=px, pady=py)
                cb_desc.current(0) # selects the first value as default
                cb_desc.event_generate("<<ComboboxSelect>>") # works with the prev line
            else:
                lab_desc=Label(my_window, text=' ',font=f)
                lab_desc.grid(row=2,column=0,padx=px, pady=py)
            
            # row 6-3 Labels
            lab_r=Label(my_window, text='Root',font=f2)
            lab_r.grid(row=3,column=0,padx=px, pady=py)       
            # row 7-3 cb root notes
            liscales=[v for k,v in dict_numnotes.items()]
            cb_r=Combobox(width=cdw,values = liscales,font=f)
            cb_r.grid(row=4,column=0,padx=px, pady=py)
            cb_r.current(0) # selects the first value as default
            cb_r.event_generate("<<ComboboxSelect>>") # works with the prev line
            # row 8-3 Labels
            t='Scale / Quality'
            lab_sc=Label(my_window, text=t,font=f2)
            lab_sc.grid(row=5,column=0,padx=px, pady=py)
    
            # row 9 cb scale
            liscales=['c','temp']
            cb_sc=Combobox(width=cdw,values = liscales,font=f)
            cb_sc.grid(row=6,column=0,padx=px, pady=py)
    
    
        def getvals(self):
            vals={}
    
            return vals
            #print(vals)
        '''
    # geometry width x height + xposition +yposition
    my_window.geometry('580x510+200+200')
    
    # row 0
    lab_title=Label(my_window, text='Title',font=f)
    lab_title.grid(row=0,column=0,padx=px, pady=py)
    en_title=Entry(my_window,width=cdw*2+5,font=f)
    en_title.grid(row=0,column=1,columnspan=2,padx=px, pady=py)
    # row 1 Tuning
    lab_tune=Label(my_window, text='Tuning',font=f)
    lab_tune.grid(row=1,column=0,padx=px, pady=py)
    cb_tune=Combobox(width=cdw,values = list(dict_tunings.keys()),font=f)
    cb_tune.grid(row=1,column=1,padx=px, pady=py)
    en_tune=Entry(my_window,width=cdw+2,font=f)
    en_tune.grid(row=1,column=2,padx=px, pady=py)
    def UpdTuning(event):
        en_tune.delete(0, END)
        en_tune.insert(0, cb_tune.get().split('_')[0])
    cb_tune.bind("<<ComboboxSelected>>",UpdTuning)
    cb_tune.current(0) # selects the first value as default
    cb_tune.event_generate("<<ComboboxSelected>>")# works with the previous line
    # frets row 2
    ro=2
    lifret=[i for i in range(16)]
    lab_fret=Label(my_window, text='Frets start - end',font=f)
    lab_fret.grid(row=ro,column=0,padx=px, pady=py)
    cb_fr1=Combobox(width=cdw,values = lifret,font=f)
    cb_fr1.grid(row=ro,column=1,padx=px, pady=py)
    cb_fr1.current(0) # selects the first value as default
    cb_fr1.event_generate("<<ComboboxSelect>>") # works with the prev line
    cb_fr2=Combobox(width=cdw,values = lifret,font=f)
    cb_fr2.grid(row=ro,column=2,padx=px, pady=py)
    cb_fr2.current(7) # selects the 8 as default
    cb_fr2.event_generate("<<ComboboxSelect>>") # works with the prev line
    
    
    # row 10 cb scale
    ro=10
    cb_sq1=Combobox(width=cdw,font=f)
    cb_sq1.grid(row=ro,column=0,padx=px, pady=py)
    cb_sq2=Combobox(width=cdw,font=f)
    cb_sq2.grid(row=ro,column=1,padx=px, pady=py)
    cb_sq3=Combobox(width=cdw,font=f)
    cb_sq3.grid(row=ro,column=2,padx=px, pady=py)
    # ro=3
    ro=3
    lab_scachor=Label(my_window, text='Scales or Chords',font=f)
    lab_scachor.grid(row=ro,column=0,padx=px, pady=py)
    #category
    cb_cat=Combobox(width=cdw,font=f)
    cb_cat.grid(row=ro,column=2,padx=px, pady=py)
    def UpdscalesNames(event):
        sc=cb_scachor.get()
        cat=cb_cat.get()
        liscales=list(dict_definitions[sc][cat].keys())
        cb_sq1['values'] = liscales
        cb_sq1.current(0) # selects the first value as default
        cb_sq1.event_generate("<<ComboboxSelected>>") # works with the prev line
        cb_sq2['values'] = liscales
        cb_sq3['values'] = liscales
    cb_cat.bind('<<ComboboxSelected>>',UpdscalesNames) 
    cb_scachor=Combobox(width=cdw,values = ['scales','chords'],font=f)
    cb_scachor.grid(row=ro,column=1,padx=px, pady=py)
    def UpdCategory(event):
        cb_cat['values'] = list(dict_definitions[cb_scachor.get()].keys())
        cb_cat.current(0) # selects the first value as default
        cb_cat.event_generate("<<ComboboxSelected>>")# works with the previous line
    
    cb_scachor.bind('<<ComboboxSelected>>',UpdCategory) 
    cb_scachor.current(0) # selects the first value as default
    cb_scachor.event_generate("<<ComboboxSelected>>") # works with the prev line
    
    
    
    '''
    fbnum=1
    sinfo=' '
    cblist=' '
    fram1=tab_frame(my_window,fbnum,sinfo,cblist)
    fram1.grid(row=3,column=fbnum-1)
    #
    fbnum=2
    sinfo='Use desc for viewing Descending'
    cblist=['desc','ignore desc']
    fram1=tab_frame(my_window,fbnum,sinfo,cblist)
    fram1.grid(row=3,column=fbnum-1)
    # 3
    fbnum=3
    sinfo='works for chords only'
    cblist=' '
    fram1=tab_frame(my_window,fbnum,sinfo,cblist)
    fram1.grid(row=3,column=fbnum-1)
    '''
    #  Labels
    ro=4
    lab_fb=Label(my_window, text='FBoard 1',font=f)
    lab_fb.grid(row=ro,column=0,padx=px, pady=py)
    lab_fb2=Label(my_window, text='FBoard 2',font=f)
    lab_fb2.grid(row=ro,column=1,padx=px, pady=py)
    lab_fb3=Label(my_window, text='FBoard 3',font=f)
    lab_fb3.grid(row=ro,column=2,padx=px, pady=py)
    
    #♠ row 5
    ro=5
    lab_c2inf=Label(my_window, text='Use desc for viewing Descending',font=fsm)
    lab_c2inf.grid(row=ro,column=1,padx=px, pady=py)
    lab_c3inf=Label(my_window, text='works for chords only',font=fsm)
    lab_c3inf.grid(row=ro,column=2,padx=px, pady=py)
    # row 6
    ro=6
    cb_desc=Combobox(width=cdw,values = ['desc','ignore desc'],font=f)
    cb_desc.grid(row=ro,column=1,padx=px, pady=py)
    cb_desc.current(0) # selects the first value as default
    cb_desc.event_generate("<<ComboboxSelect>>") # works with the prev line
    
    #  Labels
    ro=7
    lab_r=Label(my_window, text='Root',font=f2)
    lab_r.grid(row=ro,column=0,padx=px, pady=py)
    lab_r2=Label(my_window, text='Root',font=f2)
    lab_r2.grid(row=ro,column=1,padx=px, pady=py)
    lab_r3=Label(my_window, text='Root',font=f2)
    lab_r3.grid(row=ro,column=2,padx=px, pady=py)
    
    
    # row 8 cb root notes
    ro=8
    liscales=[v for k,v in dict_numnotes.items()]
    cb_r1=Combobox(width=cdw,values = liscales,font=f)
    cb_r1.grid(row=ro,column=0,padx=px, pady=py)
    cb_r1.current(0) # selects the first value as default
    cb_r1.event_generate("<<ComboboxSelect>>") # works with the prev line
    cb_r2=Combobox(width=cdw,values = liscales,font=f)
    cb_r2.grid(row=ro,column=1,padx=px, pady=py)
    cb_r2.current(0) # selects the first value as default
    cb_r2.event_generate("<<ComboboxSelect>>") # works with the prev line
    cb_r3=Combobox(width=cdw,values = liscales,font=f)
    cb_r3.grid(row=ro,column=2,padx=px, pady=py)
    cb_r3.current(0) # selects the first value as default
    cb_r3.event_generate("<<ComboboxSelect>>") # works with the prev line
    # row 9 Labels
    ro=9
    t='Scale / Quality'
    lab_sq=Label(my_window, text=t,font=f2)
    lab_sq.grid(row=ro,column=0,padx=px, pady=py)
    lab_sq2=Label(my_window, text=t,font=f2)
    lab_sq2.grid(row=ro,column=1,padx=px, pady=py)
    lab_sq3=Label(my_window, text=t,font=f2)
    lab_sq3.grid(row=ro,column=2,padx=px, pady=py)
    def get_vals():
        dict_vals={}
        dict_vals['title']=en_title.get()
        dict_vals['tune_cb']=cb_tune.get()
        dict_vals['tune_ent']=en_tune.get()
        dict_vals['fret1_cb']=cb_fr1.get()
        dict_vals['fret2_cb']=cb_fr2.get()
        dict_vals['scorchor']=cb_scachor.get()
        dict_vals['sc_cat']=cb_cat.get()
        dict_vals['desc']=cb_desc.get()
        dict_vals['root1']=cb_r1.get()
        dict_vals['sq1']=cb_sq1.get()
        dict_vals['root2']=cb_r2.get()
        dict_vals['sq2']=cb_sq2.get()
        dict_vals['root3']=cb_r3.get()
        dict_vals['sq3']=cb_sq3.get()
        tk2bok(dict_vals)
        print(dict_vals)
        
        
    
    #buttons
    ro=12
    but_1=Button(my_window,
               borderwidth=2,
               text='Close',
               font=f3,
               padx=11, pady=2,
               command=my_window.destroy)
    
    but_1.grid(row=ro,column=0)
    but_2=Button(my_window,
               borderwidth=2,
               text='Show',
               font=f3,
               padx=10, pady=2,
               command=get_vals)
    
    but_2.grid(row=ro,column=1)
    #lab_t=Label(my_window, text=' ',font=f2)
    #lab_t.grid(row=10,column=1,padx=px, pady=py)
    img = ImageTk.PhotoImage(Image.open("jh100.png"))
    imglabel=Label(my_window,image=img)
    imglabel.grid(row=11,column=2, rowspan=2)
    # title
    my_window.title('My Fretboard')
    #entry_1.focus()
    my_window.mainloop()