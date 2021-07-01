import os
import sys
import logging
import argparse
 
import gensim
from gensim import utils
 
logger = logging.getLogger(__name__)
 
 
def word2vec2tensor(word2vec_model_path, tensor_filename, binary=False):
    """Convert file in Word2Vec format and writes two files 2D tensor TSV file.
 
    File "tensor_filename"_tensor.tsv contains word-vectors, "tensor_filename"_metadata.tsv contains words.
 
    Parameters
    ----------
    word2vec_model_path : str
        Path to file in Word2Vec format.
    tensor_filename : str
        Prefix for output files.
    binary : bool, optional
        True if input file in binary format.
 
    """
    model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_path, binary=binary)
    outfiletsv = tensor_filename + '_tensor.tsv'
    outfiletsvmeta = tensor_filename + '_metadata.tsv'
 
    with utils.open(outfiletsv, 'wb') as file_vector, utils.open(outfiletsvmeta, 'wb') as file_metadata:
        for word in model.index2word:
            file_metadata.write(gensim.utils.to_utf8(word) + gensim.utils.to_utf8('\n'))
            vector_row = '\t'.join(str(x) for x in model[word])
            file_vector.write(gensim.utils.to_utf8(vector_row) + gensim.utils.to_utf8('\n'))
 
    logger.info("2D tensor file saved to %s", outfiletsv)
    logger.info("Tensor metadata file saved to %s", outfiletsvmeta)
 
 
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", required=True, help="Path to input file in word2vec format")
    parser.add_argument("-o", "--output", required=True, help="Prefix path for output files")
    parser.add_argument(
        "-b", "--binary", action='store_const', const=True, default=False,
        help="Set this flag if word2vec model in binary format (default: %(default)s)"
    )
    args = parser.parse_args()
 
    logger.info("running %s", ' '.join(sys.argv))
    word2vec2tensor(args.input, args.output, args.binary)
    logger.info("finished running %s", os.path.basename(sys.argv[0]))
