# -*- coding: utf-8 -*-
import os
import json
import colorama

from datetime import datetime
from termcolor import *
from time import sleep

from textual.app import App, ComposeResult
from textual.widgets import Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on






class RMD_LOG:


		



	def display_message_function(self, message, time=True):
		print("[%s] MESSAGE - %s"%(str(datetime.now()), str(message)))

		self.add_to_log_function(message, "MESSAGE", "text-secondary", time)


	def display_notification_function(self, message, time=True):
		print(colored("[%s] NOTIFICATION"%str(datetime.now()), "cyan")," - %s"%(str(message)))

		self.add_to_log_function(message, "NOTIFICATION", "text-accent", time)


	def display_warning_function(self, message, time=True):
		print(colored("[%s] WARNING"%str(datetime.now()), "yellow")," - %s"%(str(message)))

		self.add_to_log_function(message, "WARNING", "text-warning", time)


	def display_success_function(self, message, time=True):
		print(colored("[%s] SUCCESS"%str(datetime.now()), "green")," - %s"%(str(message)))

		self.add_to_log_function(message, "SUCCESS", "text-success", time)


	def display_error_function(self, message, time=True):
		print(colored("[%s] ERROR"%str(datetime.now()), "red")," - %s"%(str(message)))

		self.add_to_log_function(message, "ERROR", "text-error", time)



	def add_to_log_function(self, message, severity, color, time):
		if time == True:
			label = Label("[%s] %s : %s"%(severity, str(datetime.now()), str(message)))
		else:
			label = Label(str(message))
		label.styles.color = self.color_dictionnary[color]
		self.listview_log.append(ListItem(label))

