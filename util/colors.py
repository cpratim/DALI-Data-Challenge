from random import choice

bar_colors = [
	"#b91d47",
	"#00aba9",
	"#2b5797",
	"#e8c3b9",
	"#1e7145", 
	"#00548B",
	"#9B00B3",
	"#A9CB00",
	
]

bar_colors.extend([
	"#"+''.join([choice('0123456789ABCDEF') for i in range(6)]) for i in range(100)
])