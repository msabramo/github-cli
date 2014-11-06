from gh.base import Command
from gh.util import tc
from github3.users import User


class ReposCommand(Command):
    name = 'repo.repos'
    usage = ('%prog [options] repos [options] [login] [sub-command]')
    summary = ('Interact with the Repositories API')
    fs = ("{d[bold]}{0.owner}/{0.name}{d[default]}\n  {1:.72}")
    fs2 = ("{d[bold]}{0.owner}/{0.name}{d[default]}")
    subcommands = {}

    def __init__(self):
        super(ReposCommand, self).__init__()
        self.parser.add_option('-t', '--type',
                               dest='type',
                               help='Which repositories to list',
                               choices=('all', 'owner', 'public', 'private',
                                        'member'),
                               default='all',
                               nargs=1,
                               )
        self.parser.add_option('-s', '--sort',
                               dest='sort',
                               help='How to sort the listed repositories',
                               choices=('created', 'updated', 'pushed',
                                        'name'),
                               nargs=1,
                               )
        self.parser.add_option('-d', '--direction',
                               dest='direction',
                               help='Which direction to list them in',
                               choices=('asc', 'desc'),
                               nargs=1,
                               )
        self.parser.add_option('-n', '--number',
                               dest='number',
                               help='Number of repositories to list',
                               type='int',
                               default=-1,
                               nargs=1,
                               )
        self.parser.add_option('-o', '--organization',
                               dest='organization',
                               help='List repositories of only a certain org',
                               )

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if opts.sort == 'name':
            opts.sort = 'full_name'

        if args:
            user = args.pop(0)
        else:
            user = self.get_user()

        kwargs = {
            'type': opts.type,
            'sort': opts.sort,
            'direction': opts.direction,
            'number': opts.number
        }

        if opts.organization:
            org = self.gh.organization(opts.organization)
            for key in ('sort', 'direction'):
                del kwargs[key]
            repos = org.iter_repos(**kwargs)
        elif opts.type == 'all':
            # These keys not supported by iter_all_repos
            for key in ('sort', 'direction', 'type'):
                del kwargs[key]
            repos = self.gh.iter_all_repos(**kwargs)
        elif isinstance(user, User):
            repos = self.gh.iter_repos(self.user, **kwargs)
        else:
            repos = self.gh.iter_repos(**kwargs)

        for repo in repos:
            if repo.description:
                fs = self.fs
                description = repo.description.encode('utf-8')
            else:
                fs = self.fs2
                description = None
            print(fs.format(repo, description, d=tc))

        return self.SUCCESS


ReposCommand()
