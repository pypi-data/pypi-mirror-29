import click

reflection = {
    'baidu': 'BaiDu',
    'bangumi': 'Bangumi'
}


@click.command()
@click.argument('source', required=True)
@click.option('-p', '--page', default=1, help='页数')
@click.option('-l', '--limit', default=None, help='限制条数')
def parse_command(page, limit, source):
    getattr(__import__('src'), reflection[source]).page(page, limit)


def main():
    parse_command()


if __name__ == '__main__':
    main()
