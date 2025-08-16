#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class gfsk_test_graph(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "gfsk_test_graph")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            100, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [1, 8, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_MUELLER_AND_MULLER,
            2,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=2,
            sensitivity=1.0,
            bt=0.35,
            verbose=False,
            log=False,
            do_unpack=False)
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
            samples_per_symbol=2,
            sensitivity=1.0,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1, 1], 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0, 0, 0, 1, 1, 1, 0, 1, 1), True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 9, "packet_len")
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, 120)
        self.blocks_file_sink_5 = blocks.file_sink(gr.sizeof_float*1, 'tmp/chunks_to_symbols.dat', False)
        self.blocks_file_sink_5.set_unbuffered(True)
        self.blocks_file_sink_4_0_0_0 = blocks.file_sink(gr.sizeof_float*1, 'tmp/symbol_sink_output.data', False)
        self.blocks_file_sink_4_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_4_0_0 = blocks.file_sink(gr.sizeof_float*1, 'tmp/quadrature_demod_output.data', False)
        self.blocks_file_sink_4_0_0.set_unbuffered(True)
        self.blocks_file_sink_4_0 = blocks.file_sink(gr.sizeof_char*1, 'tmp/gfsk_demod_custom.data', False)
        self.blocks_file_sink_4_0.set_unbuffered(True)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_char*1, 'tmp/gfsk_demod.data', False)
        self.blocks_file_sink_4.set_unbuffered(True)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_gr_complex*1, 'tmp/gfsk_mod.dat', False)
        self.blocks_file_sink_3.set_unbuffered(True)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_char*1, 'tmp/throttle.dat', False)
        self.blocks_file_sink_2.set_unbuffered(True)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, 'tmp/stream_to_tagged_stream_data.dat', False)
        self.blocks_file_sink_1.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'tmp/vector_source_data.dat', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_file_sink_4_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_head_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_4_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_file_sink_5, 0))
        self.connect((self.digital_gfsk_demod_0, 0), (self.blocks_file_sink_4, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.digital_gfsk_demod_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_file_sink_4_0_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "gfsk_test_graph")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)




def main(top_block_cls=gfsk_test_graph, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
