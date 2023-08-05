import code

from basescript import BaseScript

from .convert import GWVec2WordVecSpace
from .wordvecspace import WordVecSpace
from .server import WordVecSpaceServer

class WordVecSpaceCommand(BaseScript):
    DESC = 'Word Vector Space command-line tool and Service'

    DEFAULT_PORT = 8900

    def convert(self):
        #FIXME: track issue to send logger
        convertor = GWVec2WordVecSpace(
                        self.args.input_dir,
                        self.args.output_dir,
                        self.args.num_vecs_per_shard)
        convertor.start()

    # FIXME: track issue to remove sharding or not
    DEFAULT_NUM_VECS_PER_SHARD = 0

    def interact(self):
        interact = WordVecSpace(self.args.input_dir)
        interact.load()

        vectors = interact.num_vectors
        dimensions = interact.num_dimensions

        print("Total number of vectors and dimensions in .npy file (%s, %s)" %(vectors, dimensions))
        print("")
        print("help")
        print("%s" %(dir(interact)))

        namespace=dict(WordVecSpace=interact)
        code.interact("WordVecSpace Console", local=namespace)

    def runserver(self):
        server = WordVecSpaceServer(self.args.input_dir, self.args.port, log=self.log)
        server.start()

    def define_subcommands(self, subcommands):
        super(WordVecSpaceCommand, self).define_subcommands(subcommands)

        convert_cmd = subcommands.add_parser('convert',
            help='Convert data in Google\'s Word2Vec format to WordVecSpace format')
        convert_cmd.set_defaults(func=self.convert)
        convert_cmd.add_argument('input_dir',
            help='Input directory containing Google Word2Vec format files'
                 ' (vocab.txt, vectors.bin)')
        convert_cmd.add_argument('output_dir',
            help='Output directory where WordVecSpace format files are produced')
        convert_cmd.add_argument('-n', '--num-vecs-per-shard',
            default=self.DEFAULT_NUM_VECS_PER_SHARD, type=int,
            help='Number of vectors per shard. 0 value ensures all vecs in one shard.')

        interact_cmd = subcommands.add_parser('interact',
                help='WordVecSpace Console')
        interact_cmd.set_defaults(func=self.interact)
        interact_cmd.add_argument('input_dir',
                help='Input directory containing WordVecSpace format files'
                ' (vocab.txt, vectors.npy)')

        runserver_cmd = subcommands.add_parser('runserver',
                help='WordVecSpace Service')
        runserver_cmd.set_defaults(func=self.runserver)
        runserver_cmd.add_argument('input_dir',
                help='Input directory containing WordVecSpace format files'
                ' (vocab.txt, vectors.npy)')
        runserver_cmd.add_argument('-p', '--port',
                default=self.DEFAULT_PORT, type=int,
                help='Port for wordvecspace service to run.')

def main():
    WordVecSpaceCommand().start()

if __name__ == '__main__':
    main()
