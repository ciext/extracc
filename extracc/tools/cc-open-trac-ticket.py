#!/usr/bin/env python
from __future__ import with_statement 

# cc-open-trac-ticket
# ----------------------------------------------------------------------------
# Copyright (c) 2004 Christophe LACOMBE
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

import sys

from trac.env import open_environment
from trac.ticket import Ticket
from trac.versioncontrol.api import NoSuchChangeset
from trac.ticket.notification import TicketNotifyEmail
from trac.web.href import Href

from optparse import OptionParser

parser = OptionParser()
depr = '(not used anymore)'
parser.add_option('-p', '--project', dest='projectPath',
				  help='Path to the Trac project.')
parser.add_option('-r', '--revision', dest='svnrevision',
				  help='Repository revision number.')
parser.add_option('-f', '--buildinfofile', dest='buildinfofile',
				  help='Repository revision number and build timestamp')
parser.add_option('-s', '--siteurl', dest='url', 
				  help=	'The base URL to the project\'s trac website (to which ' 
						'/ticket/## is appended).  If this is not specified, ' 
						'the project URL from trac.ini will be used.') 
parser.add_option('-u', '--ccurl', dest='ccurl', 
				  help=	'The CC report url on which the issue can be found') 

(options, args) = parser.parse_args(sys.argv[1:])

class CreateTicketForCC:

	def init_env(self, projectPath, url):
		self.env = open_environment(projectPath)
		

	def __init__(self, projectPath=options.projectPath, svnrevision=options.svnrevision,
				buildinfofile=options.buildinfofile, url=options.url, ccurl=options.ccurl):
		self.init_env( projectPath, url )
		if url is None:
			url = self.env.config.get('project', 'url') 
		
		self.env._href = Href(url) 
		self.env._abs_href = self.env._href
		
		if buildinfofile:
			with open(buildinfofile,'r') as f:
				variables=dict(filter(lambda i:len(i)==2, [line.strip().split('=') for line in f]))
			svnrevision=variables.get('svnrevision',svnrevision)
			cctimestamp=variables.get('cctimestamp')
			lastbuildsuccessful=variables.get('lastbuildsuccessful')
		
		# Do not open a ticket if last build was already not successful
		if lastbuildsuccessful == 'true':
			try:
				repos = self.env.get_repository()
				repos.sync()
				chgset = repos.get_changeset(svnrevision)
				chgsetmessage = chgset.message
				chgsetauthor = chgset.author
			except NoSuchChangeset:
				chgsetmessage = None
				chgsetauthor = None

			description = 'Opened automatically by CC due to build error after commit [%s]:\n\r%s' % (svnrevision, chgsetmessage)
			if ccurl:
				if cctimestamp:
					ccurl = '%s?log=log%s' % (ccurl, cctimestamp)
				description = '%s\n\r%s' % (description, ccurl)

			new_Ticket = Ticket(self.env)
			new_Ticket['owner'] = chgsetauthor
			new_Ticket['summary'] = 'CC build error after commit [%s]' % svnrevision
			new_Ticket['description'] = description
			new_Ticket['reporter'] = 'Cruise Control'
			new_Ticket['status'] = 'new'
			new_Ticket['type'] = 'defect'
			new_Ticket.insert()
			if buildinfofile:
				with open(buildinfofile,'a') as f:
					f.write('newticketid='+str(new_Ticket.id)+'\n')

			print 'INFO: New ticket #' + str(new_Ticket.id) + ' opened'
			
			tn = TicketNotifyEmail(self.env)
			tn.notify(new_Ticket)
		else:
			print 'INFO: Do not open a ticket on a not successful build'

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "For usage: %s --help" % (sys.argv[0])
	else:
		CreateTicketForCC()

