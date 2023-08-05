'''
Created on Jul 4, 2014

@author: eze
'''
import logging
import os

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import is_aa
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import Bio.SeqIO as bpio
from Bio.Data.IUPACData import protein_letters_3to1
from Bio.SeqUtils import seq1

from SNDG.WebServices import download_file
from SNDG import mkdir, execute

_log = logging.getLogger(__name__)

SIFTS_GO_TERMS = {"loop": "SO:0100012", "strand": "SO:0001111", "helix": "SO:0001114"}
HOMOLOGOUS = ["InterPro", "UniProt", "SCOP", "CATH", "NCBI"]


# ftp://ftp.ebi.ac.uk/pub/databases/pdb/derived_data/index/entries.idx


class PDBs(object):
    '''

    '''

    def __iter__(self):
        for index_dir in os.listdir(self.pdbs_dir):
            if len(index_dir) == 2:
                for x in os.listdir(self.pdbs_dir + "/" + index_dir):
                    if x.endswith(self.pdb_prefix):
                        yield x[3:7], self.pdbs_dir + "/" + index_dir + "/" + x

    def __init__(self, pdb_dir='/data/databases/pdb/'):
        '''

        '''
        self.pdb_dir = pdb_dir
        self.pdbs_dir = self.pdb_dir + 'divided/'

        self.pdb_seq_res_path = self.pdb_dir + "/pdb_seqres.txt"
        self.url_pdb_seq_res = "ftp://ftp.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt"

        self.url_pdb_files = 'ftp://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/'  # 00/pdb100d.ent.gz

        self.pdb_prefix = ".ent"
        self.pdb_download_extention = ".ent.gz"

        self.uncompress_file = True
        self.delete_compressed = True

    def download_pdb_seq_ses(self):
        download_file(self.url_pdb_seq_res, self.pdb_seq_res_path,ovewrite=True)

    def update_pdb_dir(self):
        assert os.path.exists(self.pdb_dir), "the target directory does not exists %s" % self.pdb_dir
        assert os.path.exists(self.pdb_seq_res_path), "the pdbseqres does not exists %s" % self.pdb_seq_res_path

        pdbs = set([x.id.split("_")[0] for x in bpio.parse(self.pdb_seq_res_path, "fasta")])
        total_pdbs = len(pdbs)
        pdb_count = 0
        for pdb in pdbs:
            try:
                pdb_count = pdb_count + 1
                _log.debug("pdbs: %s / %s" % (pdb_count, total_pdbs))
                mkdir(self.pdbs_dir + pdb[1:3])
                if not os.path.exists(self.pdb_path(pdb)):
                    download_file(self.url_pdb_files + pdb[1:3] + "/pdb" + pdb + self.pdb_download_extention,
                                  self.pdbs_dir + pdb[1:3] + "/pdb" + pdb + self.pdb_download_extention)
                    execute("gunzip " + self.pdbs_dir + pdb[1:3] + "/pdb" + pdb + self.pdb_download_extention)

            except Exception as ex:
                _log.warn(str(ex))

    def pdbs_seq_for_modelling(self, out_fasta=None,
                               pdbsIter=lambda: PDBs()):
        if not out_fasta:
            out_fasta = self.pdb_dir + "processed/seqs_from_pdb.fasta"
        pdbsIter = pdbsIter()
        with open(out_fasta, "w") as handle:
            for i, (pdb, pdb_file_path) in enumerate(pdbsIter):
                _log.debug("processing %s pdb %i" % (pdb, i))
                struct = PDBParser(PERMISSIVE=1, QUIET=1).get_structure(pdb, pdb_file_path)
                for chain in struct.get_chains():
                    residues = [x for x in chain.get_residues() if is_aa(x, standard=True)]
                    if residues:
                        seq = "".join([seq1(x.resname) for x in residues])
                        start = str(residues[0].id[1])
                        end = str(residues[-1].id[1])
                        record = SeqRecord(id="_".join([pdb, chain.id, start, end]), seq=Seq(seq))
                        bpio.write(record, handle, "fasta")

    def pdb_path(self, pdb):
        return self.pdbs_dir + pdb[1:3] + "/pdb" + pdb + ".ent"

    @staticmethod
    def sequence_from_residues(residues):
        return "".join([protein_letters_3to1[res.get_resname()[0] + res.get_resname()[1:3].lower()]
                        for res in residues])


if __name__ == '__main__':
    from SNDG import init_log

    init_log()
    pdbs = PDBs()
    os.environ["ftp_proxy"] = "http://proxy.fcen.uba.ar:8080"
    pdbs.update_pdb_dir()
    pdbs.pdbs_seq_for_modelling("/tmp/pepe.fasta")
