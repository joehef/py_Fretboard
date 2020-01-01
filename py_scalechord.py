# -*- coding: utf-8 -*-
"""

@author: H Josiah Raj
2011
"""
import numpy as np
dict_notesnum={'C':1,'C#':2,'Db':2,'D':3,'D#':4,'Eb':4,
            'E':5,'F':6,'F#':7,'Gb':7,
            'G':8,'G#':9,'Ab':9,
            'A':10,'A#':11,'Bb':11,'B':12}
dict_numnotes = {1: 'C', 2: 'C#', 3: 'D', 4: 'D#', 5: 'E', 6: 'F',
                 7: 'F#', 8: 'G', 9: 'G#', 10: 'A', 11: 'A#', 12: 'B'}
dict_numita = {1: 'Do', 2: 'Do#', 3: 'Re', 4: 'Re#', 5: 'Mi', 6: 'Fa',
                 7: 'Fa#', 8: 'Sol', 9: 'Sol#', 10: 'La', 11: 'La#', 12: 'Si'}

dict_tunings={
            'Guitar_EADGBE': (5,10,3,8,12,5),
            'Guitar_OpenD_DADF#AD':(3,10,3,7,10,3),
            'Guitar_OpenG_DGDGBD':(3,8,3,8,12,3),
            'Guitar_DropD_DADGBE':(3,10,3,8,12,5),
            'Guitar_Celtic_DADGAD':(3,10,3,8,10,3),
            'Mandolin_GDAE':(8,3,10,5),
            'Mandola_CGDA':(1,8,3,10),
            'IrishBouzouki_GDAD':(8,3,10,3),
            'GreekLute_DGDA':(3,8,3,10),
}
dict_chordquality={
            'Maj':(1,5,8),'min':(1,4,8),
            '7th':(1,5,8,11),'9th':(1,3,5,8,11),'11th':(1,3,5,6,8,11),'13th':(1,5,10,11),
            'm6':(1,4,8,10),'min7th':(1,4,8,11),'m9':(1,3,4,11),'m11':(1,4,6,8,11),'m13':(1,4,8,10,11),
            '6th':(1,5,8,10),'Maj7th':(1,5,8,12),'Maj9':(1,3,5,8,12),'Maj13':(1,3,5,8,10,12),
            '+':(1,5,9),'dim':(1,4,7,10),'sus4':(1,6,8),'sus2':(1,3,8),'dim7':(1,4,7,10),
            '7+':(1,5,9,11),'9sus4':(1,3,6,8,11),'9+':(1,3,5,9,11),'7sus4':(1,6,8,11),
            'add9':(1,3,5,8),'m(add9)':(1,3,4,8),
            '6/9':(1,3,5,10),'7#9':(1,4,5,8,11),
            '7b5':(1,5,7,11),'m7b5':(1,4,7,11),
            '7b9':(1,2,5,8,11),'9b5':(1,3,5,7,11),
            '2,#4':(1,3,7),'2, 4':(1,3,6)          
            }

'''dict_scales={
            'Major': (1,3,5,6,8,10,12),
            'Minor': (1,3,4,....),
            'Pentatonic': (1,3,6,8,10),
            'Romanian': (1,3,4,7,8,10,11),
            'HungarianMajor': (1,4,5,7,8,10,11),
            'Persian': (1,2,5,6,7,9,12),
            'Enigmatic': (1,2,5,7,9,11,12),
            'Major': (1,3,5,6,8,10,12),


}'''

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
    def __init__(self,fret_tup,tune_tup,scale_tup):
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
        stune=''
        nst=0
        for st in tune_tup:
            nst+=1
            stemp=dict_numnotes[st]
            stune+=stemp
            litemp=[]
            litemp2=[]
            for fr in range(fretstart):
                itemp=st+fr
                litemp.append(itemp) # the complete integer fretboard will have all the notes
                litemp2.append(' ')# ignore frets till starting fret
            for fr in range(fretstart,fretlast+1):
                itemp=st+fr
                while itemp>12:
                    itemp-=12
                litemp.append(itemp)
                if itemp in scale_tup:
                    litemp2.append(dict_numnotes[itemp])
                else:
                    litemp2.append(' ')
                    
            dict_fretb[nst]=litemp
            dict_fretb2[str(nst)+'_'+stemp]=litemp2   
        self.tuning=stune
        self.fretboard=dict_fretb2
        self.numboard=dict_fretb
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
            
            
        
        