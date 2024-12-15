from textual.theme import Theme


downtown_theme = Theme(
	name="downtown",
	primary="#e41d59",
	secondary="#f76120",
	accent="#fd653d",
	foreground="#eacbd5",
	background="#29232e",
	success="#b7c664",
	warning="#cd854c",
	error="#cd5a4c",
	surface="#201b24",
	panel="#1a161d",
	dark=True,
	)

abyss_theme = Theme(
	name="abyss",
	primary="#8699da",
	secondary="#48b6bb",
	)



theme_registry = [downtown_theme, abyss_theme]