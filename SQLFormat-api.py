import sublime, sublime_plugin
from urllib.parse import urlencode
from urllib.request import urlopen
from json import loads


class SqlformatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                region = sublime.Region(0, self.view.size())

            sql = self.view.substr(region)
            params = {
                'sql': sql,
                'reindent': 1,
                'indent_width': 4,
                'identifier_case': 'lower',
                'keyword_case': 'upper',
                'strip_comments': 1,
            }
            data = urlencode(params)
            response = urlopen('http://sqlformat.org/api/v1/format', data=data.encode('utf8'))
            data = loads(response.read().decode('utf8'))
            result = data['result']
            self.view.replace(edit, region, result)
