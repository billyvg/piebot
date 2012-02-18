from modules import *

class Irc(Module):
    """IRC Module to provide chat commands for common IRC actions."""

    def __init__(self, *args, **kwargs):
        """Constructor."""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        """Register module events and commands."""

        self.add_command('ban')
        self.add_command('deop')
        self.add_command('devoice')
        self.add_command('invite')
        self.add_command('join')
        self.add_command('kick')
        self.add_command('msg')
        self.add_command('op', 'giveop')
        self.add_command('nick')
        self.add_command('part')
        self.add_command('quit')
        self.add_command('topic')
        self.add_command('unban')
        self.add_command('voice')
        self.add_command('debug')
        self.add_command('python')

    def debug(self, event):
        print self.commands
        print self.modules

    def python(self, event):
        self.msg(event['target'], 'hi')

    @op
    def ban(self, event):
        """Bans a user from the channel.

        TODO: Work on better userhost handling.
        TODO: Have this interact with the user database
        """

        if self.num_args == 1:
            self.server.mode(event['target'], '+b %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.ban <hostmask>')

    @op
    def deop(self, event):
        """Deops a user from the specified channel or the current one."""

        if self.num_args == 0:
            self.server.mode(event['target'], '-o %s' % event['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '-o %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.deop <nick>')

    @op
    def devoice(self, event):
        """Devoices a user from the specified channel or the current one."""

        if self.num_args == 0:
            self.server.mode(event['target'], '-v %s' % event['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '-v %s ' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.devoice <nick>')

    @op
    def invite(self, event):
        """Invites a user to a specified channel or the current one."""

        if self.num_args == 1:
            self.server.invite(event['args'][0], event['target'])
        elif self.num_args == 2:
            self.server.invite(event['args'][0], event['args'][1])
        else:
            self.syntax_message(event['nick'], '.invite <nick> [channel]')

    @master
    def join(self, event):
        """Makes the bot join a channel."""

        if self.num_args == 1:
            self.server.join(event['args'][0])
        elif self.num_args == 2:
            self.server.join(event['args'][0], event['args'][1])
        else:
            self.syntax_message(event['nick'], '.join <channel>')

    @op
    def kick(self, event):
        """Kicks a user from the channel, with a kick message optional."""

        if self.num_args == 1:
            self.server.kick(event['target'], event['args'][0])
        elif self.num_args > 1:
            self.server.kick(event['target'], event['args'][0], ' '.join(event['args'][1:]))
        else:
            self.syntax_message(event['nick'], '.kick <nick> [message]')

    @master
    def msg(self, event):
        """Messages a channel or user."""

        if self.num_args > 1:
            self.server.privmsg(event['args'][0], ' '.join(event['args'][1:]))
        elif self.num_args == 1:
            self.server.privmsg(event['target'], ' '.join(event['args'][0:]))
        else:
            self.syntax_message(event['nick'], '.msg [nick/channel] <message>')

    @command
    def nick(self, event):
        """Changes the bot's nickname."""

        if self.num_args == 1:
            self.server.nick(event['args'][0])
        else:
            self.syntax_message(event['nick'], '.nick <newnick>')

    @op
    def giveop(self, event):
        """Ops a person in the specified channel, or the current channel."""

        if self.num_args == 0:
            self.server.mode(event['target'], '+o %s' % event['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '+o %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.op <nick>')

    @master
    def part(self, event):
        """Makes the bot part a channel."""

        if self.num_args == 1:
            self.server.part(event['args'][0])
        else:
            self.syntax_message(event['nick'], '.part <channel>')

    @master
    def quit(self, event):
        """Makes the bot quit IRC."""

        message = "quit requested by %s" % event['nick']
        self.server.disconnect(message)

    @op
    def topic(self, event):
        """Changes the channel's topic."""

        if self.num_args >= 1:
            self.server.topic(event['target'], ' '.join(event['args'][0:]))
        else:
            self.syntax_message(event['nick'], '.topic <new topic>')

    @op
    def unban(self, event):
        """Unbans a user from the channel.

        TODO: Work on better userhost handling.
        TODO: Have this interact with the user database
        """

        if self.num_args == 1:
            self.server.mode(event['target'], '-b %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.unban <hostmask>')

    @op
    def voice(self, event):
        """Voices a user from the specified channel or the current one."""

        if self.num_args == 0:
            self.server.mode(event['target'], '+v %s' % event['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '+v %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.voice <nick>')
