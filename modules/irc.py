from modules import *

class Irc(Module):
    """IRC Module to provide chat commands for common IRC actions."""

    def __init__(self, server):
	    """Constructor."""
	    
	    Module.__init__(self, server)

    def _register_triggers(self):
        """Register module triggers."""

        self.add_trigger('ban')
        self.add_trigger('deop')
        self.add_trigger('devoice')
        self.add_trigger('invite')
        self.add_trigger('join')
        self.add_trigger('kick')
        self.add_trigger('msg')
        self.add_trigger('op')
        self.add_trigger('nick')
        self.add_trigger('part')
        self.add_trigger('quit')
        self.add_trigger('topic')
        self.add_trigger('unban')
        self.add_trigger('voice')
	
    @master
    def ban(self, event):
        """Bans a user from the channel.

        TODO: Work on better userhost handling.
        TODO: Have this interact with the user database
        """

        if self.num_args == 1:
            self.server.mode(event['target'], '+b %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.ban <hostmask>')
            
    def deop(self, event):
        """Deops a user from the specified channel or the current one."""
        
        if self.num_args == 0:
            self.server.mode(event['target'], '-o %s' % event['source']['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '-o %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.deop <nick>')
    
    def devoice(self, event):
        """Devoices a user from the specified channel or the current one."""

        if self.num_args == 0:
            self.server.mode(event['target'], '-v %s' % event['source']['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '-v %s ' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.devoice <nick>')
            	    
    def invite(self, event):
        """Invites a user to a specified channel or the current one."""
        
        if self.num_args == 1:
            self.server.invite(event['args'][0], event['target'])
        elif self.num_args == 2:
            self.server.invite(event['args'][0], event['args'][1])
        else:
            self.syntax_message(event['source']['nick'], '.invite <nick> [channel]')
                
    def join(self, event):
        """Makes the bot join a channel."""
        
        if self.num_args == 1:
            self.server.join(event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.join <channel>')
	
    def kick(self, event):
        """Kicks a user from the channel, with a kick message optional."""

        if self.num_args == 1:
            self.server.kick(event['target'], event['args'][0])
        elif self.num_args > 1:
            self.server.kick(event['target'], event['args'][0], ' '.join(event['args'][1:]))
        else:
            self.syntax_message(event['source']['nick'], '.kick <nick> [message]')
    
    def msg(self, event):
        """Messages a channel or user."""   
        
        if self.num_args > 2:
            self.server.privmsg(event['args'][0], event['args'][1:])
        else:
            self.syntax_message(event['source']['nick'], '.msg <nick/channel> [message]')
            
    def nick(self, event):
        """Changes the bot's nickname."""

        if self.num_args == 1:
            self.server.nick(event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.nick <newnick>')
    
    def op(self, event):
        """Ops a person in the specified channel, or the current channel."""
        
        if self.num_args == 0:
            self.server.mode(event['target'], '+o %s' % event['source']['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '+o %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.op <nick>')
            
    def part(self, event):
        """Makes the bot part a channel."""
        
        if self.num_args == 1:
            self.server.part(event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.part <channel>')
              
    def quit(self, event):
        """Makes the bot quit IRC."""
        
        message = "quit requested by %s" % event['source']['nick']
        self.server.disconnect(message)
        
    def topic(self, event):
        """Changes the channel's topic."""

        if self.num_args >= 1:
            self.server.topic(event['target'], ' '.join(event['args'][0:]))
        else:
            self.syntax_message(event['source']['nick'], '.topic <new topic>')
        
    def unban(self, event):
        """Unbans a user from the channel.
	    
	    TODO: Work on better userhost handling.
	    TODO: Have this interact with the user database
	    """

        if self.num_args == 1:
            self.server.mode(event['target'], '-b %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.unban <hostmask>')
            
    def voice(self, event):
        """Voices a user from the specified channel or the current one."""

        if self.num_args == 0:
            self.server.mode(event['target'], '+v %s' % event['source']['nick'])
        elif self.num_args == 1:
            self.server.mode(event['target'], '+v %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.voice <nick>')
