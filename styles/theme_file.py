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
	primary="#e15408",
	secondary="#bbaf99",
	background="#0f0e0d",
	surface="#0f0e0d",
	foreground="#ffffff",
	panel="#161414",
	warning="#ff9900",
	success="#59c337",
	error="#da4b12",
	dark=True,
	)



THEME_REGISTRY = [DOWNTOWN_THEME, ABYSS_THEME]