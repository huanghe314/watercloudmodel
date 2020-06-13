import click
from util import is_csv
from water_cloud_model import WaterCloudModel


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(exists=True))
@click.option('--alpha', help='parameter', type=float, required=True, prompt='alpha')
@click.option('--constA', help='parameter', type=float, required=True, prompt='A')
@click.option('--constB', help='parameter', type=float, required=True, prompt='B')
@click.option('--theta', help='parameter', type=float, required=True, prompt='theta')
@click.option('--columns', help='parameter', nargs=1, type=tuple, default=('soil_results',))
def main(input_file, output_file, alpha, consta, constb, theta, columns):
    if not is_csv(input_file):
        err = click.UsageError("File is not csv")
        err.show()
        raise err
    if not is_csv(output_file):
        err = click.UsageError("File is not csv")
        err.show()
        raise err
    # init water cloud model
    wcm = WaterCloudModel(input_file, output_file, alpha, consta, constb, theta, columns)
    wcm.compute_and_write_soil()


if __name__ == '__main__':
    main()