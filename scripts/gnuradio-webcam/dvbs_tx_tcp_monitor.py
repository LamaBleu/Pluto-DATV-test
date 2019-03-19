#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbs Tx Tcp Monitor
# Generated: Tue Mar 19 18:07:17 2019
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
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import fec
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
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import os
import wx


class dvbs_tx_tcp_monitor(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Dvbs Tx Tcp Monitor")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1000000
        self.samp_rate = samp_rate = symbol_rate * 2
        self.rrc_taps = rrc_taps = 100
        self.frequency = frequency = 970000000

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
        	avg_alpha=0.13333,
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
        	choices=[250000,333000,500000,1000000,1200000, 1500000],
        	labels=["250kS/s","333kS/s","500 kS/s","1000kS/s","1200kS/s","1500kS/s"],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._symbol_rate_chooser)
        self.pluto_sink_0 = iio.pluto_sink('', int(frequency), int(samp_rate), int(20000000), 0x8000, False, 5.0, '', True)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.root_raised_cosine(1.0, samp_rate, samp_rate/2, 0.35, rrc_taps)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.fec_puncture_xx_0 = fec.puncture_bb(14, 0b11010101100110, 0)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 8)
        self.dtv_dvbt_energy_dispersal_0 = dtv.dvbt_energy_dispersal(1)
        self.dtv_dvbt_convolutional_interleaver_0 = dtv.dvbt_convolutional_interleaver(136, 12, 17)
        self.dtv_dvbs2_modulator_bc_0 = dtv.dvbs2_modulator_bc(dtv.FECFRAME_NORMAL,
        dtv.C5_6, dtv.MOD_QPSK, dtv.INTERPOLATION_ON)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_char*1, '127.0.0.1', 58000, 1472, False)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(2)
        self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
        	itemsize=gr.sizeof_char*1,
        	addr='0.0.0.0',
        	port=57000,
        	server=True,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.dtv_dvbs2_modulator_bc_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.trellis_encoder_xx_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blks2_tcp_sink_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.dtv_dvbt_energy_dispersal_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.fec_puncture_xx_0, 0))    
        self.connect((self.dtv_dvbs2_modulator_bc_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.dtv_dvbt_convolutional_interleaver_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.dtv_dvbt_energy_dispersal_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))    
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.dtv_dvbt_convolutional_interleaver_0, 0))    
        self.connect((self.fec_puncture_xx_0, 0), (self.blocks_pack_k_bits_bb_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.pluto_sink_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.trellis_encoder_xx_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))    

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate * 2)
        self._symbol_rate_chooser.set_value(self.symbol_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.pluto_sink_0.set_params(int(self.frequency), int(self.samp_rate), int(20000000), 5.0, '', True)
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(1.0, self.samp_rate, self.samp_rate/2, 0.35, self.rrc_taps)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(1.0, self.samp_rate, self.samp_rate/2, 0.35, self.rrc_taps)))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency)
        self.pluto_sink_0.set_params(int(self.frequency), int(self.samp_rate), int(20000000), 5.0, '', True)


def main(top_block_cls=dvbs_tx_tcp_monitor, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
