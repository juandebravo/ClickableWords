import sublime
import sublime_plugin
import webbrowser
import re


def open_url(url):
    webbrowser.get(
        sublime.load_settings('ClickableWords.sublime-settings').get(
            'clickable_word_browser')
    ).open(url, autoraise=True)


URL_MATCHES = []

for url in sublime.load_settings('ClickableWords.sublime-settings').get('URLS'):
    URL_MATCHES.append((url['regexpr'], url['url']))


class ClickableWordCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()[0]
        region = self.view.line(selection)
        line = self.view.substr(region)
        col = self.view.rowcol(selection.a)[1]
        pair = line[:col], line[col:]
        word = pair[0].split(' ')[-1] + pair[1].split(' ')[0]

        for url in URL_MATCHES:
            values = re.search(url[0], word)
            if values:
                u = url[1].format(*values.groups())
                open_url(u)
                break


class ClickableAllWordsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for url in URL_MATCHES:
            values = self.view.find_all(url[0])
            if values:
                for v in values:
                    v = re.search(url[0], self.view.substr(v))
                    u = url[1].format(*v.groups())
                    open_url(u)
