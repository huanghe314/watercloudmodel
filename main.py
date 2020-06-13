import click
from util import is_csv
from water_cloud_model import WaterCloudModel


@click.command()
@click.Argument('input_file', help='input file path', prompt='input file path', type=click.Path(exists=True))
@click.Argument('output_file', help='output file path', prompt='output file path', type=click.Path(exists=True))
@click.Option('--alpha', help='parameter', prompt='parameter alpha', type=click.FLOAT)
@click.Option('--A', help='parameter', prompt='parameter A', type=click.FLOAT)
@click.Option('--B', help='parameter', prompt='parameter B', type=click.FLOAT)
@click.Option('--theta', help='parameter', prompt='parameter theta', type=click.FLOAT)
@click.Option('--columns', help='parameter', prompt='output csv columns', type=click.Tuple)
def main(input_file, output_file, alpha, A, B, theta, columns):
    if not is_csv(input_file):
        err = click.UsageError("File is not csv")
        err.show()
        raise err
    if not is_csv(output_file):
        err = click.UsageError("File is not csv")
        err.show()
        raise err
    # init water cloud model
    wcm = WaterCloudModel(input_file, output_file, alpha, A, B, theta, columns)
    wcm.compute_and_write_soil()
