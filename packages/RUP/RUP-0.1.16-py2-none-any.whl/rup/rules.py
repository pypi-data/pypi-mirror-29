import re, yaml
from string import Template

yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:python/regexp',
                                        lambda l, n: re.compile(l.construct_scalar(n)))


class Rule:

    def __init__(self, name, experiment, facility, image, raw_path, unpacked_path,
                 log_path, min_run_number, max_run_number):
        """

        :type facility: __Regexp
        :type experiment: __Regexp
        """
        self.__unpacked_path = unpacked_path
        self.__raw_path = raw_path
        self.__log_path = log_path
        self.name = name
        self.facility = facility
        self.experiment = experiment
        self.image = image
        self.min_run_number = min_run_number
        self.max_run_number = max_run_number

    def matches(self, run):
        """

        :type run: RunFiles
        """
        return self.facility.match(run.rup.get('facility', '')) \
               and self.experiment.match(run.rup.get('experiment', '')) \
               and self.min_run_number <= run.run <= self.max_run_number

    def unpacked_path(self, experiment, facility):
        return self.__template_path(self.__unpacked_path, experiment, facility)

    def log_path(self, experiment, facility):
        return self.__template_path(self.__log_path, experiment, facility)

    def raw_path(self, experiment, facility):
        return self.__template_path(self.__raw_path, experiment, facility)

    def __template_path(self, template, experiment, facility):
        return Template(template).safe_substitute(experiment=experiment, facility=facility)

    def __repr__(self):
        return "<Rule name: {}, exp: {}, facility: {}, image: {}>"\
            .format(self.name, self.experiment.pattern, self.experiment.pattern, self.image)


def parse_rules(stream):
    result = []
    yam = yaml.safe_load(stream)
    for entry, value in yam.iteritems():
        result.append(Rule(entry, value['experiment'],
                           value['facility'], value['image'],
                           value['raw_path'], value['unpacked_path'], value['log_path'],
                           value.get('min_run_number', -2**31),
                           value.get('max_run_number', 2**31)
                           ))
    return result


def parse_rules_from_file(path):
    with open(path, 'r') as f:
        return parse_rules(f)











