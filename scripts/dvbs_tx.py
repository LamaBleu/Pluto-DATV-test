#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbs Tx
# Generated: Tue Nov 20 18:20:16 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import trellis
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import dvbs
import os
import wx


class dvbs_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Dvbs Tx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1000000
        self.username = username = os.environ.get('USER')
        self.samp_rate = samp_rate = symbol_rate * 2
        self.rrc_taps = rrc_taps = 20
        self.frequency = frequency = 970e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.trellis_encoder_xx_0 =  trellis.encoder_bb(trellis.fsm(1, 2, (0171, 0133)), 0, 0) if False else trellis.encoder_bb(trellis.fsm(1, 2, (0171, 0133)), 0) 
        self._symbol_rate_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.symbol_rate,
        	callback=self.set_symbol_rate,
        	label='symbol_rate',
        	choices=[333000,500000,1000000,1200000, 1500000],
        	labels=["333kS/s","500 kS/s","1000kS/s","1200kS/s","1500kS/s"],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._symbol_rate_chooser)
        self.pluto_sink_0 = iio.pluto_sink('', int(frequency), int(samp_rate), int(9000000), 0x8000, False, 0.0, '', True)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.root_raised_cosine(1.79, samp_rate, samp_rate/2, 0.35, rrc_taps)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.dvbs_reed_solomon_enc_bb_0 = dvbs.reed_solomon_enc_bb()
        self.dvbs_randomizer_bb_0 = dvbs.randomizer_bb()
        self.dvbs_puncture_bb_0 = dvbs.puncture_bb(dvbs.C1_2)
        self.dvbs_modulator_bc_0 = dvbs.modulator_bc()
        self.dvbs_interleaver_bb_0 = dvbs.interleaver_bb()
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(2)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_char*1, "/media/" + username + "/PlutoSDR/MPEG2-lalinea.ts", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_1, 0), (self.dvbs_randomizer_bb_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.dvbs_modulator_bc_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.trellis_encoder_xx_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.dvbs_puncture_bb_0, 0))    
        self.connect((self.dvbs_interleaver_bb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.dvbs_modulator_bc_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.dvbs_puncture_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))    
        self.connect((self.dvbs_randomizer_bb_0, 0), (self.dvbs_reed_solomon_enc_bb_0, 0))    
        self.connect((self.dvbs_reed_solomon_enc_bb_0, 0), (self.dvbs_interleaver_bb_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.pluto_sink_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.trellis_encoder_xx_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))    

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate * 2)
        self._symbol_rate_chooser.set_value(self.symbol_rate)

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username
        self.blocks_file_source_1.open("/media/" + self.username + "/PlutoSDR/MPEG2-lalinea.ts", True)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.pluto_sink_0.set_params(int(self.frequency), int(self.samp_rate), int(9000000), 0.0, '', True)
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(1.79, self.samp_rate, self.samp_rate/2, 0.35, self.rrc_taps)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(1.79, self.samp_rate, self.samp_rate/2, 0.35, self.rrc_taps)))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency)
        self.pluto_sink_0.set_params(int(self.frequency), int(self.samp_rate), int(9000000), 0.0, '', True)


def main(top_block_cls=dvbs_tx, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
