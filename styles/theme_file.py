from textual.theme import Theme


DOWNTOWN_THEME = Theme(
	name="downtown",
	primary="#e41d59",
	secondary="#f76120",
	accent="#ff6947",
	foreground="#eacbd5",
	background="#29232e",
	success="#b7c664",
	warning="#cd854c",
	error="#cd5a4c",
	surface="#201b24",
	panel="#1a161d",
	dark=True,
	)

ABYSS_THEME = Theme(
	name="abyss",
	primary="#8699da",
	secondary="#48b6bb",
	)



THEME_REGISTRY = [DOWNTOWN_THEME, ABYSS_THEME]