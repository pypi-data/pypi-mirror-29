# Copyright 2018 Patrick Kunzmann.
# This source code is part of the Biotite package and is distributed under the
# 3-Clause BSD License. Please see 'LICENSE.rst' for further information.

from .localapp import LocalApp
from .application import AppState, requires_state
from ..sequence.sequence import Sequence
from ..sequence.seqtypes import NucleotideSequence, ProteinSequence
from ..sequence.io.fasta.file import FastaFile
from ..sequence.align.alignment import Alignment
from ..temp import temp_file
import abc

__all__ = ["MSAApp"]


class MSAApp(LocalApp, metaclass=abc.ABCMeta):
    """
    Perform a multiple sequence alignment.
    
    Internally this creates a `Popen` instance, which handles
    the execution.
    
    Parameters
    ----------
    sequences : iterable object of Sequence
        The sequences to be aligned.
    bin_path : str, optional
        Path of the MSA software binary. By default, the default path
        will be used.
    mute : bool, optional
        If true, the console output goes into DEVNULL. (Default: True)
    """
    
    # Prevents overwriting of input and output files
    # of different MSAApp instancs
    _counter = 0
    
    def __init__(self, sequences, bin_path=None, mute=True):
        if bin_path is None:
            bin_path = self.get_default_bin_path()
        super().__init__(bin_path, mute)
        self._sequences = sequences
        MSAApp._counter += 1
        self._id = MSAApp._counter
        self._in_file_name  = temp_file("msa_in_{:d}.fa".format(self._id))
        self._out_file_name = temp_file("msa_out_{:d}.fa".format(self._id))

    def run(self):
        in_file = FastaFile()
        for i, seq in enumerate(self._sequences):
            in_file[str(i)] = str(seq)
        in_file.write(self._in_file_name)
        self.set_options(self.get_cli_arguments())
        super().run()
    
    def evaluate(self):
        super().evaluate()
        out_file = FastaFile()
        out_file.read(self._out_file_name)
        seq_dict = dict(out_file)
        out_seq_str = [None] * len(seq_dict)
        for i in range(len(self._sequences)):
            out_seq_str[i] = seq_dict[str(i)]
        trace = Alignment.trace_from_strings(out_seq_str)
        self._alignment = Alignment(self._sequences, trace, None)
    
    @requires_state(AppState.JOINED)
    def get_alignment(self):
        """
        Get the resulting multiple sequence alignment.
        
        Returns
        -------
        alignment : Alignment
            The global multiple sequence alignment.
        """
        return self._alignment
    
    @staticmethod
    @abc.abstractmethod
    def get_default_bin_path():
        """
        Get the default path for the MSA software executable.
        
        PROTECTED: Override when inheriting.
        
        Returns
        -------
        bin_path : str
            Absolute path to executable.
        """
        pass
    
    @abc.abstractmethod
    def get_cli_arguments(self):
        """
        Get the arguments for the MSA execution on the command line
        (the executable path is exclusive).
        
        PROTECTED: Override when inheriting.
        
        Returns
        -------
        arguments : list of str
            Command line arguments.
        """
        pass
    
    def get_input_file_path(self):
        """
        Get input file path (FASTA format).
        
        PROTECTED: Do not call from outside.
        
        Returns
        -------
        path : str
            Path of input file.
        """
        return self._in_file_name
    
    def get_output_file_path(self):
        """
        Get output file path (FASTA format).
        
        PROTECTED: Do not call from outside.
        
        Returns
        -------
        path : str
            Path of output file.
        """
        return self._out_file_name
    
    @classmethod
    def align(cls, sequences, bin_path=None):
        """
        Perform a multiple sequence alignment.
        
        This is a convenience function, that wraps the `MSAApp`
        execution.
        
        Parameters
        ----------
        sequences : iterable object of Sequence
            The sequences to be aligned
        bin_path : str, optional
            Path of the MSA software binary. By default, the default path
            will be used.
        
        Returns
        -------
        alignment : Alignment
            The global multiple sequence alignment.
        """
        app = cls(sequences, bin_path)
        app.start()
        app.join()
        return app.get_alignment()
