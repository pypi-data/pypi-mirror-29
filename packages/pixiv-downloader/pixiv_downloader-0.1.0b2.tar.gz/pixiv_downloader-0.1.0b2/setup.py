from distutils.core import setup

setup(
		name = "pixiv_downloader",
		version = "0.1.0b2",
		py_modules = ["pixiv_downloader"],
		author = "Anthorty",
		author_email = "hbys126@hotmail.com",
		url = "https://github.com/Anthorty/Python",
		description = "A simple tool to download pixiv's picture",
		long_description = "This is a tool to download pixiv's picture,it can specified date list and pages,and picture will be stored in folder that named by list and date.The picture filename is this picture's id,you can find it in website easy.",
		license = "GNU V3",
		install_requires = ["requests", "lxml", "BeautifulSoup4"],
		python_requires = ">=3.6",
		project_urls = {
				"Source":"https://github.com/Anthorty/Python",
				"Tracker":"https://github.com/Anthorty/Python/issues",
		},
	)
